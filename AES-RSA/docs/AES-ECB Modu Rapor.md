### **AES-ECB Modu – Rapor**

#### **Kullanılan Kütüphaneler**

1. **os**: Python'un yerleşik kütüphanesidir ve sistemle ilgili işlevleri sağlar. Bu örnekte `os.urandom()` fonksiyonu ile rastgele 32-byte bir anahtar (key) üretmek için kullanılmıştır.

2. **cryptography.hazmat.primitives.padding**: Bu modül, verileri AES algoritmasının blok boyutuna uyacak şekilde padlemek için kullanılır. Burada PKCS7 padding algoritması kullanılarak mesajın boyutunu 16 bayta (128 bit) tam olarak uydurmak için padding eklenmiştir.

3. **cryptography.hazmat.primitives.ciphers**: AES şifreleme ve şifre çözme işlemlerini yapmak için `Cipher` sınıfı burada kullanılmıştır.

4. **cryptography.hazmat.primitives.ciphers.algorithms.AES**: AES şifreleme algoritması burada 256-bit (32 byte) simetrik anahtarla kullanılmıştır.

5. **cryptography.hazmat.primitives.ciphers.modes.ECB**: ECB (Electronic Codebook) modu, her bir bloğun bağımsız olarak şifrelenmesini sağlayan AES modudur.

#### **Kodun Çalışma Prensibi**

* **AES ECB** modunda, her blok verisi bağımsız şekilde şifrelenir. Bu nedenle aynı veriler her seferinde aynı şekilde şifrelenir. Güvenlik açısından zayıf olabilir, çünkü veriler arasındaki desenler kaybolmaz.

* Kodda, ilk olarak şifrelemek üzere bizden metni ve ya sayıyı girmemizi ister.

* 256-bit'lik rastgele bir **anahtar** oluşturulur.

* **Padding** işlemi gerçekleştirilir. AES algoritması her zaman sabit blok boyutuna (128-bit) veriyi uyarlamak zorundadır. Bu yüzden veri boyutunun 128-bit'lik bloklara bölünebilmesi için padding uygulanır.

* Veriyi şifrelemek için **AES-ECB** algoritması kullanılır.

* Şifrelenen veriyi geri çözmek için **decryptor** kullanılır ve padding çıkarılır.

* Son olarak, şifrelenmiş verilerin doğru çözülüp çözülmediği `assert` ile kontrol edilir.

**fark edildiği üzere burada ıv değeri kullanmadık bunun sebebi;**

ECB, her bloğun şifrelenmesini bağımsız bir şekilde gerçekleştirdiğinden, şifreleme sırasında **önceki bloklardan etkilenmeyen** bir yapı oluşturur. Bu, modun basitliğini sağlar.

Ancak bu basitlik, güvenlik açısından ciddi zayıflıklara yol açabilir. Çünkü aynı girdi her zaman aynı çıktıyı üretir ve bu, şifreli verilerde belirgin desenler oluşmasına neden olabilir (örneğin, dosyada aynı verinin tekrar eden yerleri şifreli veride de aynı görünebilir).

Bu nedenle ECB, genellikle **güvensiz** olarak kabul edilir ve **CBC** gibi daha güvenli modlar tercih edilir.

#### **Açıklama**

Bu işlemde şifreleme ve şifre çözme işlemleri birbirinden bağımsız olarak çalıştığı için `ECB` modunun ne kadar zayıf olduğu üzerinde durulmalıdır. Aynı veriyi defalarca şifrelediğinizde aynı şifreli veriyi alırsınız. Bu da veri analistlerinin şifreli veriyi analiz ederken bazı düzenekleri fark etmelerini kolaylaştırır.

