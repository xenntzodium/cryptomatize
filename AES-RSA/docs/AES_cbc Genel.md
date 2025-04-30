AES CBC modu kod yazım aşaması ;

Yazılacak dil seçimi nasıl yapıldı ;  
oturup düşündüm hangi dil ile yazsam diye bilgi birikimim ve el göz yatkılığım python olduğu için kodlama aşamasında python diline başvurdum. kodlamaya başlarken ilk önce öğrenmem gereken şey kodlayacağım şeyin ne olduğuydu hemen kısa öz bir araştırma ile AES VE CBC nin ne olduğuna baktım 

### **AES Ne İşe Yarar?**

AES, bir **şifreleme algoritmasıdır**.  
 Temel amacı:

**Bir bilgiyi (mesaj, dosya, veri) gizlemek.**  
 Yani, birisi bu bilgiyi ele geçirse bile **anahtarı bilmeden** okuyamasın diye\!

AES ile bir veriyi:

* **Şifreleriz (encrypt)**

* **Sonra aynı anahtarla geri açarız (decrypt)**

AES’in mantığı şudur:  
 **“Güvenli bir şekilde bilgi gizlemek ve sonra doğru anahtarla geri çözmek.”**

 **AES \= Simetrik Şifreleme** kullanır.  
 Bu demek ki:

**Şifrelerken** ve **Çözerken** aynı anahtar kullanılır.

**Örnek:**

Şifreleme anahtarın 12345 ise, çözmek için de yine 12345 gerekir. Anahtarın olmazsa, şifre çözülmez.

### **3\. AES Bloklarla Çalışır**

AES, verileri **blok blok** işler.  
 Her bir blok:

* **128 bit** yani **16 byte** büyüklüğündedir.

1 byte \= 8 bit olduğu için, 16 byte \= 128 bit ediyor.

Yani AES bir seferde **16 byte'lık** bir veri parçasını şifreler.

Eğer verin küçükse (mesela 5 byte), ya da çok büyükse (mesela 1000 byte):

* **Parçalanır** ve her parça 16 byte olacak şekilde işlenir.  
* Küçükse de **padding (doldurma)** eklenir.

### **4\. AES Anahtar Uzunlukları**

AES 3 farklı anahtar boyutuyla çalışabilir:

| Anahtar Uzunluğu | Güvenlik Düzeyi |
| ----- | ----- |
| 128 bit | Standart güvenlik |
| 192 bit | Orta seviye daha güçlü güvenlik |
| 256 bit | Çok yüksek güvenlik |

Anahtar büyüdükçe:

* Şifreyi çözmek çok daha zor olur (kaba kuvvet saldırılarına karşı güçlü).

* Ama şifreleme/çözme süresi biraz daha artar.

### **5\. AES Nasıl Çalışır? (İç Yapı)**

AES şifrelerken birkaç **adım** uygular:

* **Key Expansion:**  
   Anahtarı genişletir, çünkü her tur için farklı bir alt anahtar lazım.

* **Initial Round (Başlangıç Turu):**  
   Veriye bir ilk değişiklik yapar (AddRoundKey).

* **Main Rounds (Ana Turlar):**  
   Birçok tur boyunca aşağıdaki adımlar yapılır:

  1. **SubBytes:**  
      Verinin her baytı bir tablo (S-Box) yardımıyla değiştirilir.

  2. **ShiftRows:**  
      Veri satırları kaydırılır.

  3. **MixColumns:**  
      Sütunlar karıştırılır.

  4. **AddRoundKey:**  
      Şu anki tur anahtarı veriye eklenir.

* **Final Round (Son Tur):**  
   Karışım (MixColumns) yapılmadan sadece diğer adımlar tekrarlanır.

Bu adımlar sonucunda veri **karmaşık bir şekilde şifrelenir** ve şifre çözülmesi imkansız hale gelir (anahtar olmadan).

;

CBC Modunda AES Şifreleme  
**CBC (Cipher Block Chaining)**, blok şifreleme algoritmalarının (örneğin AES) nasıl çalışacağını belirleyen bir çalışma modudur.

