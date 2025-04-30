# RSA Algoritmasının Sadeleştirilmiş Anlatımı (Kullanıcıdan mesaj alarak)

# 1. İki asal sayı seçelim
p = 61
q = 53

# 2. n ve phi(n) hesapla
n = p * q
phi = (p - 1) * (q - 1)

# 3. Açık anahtar e seç
e = 17

# 4. Gizli anahtar d hesapla
def modinv(a, m):
    for d in range(2, m):
        if (a * d) % m == 1:
            return d
    return None

d = modinv(e, phi)

print(f"Açık anahtar (e, n): ({e}, {n})")
print(f"Gizli anahtar (d, n): ({d}, {n})")

# 5. Kullanıcıdan mesaj al
text = input("Şifrelenecek mesajı girin: ")

# 6. Her karakteri şifrele
encrypted = []
for char in text:
    m = ord(char)  # karakteri sayıya çevir
    c = pow(m, e, n)
    encrypted.append(c)

print("Şifreli mesaj:", encrypted)

# 7. Şifreli mesajı çözmek için kullanıcıdan anahtar iste
# Bu kısmı değiştirelim, kullanıcı doğru d ve n'yi girecek

try:
    d_input = int(input("Çözmek için gizli anahtar d değerini girin: "))
    n_input = int(input("Çözmek için n değerini girin: "))
except ValueError:
    print("Geçersiz giriş! Sadece sayısal değer giriniz.")
    exit(1)

decrypted = ""
for c in encrypted:
    m = pow(c, d_input, n_input)
    decrypted += chr(m)

print("Çözülen mesaj:", decrypted)
