"""
BASIT RSA ŞİFRELEME DEMOSU
- Public/Private key çifti üretimi
- Şifreleme/Deşifreleme işlemleri
- 3 çıktı formatı (binary/hex/base64)
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# OPSİYONEL PARAMETRELER ########################################
KEY_SIZE = 2048           # 1024, 2048 veya 4096 bit
OUTPUT_FORMAT = "base64"  # "binary", "hex" veya "base64" olabilir
#################################################################

# FORMAT DÖNÜŞTÜRME İŞLEMLERİ ##################################
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

# RSA ANAHTAR ÇİFTİ ÜRETİMİ ####################################
def generate_keys():
    key = RSA.generate(KEY_SIZE)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key
#################################################################

# ŞİFRELEME İŞLEMLERİ ##########################################
def encrypt(data: bytes, public_key: bytes) -> bytes:
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(data)
#################################################################

# DEŞİFRELEME İŞLEMLERİ ########################################
def decrypt(data: bytes, private_key: bytes) -> bytes:
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(data)
#################################################################

# MAIN #########################################################
if __name__ == "__main__":
    # Anahtar çifti üret
    private_key, public_key = generate_keys()
    data = b"Bu metin RSA ile sifrelenecek test verisidir."

    print(f"\nÇıktı Formatı: {OUTPUT_FORMAT.upper()}")
    print(f"Public Key:\n{public_key.decode()}")
    print(f"Private Key:\n{private_key.decode()}")

    # Şifreleme
    encrypted = encrypt(data, public_key)
    print(f"\nŞifreli Veri: {format_output(encrypted)}")

    # Deşifreleme
    decrypted = decrypt(encrypted, private_key)
    print(f"Çözülmüş Veri: {decrypted.decode()}")