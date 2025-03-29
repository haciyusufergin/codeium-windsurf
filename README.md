# Codeium Otomatik Kayıt

Codeium hesaplarını otomatik oluşturmak için gelişmiş bir otomasyon aracı.

## 📋 Genel Bakış

Bu araç, Codeium platformuna otomatik kayıt sürecini yönetir. Geçici e-posta oluşturma, form doldurma ve doğrulama işlemlerini otomatize ederek, hızlı hesap oluşturma imkanı sunar.

## ✨ Temel Özellikler

- Otomatik form doldurma ve geçici e-posta entegrasyonu
- Doğrulama kodlarını otomatik algılama ve işleme
- İnsan davranışını simüle eden gelişmiş bot tespiti önleme
- Hesap bilgilerini tek dosyada depolama

## 🚀 Kurulum

### Gereksinimler

- Python 3.8+
- Chrome tarayıcısı

### Adımlar

```bash
# Repoyu klonla
git clone https://github.com/username/codeium-windsurf2.git
cd codeium-windsurf2

# Bağımlılıkları yükle
pip install -r requirements.txt
```

## 💻 Kullanım

```bash
python main.py
```

Başlatıldıktan sonra, program otomatik olarak:
1. Geçici e-posta oluşturur
2. Kayıt formunu doldurur
3. Doğrulama kodunu işler
4. Hesap bilgilerini kaydeder

## ⚙️ Özelleştirme

`main.py` dosyasında aşağıdaki parametreler özelleştirilebilir:

```python
# Şifre uzunluğunu değiştirme
uzunluk = random.randint(9, 10)  # 9-10

# Doğrulama kodu bekleme süresini ayarlama
max_attempts = 10  # Deneme sayısı
```

## 📄 Lisans

[MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

**Not**: Bu araç eğitim ve kişisel kullanım amaçlıdır. Lütfen Codeium kullanım koşullarına uygun şekilde kullanınız.
