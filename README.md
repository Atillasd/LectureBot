# OtoYoklama

Bu proje, DEU çevrimiçi portalinde (https://online.deu.edu.tr) canlı ders toplantılarına otomatik olarak katılmak için Selenium tabanlı bir otomasyon sunar.

## Özellikler

- .env dosyasındaki kullanıcı adı ve şifre ile giriş.
- Canlı ders sayfasına geçiş.
- Aktif olan ("Sonlandı" olmayan) ilk toplantıyı bulup "Katıl" butonuna tıklama.
- Hataları ekrana yazdırır, kapatmadan önce bekler.

## Güvenlik

- Şifre, kullanıcı adı gibi hassas bilgi `.env` dosyasında tutulur.
- `.env` dosyası `git` tarafından takip edilmez (`.gitignore` içinde).
- Repoya gerçek gizli bilgiler eklenmez.

## Kurulum

1. Python 3.11+ ve pip yüklü olsun.
2. Sanal ortam oluştur ve etkinleştir (opsiyonel ama önerilir):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Gerekli paketleri yükle:
   ```bash
   pip install selenium python-dotenv
   ```
4. `.env.sample` dosyasını kopyala ve `.env` yap:
   ```bash
   copy .env.sample .env
   ```
5. `.env` içine DEU_USERNAME, DEU_PASSWORD ve BRAVE_PATH değerlerini gir.

## Çalıştırma

```bash
python main.py
```

## Notlar

- Brave tarayıcısının yüklü bulunması ve ChromeDriver uyumlu olması gerekir.
- Sitede yapı değişirse element seçimleri veya sayfa yapısı değiştirilmeli.
- Kanuni ve etik izinlerinize uyun. Erişiminiz yoksa sistem kullanmayın.
