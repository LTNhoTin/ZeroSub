# Automatic Email Unsubscriber in Python (Supports Gmail)

## Get an API Client ID and Secret

1. Use [this wizard](https://console.developers.google.com/start/api?id=gmail) to create or select a project in the Google Developers Console and automatically turn on the API. Click **Continue**, then **Go to credentials**.
2. On the **Add credentials to your project** page, click the **Cancel** button.
3. At the top of the page, select the **OAuth consent screen** tab. Select an **Email address**, enter a **Product name** if not already set, and click the Save button.
4. Select the **Credentials** tab, click the **Create credentials** button and select **OAuth client ID**.
5. Select the application type **Desktop app**, enter the name "Unsubscribe", and click the **Create** button.
6. Click **OK** to dismiss the resulting dialog.
7. Click the Download button to the right of the client ID.
8. Move this file to your working directory and rename it `client_secret.json`.

## Usage Instructions

1. Ensure you have Python 3.6 or later installed on your system.
2. Install dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python zerosub.py
   ```
4. The script will automatically:
   - Search for emails matching specific unsubscribe patterns.
   - Attempt to unsubscribe from detected services.
   - Mark processed emails as read.
   - Save the results to `services.csv`.

## Features

1. **Automatic detection of subscription emails**:
   - Searches for emails containing `List-Unsubscribe` headers or unsubscribe links in the content.
   - Processes emails in categories like `Promotions` and `Social`.
2. **Unsubscription handling**:
   - Attempts to unsubscribe using available links or email headers.
3. **Duplicate handling**:
   - Avoids unsubscribing from the same service multiple times during a session.
4. **Mark emails as read**:
   - Marks processed emails as read to reduce inbox clutter.
5. **Export results**:
   - Saves all detected services and their statuses to a CSV file for review.
6. **Detailed logging**:
   - Logs all activities and errors in `unsubscribe_services.log`.

## Output Explanation

1. **"Unsubscribed from: Sender_Name"**:
   - Unsubscription was successful. The service was unsubscribed using a valid unsubscribe URL.
2. **"Could not unsubscribe: Sender_Name"**:
   - No unsubscribe link was found in the email header or content. The service could not be unsubscribed.
3. **"Already processed: Sender_Name"**:
   - This service has already been processed during the session. The email is marked as read without additional actions.
4. **"No subscription emails found."**:
   - No matching emails were detected for unsubscription based on the search query.
5. **"Failed to unsubscribe: URL"**:
   - An error occurred during the HTTP request to the unsubscribe URL.
6. **Emails marked as read:**
   - All emails, whether successfully unsubscribed or not, are marked as read after processing.

## Advanced Options

- Customize search queries in the script to target specific email categories or keywords:
  ```python
  query = "List-Unsubscribe OR category:promotions OR unsubscribe OR manage preferences"
  ```

- Modify `services.csv` output format or add additional fields as needed.

## Contributions

Feel free to fork, improve, and contribute to this project. Feedback is welcome!

---

# Công cụ tự động hủy đăng ký email bằng Python (Hỗ trợ Gmail)

## Nhận ID và Secret API Client

1. Sử dụng [trình hướng dẫn này](https://console.developers.google.com/start/api?id=gmail) để tạo hoặc chọn một dự án trong Google Developers Console và tự động bật API. Nhấn **Continue**, sau đó nhấn **Go to credentials**.
2. Trên trang **Add credentials to your project**, nhấn nút **Cancel**.
3. Ở đầu trang, chọn tab **OAuth consent screen**. Chọn một **Email address**, nhập **Product name** nếu chưa có, và nhấn nút Save.
4. Chọn tab **Credentials**, nhấn nút **Create credentials** và chọn **OAuth client ID**.
5. Chọn loại ứng dụng **Desktop app**, nhập tên "Unsubscribe" và nhấn nút **Create**.
6. Nhấn **OK** để đóng hộp thoại.
7. Nhấn nút Download bên phải ID Client.
8. Di chuyển tệp này vào thư mục làm việc của bạn và đổi tên thành `client_secret.json`.

## Hướng dẫn sử dụng

1. Đảm bảo bạn đã cài đặt Python 3.6 hoặc mới hơn trên hệ thống của mình.
2. Cài đặt các thư viện cần thiết bằng cách chạy lệnh:
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy script:
   ```bash
   python zerosub.py
   ```
4. Script sẽ tự động:
   - Tìm kiếm các email khớp với các mẫu hủy đăng ký.
   - Cố gắng hủy đăng ký khỏi các dịch vụ được phát hiện.
   - Đánh dấu các email đã xử lý là đã đọc.
   - Lưu kết quả vào tệp `services.csv`.

## Tính năng

1. **Tự động phát hiện email đăng ký**:
   - Tìm kiếm email chứa header `List-Unsubscribe` hoặc liên kết hủy đăng ký trong nội dung.
   - Xử lý email trong các danh mục như `Promotions` và `Social`.
2. **Xử lý hủy đăng ký**:
   - Thực hiện hủy đăng ký thông qua các liên kết hoặc header có sẵn.
3. **Xử lý trùng lặp**:
   - Tránh hủy đăng ký cùng một dịch vụ nhiều lần trong một phiên.
4. **Đánh dấu email là đã đọc**:
   - Đánh dấu các email đã xử lý là đã đọc để giảm sự lộn xộn trong hộp thư.
5. **Xuất kết quả**:
   - Lưu tất cả các dịch vụ được phát hiện và trạng thái của chúng vào tệp CSV để xem xét.
6. **Ghi log chi tiết**:
   - Ghi lại tất cả hoạt động và lỗi trong `unsubscribe_services.log`.

## Giải thích đầu ra

1. **"Unsubscribed from: Sender_Name"**:
   - Hủy đăng ký thành công. Dịch vụ đã được hủy bằng URL hợp lệ.
2. **"Could not unsubscribe: Sender_Name"**:
   - Không tìm thấy liên kết hủy đăng ký trong header hoặc nội dung email.
3. **"Already processed: Sender_Name"**:
   - Dịch vụ này đã được xử lý trước đó trong phiên. Email được đánh dấu là đã đọc.
4. **"No subscription emails found."**:
   - Không phát hiện email nào khớp để hủy đăng ký dựa trên truy vấn tìm kiếm.
5. **"Failed to unsubscribe: URL"**:
   - Đã xảy ra lỗi khi gửi yêu cầu HTTP đến URL hủy đăng ký.
6. **Email được đánh dấu là đã đọc:**
   - Tất cả email, dù hủy thành công hay không, đều được đánh dấu là đã đọc sau khi xử lý.

## Tùy chọn nâng cao

- Tùy chỉnh truy vấn tìm kiếm trong script để nhắm mục tiêu các danh mục email hoặc từ khóa cụ thể:
  ```python
  query = "List-Unsubscribe OR category:promotions OR unsubscribe OR manage preferences"
  ```

- Thay đổi định dạng đầu ra của `services.csv` hoặc thêm các trường bổ sung nếu cần.

## Đóng góp

Hãy tự do fork, cải tiến và đóng góp cho dự án này. Mọi phản hồi đều được hoan nghênh!
