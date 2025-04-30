import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def aes_cbc_mode():
    # Adım 1: Şifrelenecek mesaj belirleniyor
    plaintext = b'Omu siber'
    print(f"Orijinal mesaj: {plaintext}")

    # Adım 2: Rastgele anahtar (32 byte) ve IV (16 byte) oluşturuluyor
    key = os.urandom(32)
    iv = os.urandom(16)

    # Adım 3: AES-CBC şifreleme algoritması hazırlanıyor
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))

    # Adım 4: Mesaja padding (doldurma) ekleniyor
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Adım 5: Şifreleme işlemi yapılıyor
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    print("Şifrelenmiş mesaj (CBC): {ciphertext}")

    # Adım 6: Şifre çözme işlemi başlatılıyor
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    # Adım 7: Çözülen veriden padding kaldırılıyor
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()
    print(f"Çözülmüş mesaj (CBC): {decrypted_data}")


# Adım 8: Fonksiyon çalıştırılıyor
if __name__ == "__main__":
    aes_cbc_mode()