Temel olarak şu şekilde işler;  
128,192 veya 256 bit anahtar kullanır.  
her bir blok şifrelenmeden önce bir önceki blok ile XOR işlemi yapılır.  
her defasında ilk blok için bir IV(Initialization vector) yani rastgele bir başlangıç vektörü belirler.  
 yani cbc özetle bundan ibaretmiş.

 sonrasında kod yazımına başlarken kullanmam gereken kütüphaneleri araştırdım aslında bunu direk yapay zekaya yaptıracaktım fakat dedimki önce bir githubdan bakayımhazır örnekler nasıl yapılmış ordan da zaten kütüphaneleri çeker yazarım. githubda araştırma yaparken bu konuda harbi profesyönel admaların bazıları kütüphane kullanmaya ihtiyaç bile duymamış adamlar fonksiyonun içerisine direkt işlem yazmışlar tabi ben o kdar usta değilim logaritma türev az çok biliyorum fakat ileri düzey lineer cebir felan yok her neyse daha basit yazılmış projeler buldum ve kalıp olarak bir projeden kütüphaneleri ve bağzı kodları aldım ilk başta yazmış olduğum kodda kullanılan kütüphaneler şu şekilde ;

### **1\. os Kütüphanesi**

* **İşlevi:** `os` modülü, işletim sistemi ile etkileşime geçmek için kullanılan bir Python kütüphanesidir. Dosya ve dizin işlemleri, çevresel değişkenlere erişim gibi birçok işlevi sağlar.

* **Kullanımı:** Bu modül genellikle rastgele veri üretme (`os.urandom()`) veya dosya/dizin işlemleri için kullanılır. Örneğin, rastgele IV (Initialization Vector) oluşturmak için `os.urandom()` fonksiyonu kullanılabilir.

### **2\. cryptography.hazmat.primitives.padding Modülü**

* **İşlevi:** Bu modül, şifreleme algoritmalarında kullanılan **dolgu (padding)** işlemleri için gereklidir. Blok şifreleme algoritmalarında, verilerin blok uzunluklarına uyacak şekilde verilere ekstra veriler eklemek gerekir. Dolgu, genellikle son bloğun boyutunu tamamlamak için kullanılır.

* **Kullanımı:** `padding` modülü, şifreleme sırasında son bloğu dolgu verileri ile tamamlamak için kullanılır. Örneğin, `PKCS7` gibi dolgu yöntemleriyle, verinin şifreleme için uygun blok boyutuna getirilmesi sağlanır.

### **3\. cryptography.hazmat.primitives.ciphers Modülü**

* **İşlevi:** Bu modül, **şifreleme algoritmalarını** ve **şifreleme modlarını** kullanmak için temel araçları sağlar. Şifreleme algoritmalarını ve modlarını kullanarak veri şifrelemesi ve şifre çözme işlemleri gerçekleştirilir.

* **Kullanımı:**

  * `Cipher`: Şifreleme işlemleri için bir nesne oluşturmak amacıyla kullanılır.

  * `algorithms`: Şifreleme algoritmalarını tanımlar, örneğin AES, DES gibi.

  * `modes`: Şifreleme modlarını tanımlar, örneğin CBC (Cipher Block Chaining), ECB (Electronic Codebook) gibi.

 Kütüphane seçimi tamamlandıktan sonra kod yazma aşamasına geçtim ilk başta yazmış olduğum demo kod şu şekilde ;

