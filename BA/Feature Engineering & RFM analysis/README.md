## Giả định và quyết định

- Đánh giá tại **01/10/2026**; chỉ lấy ngày từ **01/10/2025 đến hết 30/09/2026**. Không dùng ngày hiện tại của máy.
- Chỉ tính `SUCCESS`, tiền hữu hạn và lớn hơn 0, thuộc `CARD_PAYMENT`, `TRANSFER_OUT`, `BILL_PAYMENT`, `ATM_WITHDRAWAL`. Đây là hoạt động chi ra; bỏ `TRANSFER_IN`, `CASH_DEPOSIT` để không trộn tiền vào với chi tiêu.
- M là khối lượng giao dịch chi ra tính bằng VND, không phải doanh thu/lợi nhuận hoặc giá trị vòng đời khách hàng. Rút ATM cũng chỉ phản ánh hoạt động tài khoản, không chứng minh tiền đã được tiêu dùng.
- Kiểm tra mã khách không thiếu/trùng, giao dịch có khách tương ứng và không trước ngày mở tài khoản. Các điều kiện này đều đúng trên dữ liệu được giao; nếu không đúng, notebook dừng để kiểm tra thay vì âm thầm sửa.
- Loại trùng `transaction_id` trước. Các bản sao hiện tại giống nhau toàn bộ; giữ dòng đầu. Nếu cùng mã nhưng nội dung khác nhau, notebook dừng để kiểm tra.
- Tiếp theo lần lượt loại: ngày thiếu/không hợp lệ; tiền thiếu/không hữu hạn/không dương; trạng thái không thành công; loại không chọn; trước kỳ; từ ngày đánh giá trở đi. Bảng thống kê đếm lý do đầu tiên của mỗi dòng, không đếm trùng.
- Không nội suy ngày hoặc tiền. Các giá trị thiếu còn lại được xem trong notebook; mã hoặc ngày mở tài khoản thiếu sẽ làm kiểm tra thất bại.
- Ghép trái từ danh sách khách hàng: giữ đủ 1.000 khách. R là số ngày từ giao dịch hợp lệ cuối trong kỳ; F là số giao dịch; M là tổng tiền.
- Khách F = 0 có M = 0, R trống, ba điểm bằng 1, nhóm Hibernating. R trống không có nghĩa là giao dịch gần nhất cách 0 ngày. Nếu F > 0 mà R hoặc M thiếu, dừng vì dữ liệu không nhất quán.
- Với F > 0, dùng hạng trung bình theo phần trăm rồi chia năm khoảng 20%; điểm F, M tăng theo giá trị; R đảo chiều. Ties nhận cùng điểm, nên quy mô mỗi nhóm điểm có thể không bằng nhau. Không dùng thứ tự mã khách để phá ties. Các điểm là tương đối trong bộ khách hiện tại.
- Phân nhóm theo thứ tự: F = 0 → Hibernating; cả ba điểm >= 4 → Champions; R >= 3 và F >= 3 → Loyal; R >= 4 → Potential; R <= 2 và (F >= 3 hoặc M >= 3) → At Risk; R <= 2 → Hibernating; còn lại → Regular. Trong quy tắc này R, F, M là **điểm**, không phải giá trị thô. Quy tắc đầu tiên khớp được chọn.
- `synthetic_profile_hint` bị loại ngay sau khi đọc kích thước bảng; không dùng chấm điểm, chọn ngưỡng hay kiểm chứng phân nhóm. Tuổi, thành phố, kênh đăng ký không dùng chấm điểm.

## Kết quả chính

Còn 26.818 giao dịch hợp lệ, 972 khách có hoạt động, 28 khách không có giao dịch hợp lệ**. Tổng M khoảng **32,890 tỷ VND**. Champions và Loyal cộng lại chiếm khoảng **68,5% tổng M**. Notebook chứa bảng chi tiết, các đề xuất chiến dịch và KPI, đặc trưng bổ sung, hạn chế, leakage, bias, đánh giá độ ổn định và trả lời ba câu hỏi thảo luận.

