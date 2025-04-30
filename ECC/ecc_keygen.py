# ECC public & private key üretimi

from ecdsa import SigningKey, NIST256p
import os

# 1. Anahtar çifti için dizin oluştur
os.makedirs("keys", exist_ok=True)

# 2. Private Key üret (NIST P-256 eğrisi kullanarak)
private_key = SigningKey.generate(curve=NIST256p)

# 3. Public Key'i private key'den türet
public_key = private_key.verifying_key

# 4. Anahtarları PEM formatında kaydet
with open("keys/ecc_private.pem", "wb") as f:
    f.write(private_key.to_pem())  # Private Key'i dosyaya yaz

with open("keys/ecc_public.pem", "wb") as f:
    f.write(public_key.to_pem())  # Public Key'i dosyaya yaz

print("🔑 Anahtarlar 'keys/' dizininde oluşturuldu!")