import os  
from cryptography.hazmat.primitives import padding  
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def aes\_cbc\_mode():  
   \# Gizli tutulacak mesaj (plaintext)  
   plaintext \= b'Omu siber'  
   print(f"Orijinal mesaj: {plaintext}")

   \# 256-bit anahtar (32 byte) ve 128-bit IV (16 byte) rastgele oluşturuluyor  
   key \= os.urandom(32)  
   iv \= os.urandom(16)  \# CBC modu için gerekli

   \# AES-CBC algoritması tanımlanıyor  
   cipher \= Cipher(algorithms.AES(key), modes.CBC(iv))

   \# Padding uygulanıyor  
   padder \= padding.PKCS7(128).padder()  
   padded\_data \= padder.update(plaintext) \+ padder.finalize()

   \# Şifreleme işlemi  
   encryptor \= cipher.encryptor()  
   ciphertext \= encryptor.update(padded\_data) \+ encryptor.finalize()  
   print(f"Şifrelenmiş mesaj (CBC): {ciphertext}")

   \# Deşifreleme işlemi  
   decryptor \= cipher.decryptor()  
   decrypted\_padded \= decryptor.update(ciphertext) \+ decryptor.finalize()

   \# Padding kaldırılıyor  
   unpadder \= padding.PKCS7(128).unpadder()  
   decrypted\_data \= unpadder.update(decrypted\_padded) \+ unpadder.finalize()  
   print(f"Çözülmüş mesaj (CBC): {decrypted\_data}")

if \_\_name\_\_ \== "\_\_main\_\_":  
   aes\_cbc\_mode()

Yukarıda yazılan kodda aslında yapılan işlem çok basit default olarak girmiş olduğumuz omu siber textini aes cbc moduna çevirim şifreliyor fakat burda eksik olan birşeyler vardı tekrar decode ederken bizden hiçbir şekilde key istemiyordu peki nasıl çeviriyordu bu kod texti eski formata şu şekilde anlatayım ;

* `key = os.urandom(32)` ve `iv = os.urandom(16)` ile rastgele bir anahtar ve IV oluşturuluyor.

* Bu `key` ve `iv` bellekte (RAM’de) bir değişken olarak **hafızada saklı**.

* Şifreleme ve çözme işlemleri **aynı kod bloğu içinde** yapıldığı için `key` ve `iv` değişkenleri hâlâ orada duruyor.

Yani kısaca:

Şifreledikten hemen sonra **aynı anahtar ve IV** ile **hafızadan** alıp deşifre ediyoruz. 

başta nasıl olduğunu bende anlamamıştım sonrasında nasıl yaptığını chat gpt ye sorarak öğrendim. 

şimdi bırde bir sorunla karşılaştım aslında sorun değildi kodu her defasında çalıştırdığımızda kodun çıktısı şu şekilde oluyordu 

**\\xa5U\\xea\\x95^\\x00\\xd9V0L|AjY)"\\x17o\\x12\\xf6\\x85\\x0fH\\xd4=\\\\\\xd4\\r\*-z\\xc3**  

başta bunu ben bir sorun olarak anladım sonrasında merak ederek bunun neden böyle çıktı verdiğini araştırdım;

aldığım çıktı, şifrelenmiş **binary (ikili)** veridir.  
 Şifreleme işleminden çıkan veri **okunabilir metin (plaintext)** değil, **ham baytlar (bytes)** olur.

Bu baytlar rastgele gibi görünür ve terminalde gösterildiğinde de `\x` ile başlayan **hexadecimal (onaltılık)** gösterimle karışık bir şekilde çıkar:  
 Mesela `\xa5` demek 165 sayısına denk gelen bir bayt.

Bu tamamen normaldir çünkü:

* AES CBC modunda şifreleme **plaintext**'i **ciphertext**'e çevirir.

* **Ciphertext**, insan tarafından okunabilir bir şey olmak zorunda değildir.

* Hatta **anlamsız ve rastgele görünmesi**, şifrelemenin başarılı olduğunun işaretidir.

yani aslında oldukça iyi ilerlemişim.  

Peki gelelim önemli olan kısımlarımızdan birisi olan anahtar kısmına anahtarı göremiyoruz demiştik dimi anahtar üretiliyor arkada ama biz göremiyorduk peki bunu nasıl düzelteceğiz yalnz bu da değil hexadecimal olarak aldığımız çıktıyı da düzeltmemiz gerekiyordu bunu yaparken yardım almam gerekiyordu o kadar derin bilmediğim için herşeyi yani bende insanım. her neyse sonra bende kendim birşey ekledim daha doğrusu değiştirdim normalde default olarak tanımlanıyordu şifrelenecek metin ben dedim ki neden bunu el ile girmiyorum sonra hemen kolları sıvadım önce input şeklinde şifrelenecek metni kullanıcıdan aldım.

