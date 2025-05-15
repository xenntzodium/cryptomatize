"""
BASIT AES ŞİFRELEME DEMOSU
- ECB/CBC modları
- 3 çıktı formatı (binary/hex/base64)
- Otomatik padding işlemi
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

# OPSİYONEL PARAMETRELER ########################################
KEY_LENGTH = 16              # 16(AES-128), 24(AES-192) veya 32(AES-256)
BLOCK_SIZE = 16              # AES blok boyutu (standart 16 byte)
IV_LENGTH = 16               # CBC için IV boyutu (BLOCK_SIZE ile aynı olmalı)
OUTPUT_FORMAT = "base64"     # "binary", "hex" veya "base64" olabilir
#################################################################

# FORMAT DÖNÜŞTÜRME İŞLENLERİ ##################################
def format_output(data: bytes) -> str | bytes:
    if OUTPUT_FORMAT == "binary":
        return data
    elif OUTPUT_FORMAT == "hex":
        return data.hex()
    elif OUTPUT_FORMAT == "base64":
        return base64.b64encode(data).decode()
    else:
        raise ValueError("Geçersiz format! 'binary', 'hex' veya 'base64' olmalı")
#################################################################

# ŞİFRELEME İŞLEMLERİ YAPILIYOR ECB ve CBC için ##################################
def encrypt(data: bytes, key: bytes, iv: bytes = None) -> bytes:
    padded_data = pad(data, BLOCK_SIZE)  # veriyi blok büyüklüğüne göre padding ile ayarlıyoruz
    
    if iv:
        cipher = AES.new(key, AES.MODE_CBC, iv)  # iv var ise
    else:
        cipher = AES.new(key, AES.MODE_ECB)  # iv yok ise, cipher nesnesi oluşturuluyor
    
    return cipher.encrypt(padded_data)  # şifrelenmiş veri
#################################################

# DECRYPT İŞLEMLERİ YAPILIYOR ECB ve CBC için ##################################
def decrypt(data: bytes, key: bytes, iv: bytes = None) -> bytes:
    """
    AES ile şifreli veriyi çözer. ECB veya CBC modunu seçebilirsiniz.

    :param data: Şifresi çözülmesi gereken veri (byte türünde).
    :param key: AES anahtarı (byte türünde).
    :param iv: (Opsiyonel) CBC modu için başlatma vektörü (IV).
    :return: Çözülmüş veri (byte türünde).
    """
    
    if iv:
        cipher = AES.new(key, AES.MODE_CBC, iv)  # iv var ise CBC modu kullanılır
    else:
        cipher = AES.new(key, AES.MODE_ECB)  # iv yok ise ECB modu kullanılır
    
    # Şifreli veriyi çöz ve padding'i kaldır
    decrypted_data = cipher.decrypt(data)
    return unpad(decrypted_data, BLOCK_SIZE)  # çözülmüş veri
###############################################################################

# MAİN #######################################################################
if __name__ == "__main__":
    key = get_random_bytes(KEY_LENGTH)
    iv = get_random_bytes(IV_LENGTH)
    data = b"Bu metin scriptin test metnidir. Sifrelenecek olan veri burada tutuluyor."

    print(f"\nÇıktı Formatı: {OUTPUT_FORMAT.upper()}")
    print(f"Anahtar: {format_output(key)}")
    print(f"IV: {format_output(iv)}")

    # ECB Test
    ecb_enc = encrypt(data, key)
    print(f"\nECB Şifreli: {format_output(ecb_enc)}")
    print(f"ECB Çözülmüş: {decrypt(ecb_enc, key).decode()}")

    # CBC Test
    cbc_enc = encrypt(data, key, iv)
    print(f"\nCBC Şifreli: {format_output(cbc_enc)}")
    print(f"CBC Çözülmüş: {decrypt(cbc_enc, key, iv).decode()}")
###############################################################################