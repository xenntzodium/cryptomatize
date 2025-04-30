# Adım 1: Gerekli kütüphaneler içe aktarılıyor
import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Adım 2: Şifreleme/Çözme işlemlerini yapacak GUI sınıfı oluşturuluyor
class AESCipherGUI:
    def __init__(self, root):
        # Adım 3: Pencere ayarları yapılıyor
        self.root = root
        self.root.title("AES CBC Dosya Şifreleyici")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Adım 4: Başlık ve ana arayüz elemanları ekleniyor
        label = tk.Label(root, text="AES CBC Modunda Dosya Şifreleme/Çözme", font=("Arial", 12, "bold"))
        label.pack(pady=10)

        # Adım 5: Anahtar yönetimi alanı oluşturuluyor
        key_frame = ttk.LabelFrame(root, text="Anahtar Yönetimi", padding=10)
        key_frame.pack(fill="x", padx=10, pady=5)

        # Adım 6: Anahtar girişi için Entry kutusu ekleniyor
        self.key_var = tk.StringVar()
        key_label = ttk.Label(key_frame, text="AES Anahtarı (Base64):")
        key_label.pack(anchor="w")
        self.key_entry = ttk.Entry(key_frame, textvariable=self.key_var, width=70)
        self.key_entry.pack(fill="x", pady=5)

        # Adım 7: Yeni anahtar oluştur butonu ekleniyor
        generate_key_btn = ttk.Button(key_frame, text="Yeni Anahtar Oluştur", command=self.generate_new_key)
        generate_key_btn.pack(pady=5)

        # Adım 8: Dosya şifreleme ve çözme butonları ekleniyor
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        btn_encrypt = ttk.Button(btn_frame, text="Dosya Şifrele", command=self.select_file_and_encrypt, width=30)
        btn_encrypt.pack(pady=5)

        btn_decrypt = ttk.Button(btn_frame, text="Şifreli Dosya Çöz", command=self.select_file_and_decrypt, width=30)
        btn_decrypt.pack(pady=5)

        # Adım 9: İşlem bilgilerini göstermek için text alanı ekleniyor
        self.info_text = scrolledtext.ScrolledText(root, width=70, height=15, wrap=tk.WORD)
        self.info_text.pack(pady=15, padx=10)

    # Adım 10: Yeni rastgele anahtar oluşturuluyor
    def generate_new_key(self):
        key = os.urandom(32)  # 32 byte = 256 bit
        key_base64 = base64.b64encode(key).decode('utf-8')
        self.key_var.set(key_base64)
        self.log_message("[+] Yeni anahtar oluşturuldu")

    # Adım 11: Bilgi mesajı text alanına yazılıyor
    def log_message(self, message):
        self.info_text.insert(tk.END, message + "\n")
        self.info_text.see(tk.END)

    # Adım 12: Dosya şifreleme işlemi tanımlanıyor
    def encrypt_file_cbc(self, file_path):
        try:
            # Anahtar doğrulama
            if not self.key_var.get().strip():
                raise ValueError("Lütfen bir anahtar girin veya oluşturun")

            key = base64.b64decode(self.key_var.get().encode('utf-8'))
            if len(key) != 32:
                raise ValueError("Geçersiz anahtar uzunluğu. 32 byte olmalı.")

            # Dosyayı oku
            if not os.path.exists(file_path):
                raise FileNotFoundError("Dosya bulunamadı")

            with open(file_path, 'rb') as f:
                file_data = f.read()

            # IV oluştur
            iv = os.urandom(16)

            # Şifreleme başlatılıyor
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            encryptor = cipher.encryptor()

            # Padding uygulanıyor
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(file_data) + padder.finalize()

            # Şifreleniyor
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            # IV + Şifreli veri birleştiriliyor
            final_data = iv + ciphertext

            # Şifreli dosya kaydetme yeri seçiliyor
            default_name = os.path.splitext(os.path.basename(file_path))[0] + ".encrypted"
            save_path = filedialog.asksaveasfilename(
                defaultextension=".encrypted",
                initialfile=default_name,
                title="Şifreli Dosyayı Kaydet",
                filetypes=[("Encrypted Files", "*.encrypted"), ("All Files", "*.*")]
            )

            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(final_data)
                return save_path
            return None

        except Exception as e:
            raise Exception(f"Şifreleme hatası: {str(e)}")

    # Adım 13: Dosya çözme işlemi tanımlanıyor
    def decrypt_file_cbc(self, file_path):
        try:
            # Anahtar doğrulama
            if not self.key_var.get().strip():
                raise ValueError("Lütfen geçerli anahtarı girin")

            key = base64.b64decode(self.key_var.get().encode('utf-8'))
            if len(key) != 32:
                raise ValueError("Geçersiz anahtar uzunluğu. 32 byte olmalı.")

            # Dosya oku
            if not os.path.exists(file_path):
                raise FileNotFoundError("Dosya bulunamadı")

            file_size = os.path.getsize(file_path)
            if file_size < 16:
                raise ValueError("Geçersiz şifreli dosya formatı")

            with open(file_path, 'rb') as f:
                file_data = f.read()

            # IV'yi ve şifreli veriyi ayır
            iv = file_data[:16]
            encrypted_data = file_data[16:]

            # Şifre çözme başlatılıyor
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            # Şifre çözülüyor
            try:
                padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

                # Padding kaldırılıyor
                unpadder = padding.PKCS7(128).unpadder()
                decrypted_data = unpadder.update(padded_data) + unpadder.finalize()
            except Exception:
                raise ValueError("Şifre çözme başarısız. Yanlış anahtar veya bozuk dosya.")

            # Çözülmüş dosya kaydediliyor
            default_name = os.path.splitext(os.path.basename(file_path))[0]
            if default_name.endswith('.encrypted'):
                default_name = default_name[:-10]

            save_path = filedialog.asksaveasfilename(
                title="Çözülmüş Dosyayı Kaydet",
                initialfile=default_name,
                filetypes=[("All Files", "*.*")]
            )

            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(decrypted_data)
                return save_path
            return None

        except Exception as e:
            raise Exception(f"Şifre çözme hatası: {str(e)}")

    # Adım 14: Şifrelenecek dosya seçilip şifreleme işlemi başlatılıyor
    def select_file_and_encrypt(self):
        file_path = filedialog.askopenfilename(title="Şifrelenecek Dosyayı Seç")
        if not file_path:
            return

        try:
            encrypted_file = self.encrypt_file_cbc(file_path)
            if encrypted_file:
                self.log_message(f"[+] Şifreleme Başarılı\nŞifreli Dosya: {encrypted_file}")
                messagebox.showinfo("Başarılı", "Dosya başarıyla şifrelendi!")
        except Exception as e:
            self.log_message(f"[!] Hata: {str(e)}")
            messagebox.showerror("Hata", str(e))

    # Adım 15: Şifreli dosya seçilip çözme işlemi başlatılıyor
    def select_file_and_decrypt(self):
        file_path = filedialog.askopenfilename(
            title="Çözülecek Şifreli Dosyayı Seç",
            filetypes=[("Encrypted Files", "*.encrypted"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            decrypted_file = self.decrypt_file_cbc(file_path)
            if decrypted_file:
                self.log_message(f"[+] Şifre Çözme Başarılı\nÇözülmüş Dosya: {decrypted_file}")
                messagebox.showinfo("Başarılı", "Dosya başarıyla çözüldü!")
        except Exception as e:
            self.log_message(f"[!] Hata: {str(e)}")
            messagebox.showerror("Hata", str(e))

# Adım 16: Program çalıştırılıyor
if __name__ == "__main__":
    root = tk.Tk()
    app = AESCipherGUI(root)
    root.mainloop()
