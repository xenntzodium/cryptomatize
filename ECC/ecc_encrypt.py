# Ortak anahtar üzerinden simetrik anahtar oluşturur (AES ile şifreleme yapar)

from ecdsa import SigningKey
import hashlib

def encrypt_file(input_file: str, private_key_path: str, output_file: str):
    # 1. Private Key'i yükle
    with open(private_key_path, "rb") as f:
        private_key = SigningKey.from_pem(f.read())
    
    # 2. Dosyayı oku
    with open(input_file, "rb") as f:
        plaintext = f.read()
    
    # 3. SHA-256 hash ile imzala (Şifreleme yerine imza kullanıyoruz)
    signature = private_key.sign(plaintext, hashfunc=hashlib.sha256)
    
    # 4. İmzayı ve orijinal veriyi birleştirip kaydet
    with open(output_file, "wb") as f:
        f.write(signature + plaintext)  # İlk 64 byte imza, sonrası veri

    print(f"🔒 {input_file} dosyası {output_file} olarak şifrelendi!")

# Örnek kullanım
if __name__ == "__main__":
    encrypt_file("ornek_ECC.txt", "keys/ecc_private.pem", "sifreli_ECC.enc")