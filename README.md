# 📡 GitHub Daily Radar (Săn dự án Hot hàng ngày)

Công cụ tự động quét, phân loại, lưu trữ lũy tiến vào **Excel**, xuất **Web Dashboard/Markdown**, và gửi thông báo qua **Telegram** về các repository mã nguồn mở nổi bật nhất trên GitHub theo các chủ đề: **AI Agents, Trợ lý ảo Sci-Fi (JARVIS), Anime/VTuber AI, và Công cụ Dev đỉnh cao**.

---

## ✨ Tính năng nổi bật

- 🤖 **Bộ lọc thông minh:** Quét các dự án mới tạo hoặc có lượng sao tăng trưởng đột biến.
- 📊 **Cơ sở dữ liệu Excel lũy tiến (`.xlsx`):** Tự động thêm dự án mới và cập nhật số sao/forks cho dự án cũ, không bao giờ bị trùng lặp.
- 📱 **Thông báo Telegram Bot:** Gửi tóm tắt dự án hot nhất kèm link trực tiếp về điện thoại/nhóm chat mỗi ngày.
- 🎨 **Giao diện Web Dark Mode Sci-Fi:** Báo cáo HTML hiện đại với hiệu ứng kính mờ, bộ lọc danh mục và thanh tìm kiếm trực tiếp.
- 📝 **Xuất báo cáo Markdown:** Lưu trữ ghi chú nhanh theo từng ngày.

---

## 🚀 Hướng dẫn sử dụng

### 1. Chạy ngay:
```bash
python main.py
```
*Công cụ sẽ quét dữ liệu, cập nhật file Excel, gửi thông báo Telegram (nếu bật), tạo báo cáo HTML và mở trên trình duyệt.*

### 2. Các tùy chọn lệnh:
- Không mở trình duyệt tự động:
  ```bash
  python main.py --no-open
  ```
- Dùng GitHub Token cá nhân (tùy chọn, để tăng giới hạn API):
  ```bash
  python main.py --token your_github_personal_token
  ```

---

## 📱 Hướng dẫn kích hoạt thông báo Telegram

Mở file [`config.json`](config.json) và thiết lập:

```json
"telegram": {
  "enabled": true,
  "bot_token": "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ",
  "chat_id": "123456789"
}
```

### Cách lấy Bot Token & Chat ID siêu nhanh:
1. **Lấy `bot_token`:** Nhắn tin cho [@BotFather](https://t.me/BotFather) trên Telegram $\rightarrow$ Gõ `/newbot` $\rightarrow$ Làm theo hướng dẫn để nhận API Token.
2. **Lấy `chat_id`:** Nhắn bất kỳ tin gì cho [@userinfobot](https://t.me/userinfobot) trên Telegram để xem ID của bạn (ví dụ: `123456789`).
3. Nhắn cho con bot mới tạo của bạn một chữ `hi` (để bot có quyền gửi tin nhắn cho bạn).

---

## 📊 File Excel lưu trữ ở đâu?

Tất cả dự án quét được qua các ngày sẽ được tích lũy tại:
📁 **`reports/github_radar_archive.xlsx`**
*(Bao gồm: Tên dự án, Stars, Forks, Ngôn ngữ, Mô tả, Tags, Link truy cập có thể click trực tiếp)*.
