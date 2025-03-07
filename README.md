# Yapay Zeka Sesli Ve Yazılı Konuşma Botu

![versiyon](https://img.shields.io/badge/versiyon-1.0.0-blue)
![python](https://img.shields.io/badge/python-3.8%2B-yellow)

## İçindekiler

- [Özellikler](#-özellikler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Konuşma Modları](#-konuşma-modları)
- [Özelleştirme](#-özelleştirme)
- [Sorun Giderme](#-sorun-giderme)
- [Gereksinimler](#-gereksinimler)

---

## Özellikler (Eklenecek)

---

## Kurulum

### Ön Gereksinimler
- Python 3.8 veya daha yeni bir sürüm
- Chrome tarayıcısı
- ChatGPT hesabı (ücretsiz veya ücretli)

### Adımlar (Eklenecek)

---

## Kullanım

### Temel İşlemler

- **Metin Girme:** Alt kısımdaki metin kutusuna mesajınızı yazın
- **Mesaj Gönderme:** Gönder butonuna tıklayın veya Enter tuşuna basın
- **Sesli Komut:** Mikrofon butonuna tıklayıp konuşmaya başlayın
- **Yeni Sohbet:** "Yeni Sohbet" butonuna tıklayarak sıfırdan başlayın

### İlk Kullanım

- İlk başlatmada, Selenium tarayıcısı açılacak
- ChatGPT hesabınıza manuel olarak giriş yapın
- Giriş yaptıktan sonra uygulama hazır duruma gelecek

---

## Konuşma Modları

### Günlük Mod
- **Özellik:** Normal, günlük konuşma dilinde yanıtlar
- **Kullanım:** Varsayılan moddur, özel aktivasyon gerektirmez
- **Örnek:** "Hava durumu nasıl olacak?"

### Edebi Mod
- **Özellik:** Sanatkarane ve edebi bir dille yanıtlar
- **Kullanım:** "Edebi" butonunu aktifleştirin
- **Örnek:** Şiirsel ve sanatlı cümlelerle zenginleştirilmiş yanıtlar

### Öğretici Mod
- **Özellik:** Adım adım, açıklayıcı ve didaktik yanıtlar
- **Kullanım:** "Öğretici" butonunu aktifleştirin
- **Örnek:** Kavramları detaylı açıklayan, öğretici tarzda yanıtlar

---

## Özelleştirme

### Arayüz Renkleri (Eklenecek)

### Bağlantı Ayarları
`ayarlar.json` dosyasında ChatGPT bağlantı bilgilerini düzenleyebilirsiniz:

Örnek:
```json
{
  "chatgpt_email": "email@ornek_ruhi.com",
  "chatgpt_password": "ruhi123", 
  "chrome_driver_path": "C:/WebDriver/bin/chromedriver.exe"
}
```

### Simgeler ve Görsel Öğeler (Eklenecek)
- `model` klasöründeki SVG ve PNG dosyalarını değiştirebilirsiniz
- Kendi 3B modelinizi `model/karakter.obj` olarak ekleyebilirsiniz

---

## Sorun Giderme (Şuanda kendş yaşadığım ve oluşabilecek hataları ekledim)

### PyQt6 DLL Hatası
**Belirti:** `ImportError: DLL load failed while importing QtCore`
**Çözüm:**
- Microsoft Visual C++ 2019 veya daha yeni sürüm yükleyin
- PyQt6'yı yeniden yükleyin: `pip install --force-reinstall pyqt6`

### SVG Dönüştürme Hataları
**Belirti:** Simgeler görünmüyor veya hatalı görünüyor
**Çözüm:**
(Eklenecek)

### Kamera/3B Model Sorunları
**Belirti:** Kamera görüntüsü gelmiyor veya model görünmüyor
**Çözüm:**
- OpenGL sürücülerinizi güncelleyin
- Kamera izinlerini kontrol edin
- Uygulama, bu bileşenler olmadan da çalışacaktır

### ChatGPT Bağlantı Sorunları
**Belirti:** ChatGPT yanıt vermiyor veya bağlantı kurulamıyor
**Çözüm:**
- Chrome tarayıcısının ve sürücüsünün güncel olduğundan emin olun
- İnternet bağlantınızı kontrol edin
- `ayarlar.json` dosyasındaki yolları doğru ayarladığınızdan emin olun

---

## Gereksinimler

### Temel Kütüphaneler
- PyQt6 6.6.1+
- Selenium
- SpeechRecognition
- pyttsx3

### Görüntü İşleme
- OpenCV
- NumPy
- PyOpenGL
- Trimesh

### Diğer Bağımlılıklar
- Markdown
- CairoSVG
- Pillow
- Re (Regex)

Tüm bağımlılıklar `requirements.txt` dosyasında listelenmiştir.

---

## Not

Bu uygulama, Selenium kullanarak ChatGPT web arayüzüne bağlanır ve API anahtarı gerektirmez. 3B model görüntüleme için OpenGL kullanılmaktadır. Modern ve şık arayüz tasarımı, konuşma modları ve özel formatlar sayesinde daha esnek ve kişiselleştirilmiş bir deneyim sunar. 
