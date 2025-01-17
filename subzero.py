from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client import file, client, tools
import base64
import re
import requests
import logging
import csv

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("unsubscribe_services.log"), logging.StreamHandler()]
)

# Initialize processed services to handle duplicates
processed_services = set()

def get_gmail_service():
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service

def search_emails(service, query):
    try:
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        return messages
    except HttpError as error:
        logging.error(f"Error searching emails: {error}")
        return []

def get_message_details(service, msg_id):
    try:
        message = service.users().messages().get(userId='me', id=msg_id, format='metadata').execute()
        headers = message['payload'].get('headers', [])
        return headers
    except HttpError as error:
        logging.error(f"Error getting message details: {error}")
        return []

def extract_sender(headers):
    for header in headers:
        if header['name'].lower() == 'from':
            return header['value']
    return None

def extract_unsubscribe_url(headers):
    for header in headers:
        if header['name'].lower() == 'list-unsubscribe':
            match = re.search(r'<(https?://[^>]+)>', header['value'])
            if match:
                return match.group(1)
    return None

def extract_unsubscribe_link_from_body(msg_body):
    pattern = re.compile(r'https?://[^\s"]*unsubscribe[^\s"]*', re.I)
    matches = pattern.findall(msg_body)
    return matches[0] if matches else None

def mark_email_as_read(service, msg_id):
    try:
        service.users().messages().modify(userId='me', id=msg_id, body={"removeLabelIds": ["UNREAD"]}).execute()
        logging.info(f"Marked email {msg_id} as read.")
    except HttpError as error:
        logging.error(f"Error marking email as read: {error}")

def unsubscribe(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info(f"Successfully unsubscribed: {url}")
        return True
    except requests.RequestException as error:
        logging.error(f"Failed to unsubscribe: {url}. Error: {error}")
        return False

def process_services(service, messages):
    services = []
    for msg in messages:
        msg_id = msg['id']
        headers = get_message_details(service, msg_id)
        sender = extract_sender(headers)

        if not sender:
            logging.warning(f"Email {msg_id} does not have a valid sender.")
            continue

        unsubscribe_url = extract_unsubscribe_url(headers)
        if not unsubscribe_url:
            try:
                message = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
                msg_body = base64.urlsafe_b64decode(message['raw'].encode('ASCII')).decode('utf-8', 'ignore')
                unsubscribe_url = extract_unsubscribe_link_from_body(msg_body)
            except Exception as e:
                logging.error(f"Error processing message body: {e}")

        if sender in processed_services:
            logging.info(f"Already processed: {sender}")
            mark_email_as_read(service, msg_id)
            continue

        if unsubscribe_url:
            success = unsubscribe(unsubscribe_url)
            if success:
                processed_services.add(sender)
                services.append((sender, "Unsubscribed"))
        else:
            logging.warning(f"No unsubscribe URL found for {sender}")
            services.append((sender, "No unsubscribe URL"))

        mark_email_as_read(service, msg_id)
    return services

def save_to_csv(services, filename="services.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Service", "Status"])
        for service, status in services:
            writer.writerow([service, status])
    logging.info(f"Services saved to {filename}")

def generate_report(services):
    total_services = len(services)
    unsubscribed_count = sum(1 for _, status in services if status == "Unsubscribed")
    failed_count = total_services - unsubscribed_count

    logging.info(f"Total services detected: {total_services}")
    logging.info(f"Successfully unsubscribed: {unsubscribed_count}")
    logging.info(f"Failed to unsubscribe: {failed_count}")

if __name__ == "__main__":
    # Setup Gmail API
    service = get_gmail_service()

    # Search for all emails with List-Unsubscribe header
    query = "List-Unsubscribe OR category:promotions OR unsubscribe OR manage preferences"
    messages = search_emails(service, query)

    if not messages:
        logging.info("No subscription emails found.")
        exit()

    # Process emails and unsubscribe
    logging.info(f"Found {len(messages)} emails to process.")
    services = process_services(service, messages)

    # Save results to CSV
    save_to_csv(services)

    # Generate and log the report
    generate_report(services)
