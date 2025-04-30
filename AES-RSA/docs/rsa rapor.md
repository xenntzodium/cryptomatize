## **RSA Şifreleme Algoritması** 

### 

RSA algoritması, açık anahtarlı (asimetrik) bir şifreleme yöntemidir. Bu algoritmada iki farklı anahtar kullanılır: biri **genel (public)**, diğeri **özel (private)** anahtardır. Genel anahtar şifreleme, özel anahtar ise çözme işlemi için kullanılır. Bu sistem özellikle güvenli veri iletimi için yaygın olarak kullanılır.

---

*\# RSA Algoritmasının Sadeleştirilmiş Anlatımı (Kullanıcıdan mesaj alarak)*

*\# 1\. İki asal sayı seçelim*  
p \= 61  
q \= 53

*\# 2\. n ve phi(n) hesapla*  
n \= p \* q  
phi \= (p \- 1) \* (q \- 1)

*\# 3\. Açık anahtar e seç*  
e \= 17

*\# 4\. Gizli anahtar d hesapla*  
def modinv(*a*, *m*):  
    *for* d *in* range(2, m):  
        *if* (a \* d) % m \== 1:  
            *return* d  
    *return* None

d \= modinv(e, phi)

print(f"Açık anahtar (e, n): ({e}, {n})")  
print(f"Gizli anahtar (d, n): ({d}, {n})")

*\# 5\. Kullanıcıdan mesaj al*  
text \= input("Şifrelenecek mesajı girin: ")

*\# 6\. Her karakteri şifrele*  
encrypted \= \[\]  
*for* char *in* text:  
    m \= ord(char)  *\# karakteri sayıya çevir*  
    c \= pow(m, e, n)  
    encrypted.append(c)

print("Şifreli mesaj:", encrypted)

*\# 7\. Şifreli mesajı çözmek için kullanıcıdan anahtar iste*  
*\# Bu kısmı değiştirelim, kullanıcı doğru d ve n'yi girecek*

*try*:  
    d\_input \= int(input("Çözmek için gizli anahtar d değerini girin: "))  
    n\_input \= int(input("Çözmek için n değerini girin: "))  
*except* ValueError:  
    print("Geçersiz giriş\! Sadece sayısal değer giriniz.")  
    exit(1)

decrypted \= ""  
*for* c *in* encrypted:  
    m \= pow(c, d\_input, n\_input)  
    decrypted \+= chr(m)

print("Çözülen mesaj:", decrypted)

##  **Kodun Yapısı ve Çalışma Mantığı**

### **1\. Asal Sayılar ve Anahtar Üretimi**

**p \= 11**  
**q \= 7**

* Algoritmanın temelinde iki adet asal sayı seçilir: burada **p \= 11** ve **q \= 7**. Bu sayılar **küçük** seçilmiştir, çünkü eğitim amaçlıdır. Gerçek hayatta bu sayılar **çok büyük** olur (1024 bit veya daha fazla).

**n \= p \* q**  
**phi\_n \= (p \- 1\) \* (q \- 1\)**

* **n**, hem genel hem de özel anahtarın bir parçası olur.

* **phi\_n**, Euler’in Totient fonksiyonudur. Bu fonksiyon, **n**'den küçük ve **n** ile **aralarında asal** olan sayıların sayısını verir.

* Burada:  
   `n = 61 * 53 = 3233`  
   `phi_n = (61 - 1) * (53 - 1) = 60 * 52 = 3120`

### **2\. Genel Anahtar (e)**

**e \= 17**

* `e`, açık anahtarın şifreleme bileşenidir.

* Şart: `e` ile `phi_n` **aralarında asal** olmalıdır.

* Yani: `gcd(e, phi_n) = 1` olmalı → 17 ve 3120 aralarında asal olduğu için uygundur.

#### 3\. Özel Anahtarın (d) Hesaplanması

* def modinv(*a*, *m*):  
*     *for* d *in* range(2, m):  
*         *if* (a \* d) % m \== 1:  
*             *return* d  
*     *return* None  
*   
* d \= modinv(e, phi)  
* **Her d değeri için, (a \* d) % m hesaplanır. Eğer sonuç 1'e eşitse, bu d modüler tersi sağlamaktadır ve fonksiyon d'yi döndürecektir.**

* `a` (yani `e`) ile `m` (yani `phi_n`) arasında modüler tersi hesaplanır Modüler ters **d**, **(a \* d) % m \== 1** olduğu için, modüler aritmetikte **a** ile **d**'yi birbirinin tersine çevirmiş oluruz. Bu özellik RSA algoritmasında gizli anahtar **d**'yi bulmak için kullanılır.  
    
* Örneğimizde `e = 17`, `phi_n = 3120` için sonuç `d = 53` olur çünkü:  
   1`7 * 53 = 901 → 901 % 60 = 1`

#### 4\. **Mesajın Şifrelenmesi**

**def modinv(*a*, *m*):**  
    ***for* d *in* range(2, m):**  
        ***if* (a \* d) % m \== 1:**  
            ***return* d**  
    ***return* None**

**d \= modinv(e, phi)**

* Her karakterin **ASCII değeri** (`ord(char)`) alınır.

* Bu değerin `e` kuvveti **mod n** alınarak şifreli hali bulunur:  
   `cipher = (ascii^e) % n`

* `pow()` fonksiyonu, Python’un **hızlı üs alma** yöntemidir.

Örneğin `o` harfi için:

* ASCII: 111

* Şifreli: (111^7) % 77 \= 72

##### 5\. **Mesajın Çözülmesi** 

***try*****:**  
    **d\_input \= int(input("Çözmek için gizli anahtar d değerini girin: "))**  
    **n\_input \= int(input("Çözmek için n değerini girin: "))**  
***except*** **ValueError:**  
    **print("Geçersiz giriş\! Sadece sayısal değer giriniz.")**  
    **exit(1)**

* burda öncelikle bizde özel anahtar değerini ister sonrasında da genel anahtar değerini girdikten sonra çözümleme işlemini yapar yanlış bir değer ve ya geçersiz bir değer aldığında ise direkt programı durduruyor.

`Bu satırda, her şifreli karakterin (şifre^d) % n işlemi yapılır. Bu işlem, RSA şifreleme algoritmasının çözme (decryption) aşamasıdır. Şifreli mesajın her karakteri, gizli anahtar (d) ile çözülür.`

**`chr(m)`**`: Bu işlem, sayısal değeri tekrar karakter haline getirir. Bu sayede, çözülmüş şifreli mesaj, orijinal metne dönüştürülür.`

* Ardından ASCII değeri tekrar karaktere çevrilir: `chr()`

Örnek Çıktı:  
**Genel Anahtar (Public Key): (7, 77\)**  
**Özel Anahtar (Private Key): (43, 77\)**  
**Şifrelenecek mesajı girin : omu**  
 **Şifreli Mesaj: \[72, 61, 34\]**  
**Çözülmüş Mesaj: omu**

## **Özetle RSA Adımları**

1. **Asal sayı seçimi:** p, q

2. **n \= p × q** ve **φ(n) \= (p-1)(q-1)**

3. **e seçimi:** φ(n) ile aralarında asal

4. **d hesaplama:** modüler ters (d × e ≡ 1 mod φ(n))

5. **Şifreleme:** (mesaj^e) mod n

6. **Çözme:** (şifre^d) mod n

