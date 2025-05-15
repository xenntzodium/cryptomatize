"""
BASIT ECC ŞİFRELEME DEMOSU
- ECC anahtar çifti üretimi
- ECDSA ile imzalama/doğrulama
- 3 çıktı formatı (binary/hex/base64)
"""

from ecdsa import SigningKey, NIST256p, SECP256k1, NIST384p
import base64

# OPSİYONEL PARAMETRELER ########################################
CURVE = SECP256k1  # secp256k1 NIST384p NIST256p
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

# ANAHTAR ÇİFTİ ÜRETİMİ ########################################
def generate_keys():
    private_key = SigningKey.generate(curve=CURVE)
    public_key = private_key.get_verifying_key()
    return private_key, public_key
#################################################################

# İMZALAMA İŞLEMLERİ ###########################################
def sign(data: bytes, private_key: SigningKey) -> bytes:
    return private_key.sign(data)
#################################################################

# DOĞRULAMA İŞLEMLERİ ##########################################
def verify(signature: bytes, data: bytes, public_key) -> bool:
    try:
        return public_key.verify(signature, data)
    except:
        return False
#################################################################

# MAIN #########################################################
if __name__ == "__main__":
    # Anahtar çifti üret
    private_key, public_key = generate_keys()
    data = b"Bu metin ECC ile imzalanacak test verisidir."

    print(f"\nÇıktı Formatı: {OUTPUT_FORMAT.upper()}")
    print(f"Private Key: {format_output(private_key.to_string())}")
    print(f"Public Key: {format_output(public_key.to_string())}")

    # İmzalama
    signature = sign(data, private_key)
    print(f"\nİmza: {format_output(signature)}")

    # Doğrulama
    is_valid = verify(signature, data, public_key)
    print(f"Doğrulama Sonucu: {'Başarılı' if is_valid else 'Başarısız'}")

    # Hatalı doğrulama testi
    fake_data = b"Sahte veri"
    is_valid_fake = verify(signature, fake_data, public_key)
    print(f"Sahte Veri Doğrulama: {'Başarılı' if is_valid_fake else 'Başarısız'}")