Birde ekstra olarak buraya base64 kütüphanesinde ekledik. karmaşık çıktıyı düzenlemek için. ilk baştaki kod version 1.0 idi aşağıdaki kod ise version 1.2 ;

import os  
from cryptography.hazmat.primitives import padding  
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  
import base64  \# Anahtar ve IV'yi okunabilir şekilde göstermek için

def aes\_cbc\_mode():  
   \# Kullanıcıdan şifrelenecek mesaj alınır  
   plaintext\_input \= input("Lütfen şifrelemek istediğiniz mesajı girin: ")  
   plaintext \= plaintext\_input.encode()  \# String → Bytes dönüşümü  
   print(f"Orijinal mesaj: {plaintext}")

   \# 256-bit anahtar (32 byte) ve 128-bit IV (16 byte) rastgele oluşturuluyor  
   key \= os.urandom(32)  
   iv \= os.urandom(16)  \# CBC modu için gerekli

   \# Anahtar ve IV ekrana base64 ile gösteriliyor (daha okunaklı)  
   print(f"Anahtar (base64): {base64.b64encode(key).decode()}")  
   print(f"IV (base64): {base64.b64encode(iv).decode()}")

   \# AES-CBC algoritması tanımlanıyor  
   cipher \= Cipher(algorithms.AES(key), modes.CBC(iv))

   \# Padding uygulanıyor (AES blok boyutu: 128 bit \= 16 byte)  
   padder \= padding.PKCS7(128).padder()  
   padded\_data \= padder.update(plaintext) \+ padder.finalize()

   \# Şifreleme işlemi  
   encryptor \= cipher.encryptor()  
   ciphertext \= encryptor.update(padded\_data) \+ encryptor.finalize()  
   print(f"Şifrelenmiş mesaj (CBC \- base64): {base64.b64encode(ciphertext).decode()}")

   \# Deşifreleme işlemi  
   decryptor \= cipher.decryptor()  
   decrypted\_padded \= decryptor.update(ciphertext) \+ decryptor.finalize()

   \# Padding kaldırılıyor  
   unpadder \= padding.PKCS7(128).unpadder()  
   decrypted\_data \= unpadder.update(decrypted\_padded) \+ unpadder.finalize()  
   print(f"Çözülmüş mesaj (CBC): {decrypted\_data.decode()}")

if \_\_name\_\_ \== "\_\_main\_\_":  
   aes\_cbc\_mode()

Yapılan değişiklikleri kısaca şöyle özetleyeyim ;

1. kullanıcıdan metin aldık   
2. base64 kütüphanesini ekledik  
3. ekrana ıv ve key değerini yazdırdık  
4. yazdırırken karmaşayı da engellemek için base64 kütüphanesinden yardım alarak çıktıyı düzenledik kısaca olanlar bunlardı.

kendi yazmış olduğum detaylı açıklamayı da aşağıya bırkaıyorum ;

yukarıdaki kod bloğunda ;

key \= os.urandom(32)  
iv \= os.urandom(16)  
   
Bu kısımda biz rasgele ıv yi seçtirip işleme devam ediyoruz.

print(f"Anahtar (base64): {base64.b64encode(key).decode()}")  
   print(f"IV (base64): {base64.b64encode(iv).decode()}")  
   
Bu kısımda ise oluşturulan key değeri ve ıv değerini örnek olması için ekrana yazdıran kon bloğumuz bulunuyor.

Daha sonrasında CBC algoritmamızı tanımlayıp içerisine ıv mizi de tanımlıyoruz;  
cipher \= Cipher(algorithms.AES(key), modes.CBC(iv))

sonraki adımda ise padding işlemine geçiyoruz peki padding işlemi nedir;

