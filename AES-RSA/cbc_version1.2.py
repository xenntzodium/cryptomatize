import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64  # Anahtar ve IV'yi daha okunabilir göstermek için


def aes_cbc_mode():
    # Adım 1: Kullanıcıdan şifrelenecek mesaj alınıyor
    plaintext_input = input("Lütfen şifrelemek istediğiniz mesajı girin: ")
    plaintext = plaintext_input.encode()  # String → Bytes dönüşümü
    print(f"Orijinal mesaj: {plaintext}")

    # Adım 2: Rastgele anahtar (32 byte) ve IV (16 byte) oluşturuluyor
    key = os.urandom(32)
    iv = os.urandom(16)

    # Adım 3: Anahtar ve IV base64 formatında ekrana yazdırılıyor
    print(f"Anahtar (base64): {base64.b64encode(key).decode()}")
    print(f"IV (base64): {base64.b64encode(iv).decode()}")

    # Adım 4: AES-CBC şifreleme algoritması hazırlanıyor
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

    # Adım 5: Mesaja padding (doldurma) ekleniyor
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Adım 6: Şifreleme işlemi yapılıyor
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    print(f"Şifrelenmiş mesaj (CBC - base64): {base64.b64encode(ciphertext).decode()}")

    # Adım 7: Şifre çözme işlemi yapılıyor
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    # Adım 8: Padding kaldırılıyor ve orijinal veri elde ediliyor
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
    print(f"Çözülmüş mesaj (CBC): {decrypted_data.decode()}")


# Adım 9: Fonksiyon çalıştırılıyor
if __name__ == "__main__":
    aes_cbc_mode()
