# ROADMAP

- [x] Proje Dosya İskeleti ve sanal ortam oluşturuldu 
	- [x] aes-demo.py 
	- [x] rsa-demo.py
	- [x] ecc-demo.py
	- [x] requirements.txt yani gereksinimler dosyası oluşturuldu. Proje için gereken kütüphaneler sanal ortamda kuruldu ve requirements.txt içerisine yazıldı.
- [x] AES demo scripti yazılacak 
	- [x] Padding desteği -> ecb&cbc
	- [x] IV Desteği -> cbc modu için
	- [x] Ayarlanabilir parametreler eklendi
- [x] RSA demo scripti yazılacak
	- [x] PKCS1_OAEP -> Padding desteği
	- [x] Ayarlanabilir parametreler eklendi
	- [x] yapılacaklar: Anahtar çifti (pu&pr) -> Enc. -> deenc.
- [x] ECC demo scripti yazılacak 
    - [x] ECC anahtar çifti üretimi
    - [x] ECDSA ile imzalama/doğrulama
    - [x] 3 çıktı formatı (binary/hex/base64)



## Seviye: 1: Ortam oluşturulacakk

- AES,RSA ve ECC için ayrı ayrı python scriptleri oluşturacağız. 
- her script şifreleme ve deşifreleme işlemlerini terminalden etkileşimli çalıştırabilecek şekilde olacak

- Kütüphaneler:
	- AES/RSA için -> cryptography
	- ECC -> ecdsa

## Seviye 2: rsa-demo.py oluşturulacak

- AES simetrik şifreleme algoritması (Aynı anahtar şifreleme & şifre çzme)
- ECB modu güvensiz (sebep: aynı plaintext hep aynı ciphertext'i üretiyor)
- CBC modu daha güvenilir, fakat çok güvenilir anlamına gelmez bu. ECB modundan daha güvenilir olmasının sebebi rastgele IV kullanımı
- PyCryptodome kütüphanesi kullanacağız.


### ÖNEMLİ NOKTALAR

Anahtar Boyutu:
	- KEY_LENGTH = 16  # 16(AES-128), 24(AES-192), 32(AES-256)
		- Daha yüksek değerler daha güvenli ama yavaş
Mod Seçimi
	- ECB: Hızlı ama güvensiz (test amaçlı)
	- CBC: Güvenli (gerçek projelerde tercih edilebilirlik derecesinde güvenilirlik)
Padding
	- pad(data, BLOCK_SIZE)  # Veriyi 16 byte'ın katı yapar
		- Otomatik olarak PKCS7 padding uygular
IV (Initialization Vector):
	- CBC modunda her şifreleme için yeni IV üretilmeli
	- IV gizli olmak zorunda değil ama tekrar kullanılmamalı
Çıktı Formatları
	- Binary: Ham byte verisi
	- Hex: Okunabilir hex string
	- Base64: Web/JSON uyumlu

## Seviye 3: rsa-demo.py oluşturulacak

- RSA -> Asimetrik / public&private key
- Anahtar boyutu 1024, 2048 veya 4096 bit
- PKCS#1 OAEP padding öneriliyor. Güvenli bir padding yöntemi
- PyCryptodome kütüphanesini kullanacağız.

### Önemli Noktalar;

Anahtar Boyutu:
	- KEY_SIZE = 2048  # 1024 (zayıf), 2048 (standart), 4096 (güçlü)
Güvenli Padding
	- cipher = PKCS1_OAEP.new(key)  # Güvenli şifreleme için
Anahtar Yönetimi
	- Public Key
	- Private Key
Veri Boyutu Limiti
	- RSA ile şifrelenecek veri anahtar boyutundan küçük olmalı
		- Örneğin 2048-bit anahtar için maksimum 190 byte veri

## Seviye 4: ecc.py

- ECC (Elliptic Curve Cryptography) asimetrik şifreleme kullanır
- RSA'dan daha kısa anahtar boyutlarıyla yüksek güvenlik sağlar
- secp256k1 eğrisi (Bitcoin'de kullanılan) veya P-256 standart eğrisi
- Anahtar üretimi ve ECDSA imzalama için -> ecdsa kütüphanesi kullanılacaktır.

### Önemli Noktalar;

Eğri Seçimi:
	- CURVE = NIST256p  # NIST P-256 eğrisi (diğer seçenekler: SECP256k1, NIST384p)
Anahtar Boyutu:
	- 256-bit ECC ≈ 3072-bit RSA güvenliği 
	- Private key 32 byte, Public key 64 byte
imza boyutu: 
	- ECDSA imzası 64 byte