AES gibi sabit blok şifreleme algoritmaları sabit boyutlu bloklar üzerinde çalışır. AES için bu blok boyutu 128 bit yani 16 byte tir.

fakat eğer bizim şifrelemek istediğimiz metin tam 16 byte ve katı değilse işte burada padding işlemi yani boşluk doldurma işlemi devreye girer. 

padder \= padding.PKCS7(128).padder()  
   padded\_data \= padder.update(plaintext) \+ padder.finalize()

 biz burada PKCS7 padding yöntemi ile eksik olan byte sayısı kadar veriyi sonun eklemesini sağladık.  
`padder.update()` → Veriye padding eklemeye başlar.  
`padder.finalize()` → Gerekli son padding'i de ekler ve veriyi tamamlar.

Şimdi ise verimizi şifrelemek için şifreleme işlemine geçiyoruz;  
encryptor \= cipher.encryptor()  
   ciphertext \= encryptor.update(padded\_data) \+ encryptor.finalize()  
   print(f"Şifrelenmiş mesaj (CBC):{base64.b64encode(ciphertext).decode()}")  
")

**encryptor \= cipher.encryptor()----** Burada öncelikle olıuşturulan cipher nesnesinden bir encryptor nesnesi oluşturuyoruz. ecryptor veriyi şifreleme işlemi yapacak olan nesnedir.

Sonrasında şifreleme işlemi yapılır veriler birleştirilip print ile yazdırılır.

En sonda da deşifreleme işlemleri yapılıp paddıng değerini kaldırıp orjinal metni tekrar görebilmemizi sağlayan bloklar bulunmaktadır.

VERSİOM 2.0

Biz daha önceki yazdığımız kodlarda tamamen metin şifreleme üzerine ilerledik. grup ile konuşurken dedikki neden dosya da şifrelemiyoruz. neyse okey dedik sıvadım kolları kod yazmaya version 1.2  üzerinden ilerledim bu sefer tkinter de kullanarak açılır bir pencere oluşturdum.

sonrasında anahtar oluşturmak  için bir anahtar oluştur butonu koydum ve her tıklandığında rastgele key üreten bir bölüm oldu bu anahtar ile hem dosyayı şifreledik hemde tekrar deşifreleme işlemi yaptık. 

ben bunları yaptıktan sonra eksta düzenlemeler için yapay zekalara başvurdum başta chat gpt kullandım fakat o istediğim düzeyde ve şekilde düzenleme yapmadı gpt   nin verdiği kod bloğunda şifrelenen metin .encrypt uznatılı şekilde şifreleniyordu tekrar çözerken çözülen txt doysayısını .decrypt şeklinde kaydediyordu fakat açılmıyordu. sonrasında aynı kod ile cursor a başvurdum cursor tek düzeltme ile eksikleri ve hataları düzelterek eksta eklemeler yapıp kodun son hal çıktısını hazırladı ve aşağıdaki ekran görüntüsünü aldık ;

![][image1]

en son düzenlenmiş kodda yapılan ekstra işlemler şunlardır;

def generate\_new\_key(*self*):

        key \= os.urandom(32)

        key\_base64 \= base64.b64encode(key).decode('utf-8')

        self.key\_var.set(key\_base64)

        self.log\_message("\[+\] Yeni anahtar oluşturuldu")

Yeni anahtar oluşturma fonksiyonu her butona tıklandığında yeni anahtara oluşturup bildirim veriyor bize.

 *\# Anahtar kontrolü*

      *if* not self.key\_var.get().strip():              *raise* ValueError("Lütfen bir anahtar girin veya oluşturun") 

key \= base64.b64decode(self.key\_var.get().encode('utf-8'))

            *if* len(key) \!= 32:

    *raise* ValueError("Geçersiz anahtar uzunluğu.32byte olmalı.")

burda ise anahtar kontrolü yapıp eğer eksik ve ya hatalı bir bölüm var ise ekrana error mesajı veren bloktur.

[image1]: <data:image/png;base64,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>