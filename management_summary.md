# Management Summary — Customer Feedback Dashboard

## 1. Phạm vi và KPI
- Số ticket trong phạm vi: **100**
- Thời gian: **15/09/2026 – 05/10/2026**
- Ticket khẩn cấp: **24/100 (24.0%)**
- Sentiment tiêu cực: **47/100 (47.0%)**
- Topic phổ biến nhất: **general_inquiry — 19 (19.0%)**

## 2. Phân bố topic
| Topic | Số ticket | Tỷ lệ |
|---|---:|---:|
| general_inquiry | 19 | 19.0% |
| complaint | 19 | 19.0% |
| transfer | 16 | 16.0% |
| card | 15 | 15.0% |
| fraud | 12 | 12.0% |
| loan | 11 | 11.0% |
| account | 4 | 4.0% |
| digital_banking | 4 | 4.0% |

## 3. Phân bố sentiment
| Sentiment | Số ticket | Tỷ lệ |
|---|---:|---:|
| neutral | 50 | 50.0% |
| negative | 47 | 47.0% |
| positive | 3 | 3.0% |

## 4. Xu hướng và spike theo ngày
- Trung bình: **4.76 ticket/ngày trong toàn bộ khoảng ngày**; ngưỡng spike: **trên 8.66 ticket/ngày** (mean + 1.5 SD; ngày không có ticket được tính là 0).
- **02/10/2026: 9 ticket** — vượt ngưỡng tham chiếu.
- **03/10/2026: 10 ticket** — vượt ngưỡng tham chiếu.

## 5. Khiếu nại / phản hồi tiêu biểu
- **T001** (card): “Mình làm mất ví, trong đó có thẻ ATM của ngân hàng. Mình cần khóa thẻ gấp.”
- **T003** (transfer): “Mình lỡ nhập sai số tài khoản người nhận khi chuyển 2 triệu, tiền đã đi rồi. Giờ làm sao lấy lại được?”
- **T004** (transfer): “Mình bấm chuyển tiền nhưng chờ mãi không nhận được mã OTP qua tin nhắn.”

## 6. Giả thuyết nguyên nhân cần xác minh
- Với phản hồi thuộc nhóm chuyển tiền, kiểm tra trạng thái giao dịch, thời gian đối soát và thông tin người nhận; đây là hướng điều tra, chưa phải kết luận.
- Với nhóm thẻ/gian lận, rà soát quy trình khóa thẻ, xác minh danh tính và cảnh báo giao dịch; không suy ra nguyên nhân chỉ từ nhãn topic.
- Đối chiếu các ticket tiêu cực/khẩn cấp với nhật ký hệ thống và hồ sơ xử lý trước khi kết luận nguyên nhân gốc rễ.

## 7. Phương pháp và giới hạn
- Topic/sentiment được lấy từ file phân tích có sẵn; không được coi là nhãn được dự đoán mới trong lần chạy này.
- Cluster được tính độc lập từ nội dung bằng TF-IDF ký tự và KMeans; cluster là nhóm văn bản tương đồng, không tự động chứng minh cùng nguyên nhân.
- Spike dùng quy tắc mô tả mean + 1.5 độ lệch chuẩn trên các ngày có dữ liệu; đây là tín hiệu để điều tra, không phải bằng chứng nhân quả.
- Giả thuyết nguyên nhân cần xác minh bằng log giao dịch và hồ sơ vận hành.
