import os
import base64
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def aes_ecb_mode():
    # 1. Kullanıcıdan şifrelenecek mesaj alınır
    plaintext_input = input("Lütfen şifrelemek istediğiniz mesajı girin: ")  # Kullanıcıdan şifrelemek için mesaj alınır
    plaintext = plaintext_input.encode()  # String → Bytes dönüşümü
    print(f"Orijinal mesaj: {plaintext}")  # Mesajın bytes formatında yazdırılması

    # 2. 256-bit'lik (32 byte) rastgele simetrik anahtar oluşturuluyor
    key = os.urandom(32)  # AES şifrelemesi için rastgele bir anahtar (256-bit uzunluğunda) oluşturuluyor

    # 3. Anahtarın base64 formatında gösterimi
    key_base64 = base64.b64encode(key).decode('utf-8')  # Anahtar base64 formatına dönüştürülür (insan okunabilir hale gelir)
    print(f"Şifreleme Anahtarı (Base64): {key_base64}")  # Base64 formatında şifreleme anahtarını yazdırır

    # 4. AES-ECB algoritması tanımlanıyor
    cipher = Cipher(algorithms.AES(key), modes.ECB())  # AES algoritması ve ECB modu tanımlanır

    # 5. AES blok boyutu (128 bit = 16 byte) kadar padding gerekiyor
    padder = padding.PKCS7(128).padder()  # PKCS7 padding şeması kullanılır (128 bit için)
    padded_data = padder.update(plaintext) + padder.finalize()  # Veriye padding eklenir, son blok tamamlanır

    # 6. Şifreleme işlemi
    encryptor = cipher.encryptor()  # Şifreleme için bir encryptor nesnesi oluşturulur
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()  # Veriyi şifreler, şifreli veri elde edilir

    # 7. Şifreli mesajın base64 formatında gösterimi
    ciphertext_base64 = base64.b64encode(ciphertext).decode('utf-8')  # Şifreli veri base64 formatında kodlanır
    print(f"Şifrelenmiş mesaj (Base64): {ciphertext_base64}")  # Şifrelenmiş mesaj base64 formatında yazdırılır

    # 8. Deşifreleme işlemi
    decryptor = cipher.decryptor()  # Deşifreleme için bir decryptor nesnesi oluşturulur
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()  # Şifreli veriyi deşifre eder

    # 9. Padding kaldırılıyor
    unpadder = padding.PKCS7(128).unpadder()  # Padding kaldırma işlemi için unpadder nesnesi oluşturulur
    decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()  # Padding kaldırılır, orijinal veri elde edilir

    # 10. Çözülen mesajın yazdırılması
    print(f"Çözülmüş mesaj (ECB): {decrypted_data.decode()}")  # Deşifre edilmiş orijinal mesaj yazdırılır


if __name__ == "__main__":
    aes_ecb_mode()  # Program çalıştırıldığında aes_ecb_mode fonksiyonu çağrılır
