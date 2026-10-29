# Banking CLV – bài tập Chapter 5

## Cách chạy lại
1. Cài thư viện: `pandas numpy matplotlib jupyter`.
2. Mở `clv_banking.ipynb` trong thư mục này (cùng cấp với `Banking_CLV_Data_20000/`) và chạy **Run All**.

## Các file
| File | Nội dung |
|---|---|
| `clv_banking.ipynb` | Toàn bộ phân tích: làm sạch, CLV, segment, chiến dịch, độ nhạy |
| `customer_clv.csv` | Kết quả cuối, 1 dòng mỗi khách (20.000 dòng) |
| `report.md` | Báo cáo (sẽ đổi sang PDF) |
| `output/` | Biểu đồ, `cleaning_log.csv`, `clv_by_year.csv`, `scenario_summary.csv`, `campaign_selected.csv`, `unmatched_ids.csv` |

## Giả định
- Mốc tính 2026-10-01, d = 10%, 3 năm, contribution nhận cuối năm, không tăng trưởng, không giá trị cuối kỳ, khách rời đi là rời vĩnh viễn.
- m = fee + net_interest − servicing_cost − expected_credit_loss, giữ nguyên mỗi năm.
- Chiến dịch: r' = min(1, r + 0,03), chi phí 100.000 VND/khách, tối đa 100 khách, ngân sách 10 triệu.

## Quyết định làm sạch
- Bỏ dòng trùng hoàn toàn (300). Dòng cùng ID nhưng số khác nhau sẽ bị bỏ và gắn `conflicting_rows` (dữ liệu này không có).
- Bỏ ID không có trong roster (100), không thêm vào roster.
- Không điền giá trị thiếu, không tự sửa giá trị sai. Khách đó có CLV trống.
- Giữ giá trị 0 thật và contribution/CLV âm.

## Các cột trong `customer_clv.csv`
| Cột | Ý nghĩa |
|---|---|
| `customer_id` | Mã khách |
| `annual_contribution_vnd` | m (VND/năm). Trống nếu dữ liệu khách không hợp lệ |
| `annual_retention_rate` | r. Trống nếu dữ liệu khách không hợp lệ |
| `clv_3yr_vnd` | CLV 3 năm (VND), có thể âm. **Trống = không tính được**, khác với 0 là giá trị thật bằng 0 |
| `clv_rank` | Hạng theo CLV giảm dần (1 = cao nhất), hòa thì ID nhỏ hơn trước. Trống nếu không có CLV |
| `segment` | Nhóm khách (xem dưới) |
| `quality_status` | `ok`, `missing_input`, `invalid_input`, `partial_period`, `no_economics_row`, `conflicting_rows` |
| `campaign_delta_vnd` | CLV(r') − CLV(r) − 100.000. Trống nếu không có CLV |
| `selected` | 1 nếu được chọn cho chiến dịch, 0 nếu không |

Thứ tự ưu tiên khi một khách có nhiều lỗi: conflicting_rows, no_economics_row, partial_period, missing_input, invalid_input. Trong dữ liệu này các lỗi không chồng nhau.

## Quy tắc segment (kiểm tra từ trên xuống)
1. Unscored: CLV trống
2. Negative Value: CLV < 0
3. Zero Value: CLV = 0
4. High Value / Stable: CLV ≥ P75 của CLV dương (7.963.869 VND) và r ≥ 0,75
5. High Value / At Risk: CLV ≥ P75 của CLV dương và r < 0,75
6. Low Positive Value: CLV dương còn lại

## Quy tắc hòa (tie)
Xếp hạng và chọn chiến dịch đều sắp theo giá trị giảm dần, nếu bằng nhau thì `customer_id` nhỏ hơn đứng trước.
