# AES ile çözümleme yapar

from ecdsa import VerifyingKey, BadSignatureError
import hashlib

def decrypt_file(encrypted_file: str, public_key_path: str, output_file: str):
    # 1. Public Key'i yükle
    with open(public_key_path, "rb") as f:
        public_key = VerifyingKey.from_pem(f.read())
    
    # 2. Şifreli dosyayı oku
    with open(encrypted_file, "rb") as f:
        data = f.read()
    
    # 3. İmza (ilk 64 byte) ve veriyi ayır
    signature = data[:64]  # ECDSA imzası 64 byte uzunluğunda
    plaintext = data[64:]  # Geri kalanı orijinal veri
    
    # 4. İmzayı doğrula
    try:
        public_key.verify(signature, plaintext, hashfunc=hashlib.sha256)
        with open(output_file, "wb") as f:
            f.write(plaintext)
        print(f"🔓 {encrypted_file} dosyası doğrulandı ve {output_file} olarak kaydedildi!")
    except BadSignatureError:
        print("❌ İmza geçersiz! Dosya değiştirilmiş olabilir.")

# Örnek kullanım
if __name__ == "__main__":
    decrypt_file("sifreli_ECC.enc", "keys/ecc_public.pem", "cozulmus_ECC.txt")