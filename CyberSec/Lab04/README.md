# Lab 04 - Modes of Operation (IT4010E)
## Cấu trúc code

| Hàm | Vai trò |
|---|---|
| `chunks` | Chia dữ liệu thành các block 16 byte (block cuối có thể ngắn) |
| `xor` | XOR hai chuỗi bytes, cắt về độ dài ngắn hơn (dùng cho block cuối ngắn) |
| `pad_ecb`, `unpad_ecb` | Padding 10…0 (`80 00 … 00`); `unpad_ecb` ném `ValueError` nếu sai |
| `pad_pkcs5`, `unpad_pkcs5` | Padding PKCS5; `unpad_pkcs5` ném `ValueError` nếu sai |
| `ecb_encrypt` ... `ctr_encrypt` | Mã hoá từng mode: nhận `str`, trả `bytes` (IV ngẫu nhiên `os.urandom` được ghép vào đầu, trừ ECB) |
| `ecb_decrypt` ... `ctr_decrypt` | Giải mã từng mode: nhận `bytes`, trả `str` |

Thư viện chỉ được dùng cho AES một block (`aes_enc_block`, `aes_dec_block`).

## Công thức giải mã đã dùng

- **ECB:** `x_i = Dec_k(y_i)`, rồi bỏ padding 10…0.
- **CBC:** `x_i = Dec_k(y_i) ⊕ y_{i-1}`, với `y_{-1} = IV`; nối toàn bộ rồi bỏ padding PKCS5 một lần.
- **OFB:** `s_i = Enc_k(s_{i-1})`, `s_{-1} = IV`; `x_i = y_i ⊕ s_i`. Keystream không phụ thuộc plaintext hay ciphertext.
- **CFB:** `x_i = y_i ⊕ Enc_k(y_{i-1})`, `y_{-1} = IV`. Khác OFB ở chỗ đầu vào của `Enc` là **ciphertext block trước**.
- **CTR:** `x_i = y_i ⊕ Enc_k((IV + i) mod 2^128)`, IV là số nguyên 128-bit big-endian.

Với OFB, CFB, CTR không có padding; block cuối ngắn được XOR với đúng số byte tương ứng của keystream.
16 byte đầu của ciphertext là IV (trừ ECB).

## Trả lời các câu hỏi

| Câu | Mode | Plaintext |
|---|---|---|
| 1 | ECB | `ECB is not safe.Really, I mean: ECB is not safe.` |
| 2 | ECB | `Tux is visible!` |
| 3 | ECB | `Transfer $1.00 from Oscar at bank A to bank B.` |
| 4 | CBC | `Basic CBC mode encryption needs padding.` |
| 5 | CBC | `Our implementation uses rand. IV` |
| 6 | CBC | `Never let a CBC IV be predictable to attackers.` |
| 7 | CBC | `Hello, SoICT!` |
| 8 | OFB | `OFB turns a block cipher into a synchronous stream cipher.` |
| 9 | OFB | `The OFB keystream never depends on the message.` |
| 10 | CFB | `In CFB mode each ciphertext block feeds the next block.` |
| 11 | CFB | `CFB recovers from a corrupted block after one more block.` |
| 12 | CTR | `CTR mode lets you build a stream cipher from a block cipher.` |
| 13 | CTR | `Always avoid the two time pad!` |
| 14 | CTR | `A counter is a full 128-bit integer, so every carry must propagate.` |
| 15 | CTR | `Counters wrap around modulo 2^128.` |

### Nhận xét theo gợi ý của đề

- **Câu 1 (so sánh `y0` và `y2`):** hai block ciphertext giống hệt nhau (`a1dc4d1f…4861`). ECB là deterministic nên hai block plaintext giống nhau (`ECB is not safe.`) cho ra hai block ciphertext giống nhau. Kẻ tấn công thấy được cấu trúc lặp của plaintext mà không cần key, nên ECB không an toàn.
- **Câu 13:** nhắc tới "two time pad". Ở CTR, dùng lại cùng (key, IV) cho hai thông điệp thì `y ⊕ y' = x ⊕ x'`, lộ quan hệ giữa hai plaintext.
- **Câu 14, 15:** IV nằm sát hoặc bằng `ff…ff`, nên counter phải được cộng như số nguyên 128-bit, có nhớ lan qua các byte và wrap về 0 (mod 2^128). Code dùng `int.from_bytes(..., "big")` và `% (1 << 128)`.

## Ghi chú

- Mã hoá nhận `str` (UTF-8) và trả `bytes`; giải mã làm ngược lại, nên `decrypt(encrypt(m)) == m`.
- ECB, CBC luôn thêm padding (kể cả khi plaintext đã chia hết cho 16); OFB, CFB, CTR không padding, ciphertext dài hơn plaintext đúng 16 byte (IV).
- Padding sai (ECB: không có byte `80`; CBC: không đúng PKCS5) bị từ chối bằng `ValueError`.
