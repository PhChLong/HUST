import os
from Crypto.Cipher import AES

with open("CyberSec/Lab04/lab04_questions.txt") as f:
    lines = f.readlines()[4:]

BLOCK_SIZE = 16
def xor(bytes_1:bytes, bytes_2:bytes) -> bytes:
    n = min(len(bytes_2), len(bytes_1))
    return bytes(x ^ y for x, y in zip(bytes_1[:n], bytes_2[:n]))

def aes_enc_block(key: bytes, block: bytes) -> bytes:
    return AES.new(key, AES.MODE_ECB).encrypt(block)

def aes_dec_block(key: bytes, block: bytes) -> bytes:
    return AES.new(key, AES.MODE_ECB).decrypt(block)

def unpad_ecb(pt:bytes) -> bytes:
    pt_unpaded = pt.rstrip(b"\x00")
    if len(pt_unpaded) == 0 or pt_unpaded[-1] != 0x80:
        raise ValueError("invalid padding")
    return pt_unpaded[:-1]

def unpad_pkcs5(pt: bytes) -> bytes:
    if len(pt) == 0 or len(pt) % BLOCK_SIZE != 0:
        raise ValueError("...")
    n: int = pt[-1]
    if not (1 <= n <= BLOCK_SIZE) or pt[-n:] != bytes([n]) * n:
        raise ValueError("invalid padding")
    return pt[:-n]

def pad_ecb(pt: bytes) -> bytes:
    missing: int = BLOCK_SIZE - len(pt) % BLOCK_SIZE
    return pt + b"\x80" + b"\x00" * (missing - 1)

def pad_pkcs5(pt: bytes) -> bytes:
    missing: int = BLOCK_SIZE - len(pt) % BLOCK_SIZE
    return pt + bytes([missing]) * missing

def chunks(data: bytes, n: int = 16) -> list[bytes]:
    return [data[i:i + n] for i in range(0, len(data), n)]

def ecb_decrypt(key: bytes, message: bytes) -> str:
    blocks = chunks(message, BLOCK_SIZE)
    parts: list[bytes] = []
    decoded_message = ""
    for block in blocks:
        decoded_block = aes_dec_block(key, block)
        parts.append(decoded_block)
    decoded = b"".join(parts)
    plain_text = unpad_ecb(decoded).decode("utf-8")
    return plain_text

def cbc_decrypt(key: bytes, message: bytes) -> str:
    blocks = chunks(message, BLOCK_SIZE)
    IV, blocks = blocks[0], blocks[1:]
    y_prev = IV
    parts: list[bytes] = []
    for block in blocks:
        decoded_block = xor(aes_dec_block(key, block), y_prev)
        parts.append(decoded_block)
        y_prev = block
    decoded: bytes = b"".join(parts)
    decoded = unpad_pkcs5(decoded)
    plain_text: str = decoded.decode("utf-8")
    return plain_text

def ofb_decrypt(key: bytes, message: bytes) -> str:
    blocks = chunks(message, BLOCK_SIZE)
    IV, blocks = blocks[0], blocks[1:]
    s_prev = IV
    parts: list[bytes] = []
    for block in blocks:
        s_cur = aes_enc_block(key, s_prev)
        decoded_block = xor(s_cur, block)
        parts.append(decoded_block)
        s_prev = s_cur
    decoded: bytes = b"".join(parts)
    plain_text: str = decoded.decode("utf-8")
    return plain_text

def cfb_decrypt(key: bytes, message: bytes) -> str:
    blocks = chunks(message, BLOCK_SIZE)
    IV, blocks = blocks[0], blocks[1:]
    s_prev = IV
    parts: list[bytes] = []
    for block in blocks:
        s_cur = aes_enc_block(key, s_prev)
        decoded_block = xor(s_cur, block)
        parts.append(decoded_block)
        s_prev = block
    decoded: bytes = b"".join(parts)
    plain_text: str = decoded.decode("utf-8")
    return plain_text

def ctr_decrypt(key: bytes, message: bytes) -> str:
    blocks = chunks(message, BLOCK_SIZE)
    IV, blocks = blocks[0], blocks[1:]
    IV_int = int.from_bytes(IV, "big")
    parts: list[bytes] = []
    for i, block in enumerate(blocks):
        IV_cur: bytes = ((IV_int + i) % (1 << 128)).to_bytes(16, "big")
        decoded_block = xor(aes_enc_block(key, IV_cur), block)
        parts.append(decoded_block)
    decoded: bytes = b"".join(parts)
    plain_text: str = decoded.decode("utf-8")
    return plain_text

def ecb_encrypt(key: bytes, plain_text: str) -> bytes:
    blocks = chunks(pad_ecb(plain_text.encode("utf-8")), BLOCK_SIZE)
    parts: list[bytes] = []
    for block in blocks:
        parts.append(aes_enc_block(key, block))
    return b"".join(parts)

def cbc_encrypt(key: bytes, plain_text: str) -> bytes:
    blocks = chunks(pad_pkcs5(plain_text.encode("utf-8")), BLOCK_SIZE)
    IV: bytes = os.urandom(BLOCK_SIZE)
    y_prev = IV
    parts: list[bytes] = [IV]
    for block in blocks:
        y_prev = aes_enc_block(key, xor(block, y_prev))
        parts.append(y_prev)
    return b"".join(parts)

def ofb_encrypt(key: bytes, plain_text: str) -> bytes:
    blocks = chunks(plain_text.encode("utf-8"), BLOCK_SIZE)
    IV: bytes = os.urandom(BLOCK_SIZE)
    s_prev = IV
    parts: list[bytes] = [IV]
    for block in blocks:
        s_cur = aes_enc_block(key, s_prev)
        parts.append(xor(s_cur, block))
        s_prev = s_cur
    return b"".join(parts)

def cfb_encrypt(key: bytes, plain_text: str) -> bytes:
    blocks = chunks(plain_text.encode("utf-8"), BLOCK_SIZE)
    IV: bytes = os.urandom(BLOCK_SIZE)
    y_prev = IV
    parts: list[bytes] = [IV]
    for block in blocks:
        y_prev = xor(aes_enc_block(key, y_prev), block)
        parts.append(y_prev)
    return b"".join(parts)

def ctr_encrypt(key: bytes, plain_text: str) -> bytes:
    blocks = chunks(plain_text.encode("utf-8"), BLOCK_SIZE)
    IV: bytes = os.urandom(BLOCK_SIZE)
    IV_int = int.from_bytes(IV, "big")
    parts: list[bytes] = [IV]
    for i, block in enumerate(blocks):
        IV_cur: bytes = ((IV_int + i) % (1 << 128)).to_bytes(16, "big")
        parts.append(xor(aes_enc_block(key, IV_cur), block))
    return b"".join(parts)

method_map = {
    "ECB": ecb_decrypt,
    "CBC": cbc_decrypt,
    "OFB": ofb_decrypt,
    "CFB": cfb_decrypt,
    "CTR": ctr_decrypt
}
if __name__ == "__main__":
    for line in lines:
        question_num, encryption_type, key_hex, message_hex = line.split()
        key:bytes = bytes.fromhex(key_hex)
        message: bytes = bytes.fromhex(message_hex)
        decrypted_message:str = method_map[encryption_type](key, message)
        print(f"Question {question_num}, plaintext is :     {decrypted_message}")

        