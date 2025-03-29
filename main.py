import undetected_chromedriver as uc  # Anti-bot tespit sistemlerini aşan gelişmiş Chrome sürücüsü
from selenium import webdriver             # Web tarayıcı otomasyonu için temel kütüphane
from selenium.webdriver.common.by import By  # HTML elementlerini seçmek için lokasyon stratejileri
from selenium.webdriver.support.ui import WebDriverWait  # Sayfadaki elementlerin yüklenmesini beklemek için
from selenium.webdriver.support import expected_conditions as EC  # Bekleme koşulları (element görünür, tıklanabilir, vb.)
from selenium.webdriver import ActionChains  # Karmaşık fare ve klavye eylemleri için (sürükle-bırak, hover, vb.)
from selenium.webdriver.common.keys import Keys  # Klavye tuşları simülasyonu için (Enter, Tab, vb.)
import requests  # HTTP istekleri göndermek için (Mail.tm API'sine bağlanmak için kullanılır)
import random  # Rastgele değerler oluşturmak için (isim, şifre, vb.)
import string  # Karakter setleri için (harfler, rakamlar, semboller)
import time  # Bekleme süreleri ve zaman işlemleri için
import os  # İşletim sistemi ile etkileşim için (dosya yolları, programı sonlandırma)
import json  # JSON verileri işlemek için (API yanıtları)
import base64  # Base64 kodlama/çözme işlemleri için
import signal  # Sinyal işleme (Ctrl+C yakalama)
import sys  # Sistem işlevleri ve program sonlandırma için

class CodeiumKayit:
    def __init__(self):
        """
        Sınıfın yapıcı metodu. Tarayıcı ayarlarını yapılandırır ve başlatır.
        - Ctrl+C sinyalini yakalar
        - undetected_chromedriver kullanarak Chrome'u başlatır
        - Pencere boyutunu ayarlar
        """
        # Ctrl+C sinyalini yakala (SIGINT işleyicisi)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Varsayılan Chrome versionunu kullan (otomatik tespit)
        version_main = None
        
        try:
            # undetected-chromedriver ile tarayıcıyı başlat
            # Bu modül anti-bot korumalara karşı daha etkilidir
            self.driver = uc.Chrome(
                version_main=version_main,  # Otomatik versiyon tespiti
                headless=False,  # Görünür modda çalıştır (headless=True botlar daha kolay tespit edilir)
                use_subprocess=True,  # Alt süreç kullanarak daha stabil çalışma sağlar
                browser_executable_path=None,  # Chrome'un yolunu otomatik tespit et
                suppress_welcome=True,  # Karşılama sayfasını gösterme
                options=None  # Özel seçenekler kullanma (varsayılan ayarları kullan)
            )
            
            # Pencere boyutunu ayarla (1280x800 - standart masaüstü boyutu)
            self.driver.set_window_size(1280, 800)
            
            print("Tarayıcı başarıyla başlatıldı!")
            
        except Exception as e:
            print(f"Tarayıcı başlatma hatası: {str(e)}")
            raise
            
    def signal_handler(self, sig, frame):
        """
        Ctrl+C (SIGINT) sinyalini yakalar ve programı temiz bir şekilde sonlandırır.
        
        Args:
            sig: Yakalanan sinyal
            frame: Geçerli çerçeve
        """
        print("\nProgram kullanıcı tarafından sonlandırıldı.")
        self.temizle()
        sys.exit(0)

    def random_isim_uret(self, min_uzunluk, max_uzunluk):
        """
        Belirlenen uzunluk aralığında rastgele isim oluşturur.
        
        Args:
            min_uzunluk: Minimum karakter sayısı
            max_uzunluk: Maksimum karakter sayısı
            
        Returns:
            str: Rastgele oluşturulmuş isim
        """
        uzunluk = random.randint(min_uzunluk, max_uzunluk)
        return ''.join(random.choice(string.ascii_letters) for _ in range(uzunluk))

    def sifre_olustur(self):
        """
        Güvenlik kurallarına uygun rastgele şifre oluşturur.
        - En az bir küçük harf içerir
        - En az bir büyük harf içerir
        - En az bir rakam içerir
        - En az bir özel karakter içerir
        - Toplam uzunluk 9-10 karakterdir
        
        Returns:
            str: Oluşturulan güvenli şifre
        """
        kucuk_harfler = string.ascii_lowercase
        buyuk_harfler = string.ascii_uppercase
        rakamlar = string.digits
        semboller = "!@#$%^&*"
        
        # Her kategoriden en az bir karakter seç (güvenlik kriterleri için)
        sifre = [
            random.choice(kucuk_harfler),  # En az 1 küçük harf
            random.choice(buyuk_harfler),  # En az 1 büyük harf
            random.choice(rakamlar),       # En az 1 rakam
            random.choice(semboller)       # En az 1 özel karakter
        ]
        
        # Kalan karakterleri rastgele seç (toplam 9-10 karakter olacak şekilde)
        uzunluk = random.randint(9, 10)
        kalan = random.choices(kucuk_harfler + buyuk_harfler + rakamlar + semboller, k=uzunluk-4)
        sifre.extend(kalan)
        
        # Karakterlerin sırasını karıştır (tahmin edilebilirliği azaltmak için)
        random.shuffle(sifre)
        return ''.join(sifre)

    def mailTM_hesap_olustur(self):
        """Mail.tm üzerinden geçici mail hesabı oluşturur"""
        try:
            # Rastgele kullanıcı adı oluştur
            username = self.random_isim_uret(8, 12).lower()
            password = "Test123456!"
            
            # Domain listesini al
            domains_response = requests.get("https://api.mail.tm/domains")
            if domains_response.status_code != 200:
                return None
            
            domain = domains_response.json()["hydra:member"][0]["domain"]
            email = f"{username}@{domain}"
            
            # Hesap oluştur
            account_data = {
                "address": email,
                "password": password
            }
            
            response = requests.post("https://api.mail.tm/accounts", json=account_data)
            if response.status_code != 201:
                return None
            
            # Giriş yap ve token al
            auth_data = {
                "address": email,
                "password": password
            }
            
            auth_response = requests.post("https://api.mail.tm/token", json=auth_data)
            if auth_response.status_code != 200:
                return None
                
            token = auth_response.json()["token"]
            return {"email": email, "token": token}
            
        except Exception as e:
            print(f"Mail.tm hesap oluşturma hatası: {str(e)}")
            return None

    def mailTM_kod_al(self, mail_hesabi):
        """
        Mail.tm üzerinden gelen doğrulama kodunu alır ve işler.
        
        Farklı e-posta formatlarındaki doğrulama kodlarını tespit eder:
        - "code: XXXXXX" formatı
        - "verification code is XXXXXX" formatı
        - "code is XXXXXX" formatı
        - Veya doğrudan 6 haneli bir kod
        
        Args:
            mail_hesabi: Mail.tm hesap bilgilerini içeren sözlük (email ve token)
            
        Returns:
            str: 6 haneli doğrulama kodu, kod bulunamazsa None
        """
        try:
            # Mail.tm API'sine giriş yap (JWT token ile kimlik doğrulama)
            headers = {
                "Authorization": f"Bearer {mail_hesabi['token']}"
            }
            
            # Mesaj kutusundaki mailleri al
            response = requests.get("https://api.mail.tm/messages", headers=headers)
            if response.status_code != 200:
                print(f"Mail kutusunu alma hatası: HTTP {response.status_code}")
                return None
            
            # İlk mesajı al (en son gelen mail)
            messages = response.json()["hydra:member"]
            if not messages:
                print("Mesaj kutusunda mail bulunamadı")
                return None
            
            message = messages[0]
            
            # Mesaj içeriğini detaylı olarak al
            message_id = message["id"]
            response = requests.get(f"https://api.mail.tm/messages/{message_id}", headers=headers)
            if response.status_code != 200:
                print(f"Mesaj içeriğini alma hatası: HTTP {response.status_code}")
                return None
            
            # Doğrulama kodunu farklı formatlardan çıkarmayı dene
            try:
                message_data = response.json()
                # Hem HTML hem de düz metin içeriğini kontrol et
                html_content = message_data.get("html", "")
                text_content = message_data.get("text", "")
                
                # Olası kod formatları
                kod = None
                
                # Farklı kod formatlarını deneyerek bulmaya çalış
                # "code: XXXXXX" formatı
                if "code: " in text_content:
                    kod = text_content.split("code: ")[1].split("\n")[0].strip()
                # "verification code is XXXXXX" formatı
                elif "verification code is " in text_content:
                    kod = text_content.split("verification code is ")[1].split("\n")[0].strip()
                # "code is XXXXXX" formatı
                elif "code is " in text_content:
                    kod = text_content.split("code is ")[1].split("\n")[0].strip()
                # Direkt 6 haneli kod arama (regex ile)
                elif not kod:
                    import re
                    # 6 haneli sayıyı bul (kelime sınırları ile)
                    matches = re.findall(r'\b\d{6}\b', text_content)
                    if matches:
                        kod = matches[0]
                
                # Boşlukları temizle
                if kod:
                    kod = kod.strip()
                
                # Kod 6 haneli mi kontrol et (doğrulama kodları genellikle 6 haneli olur)
                if kod and len(kod) == 6 and kod.isdigit():
                    return kod
                else:
                    print(f"Geçerli bir doğrulama kodu bulunamadı: {kod}")
                    return None
                    
            except Exception as e:
                print(f"Kod çıkarma hatası: {str(e)}")
                # Mesaj içeriğini yazdır (debug için ilk 200 karakter)
                print(f"Mesaj içeriği: {text_content[:200]}...")
                return None
            
        except Exception as e:
            print(f"Doğrulama kodu alma hatası: {str(e)}")
            return None

    def pencere_kontrol(self):
        """Tarayıcı penceresinin açık olup olmadığını kontrol eder"""
        try:
            # Mevcut pencere handle'ını al
            current_window = self.driver.current_window_handle
            return True
        except:
            return False

    def cloudflare_kontrol(self):
        """Cloudflare/Turnstile doğrulamasını işle"""
        try:
            print("\nCloudflare doğrulaması bekleniyor...")
            time.sleep(2)
            
            # Continue butonunu bul ve tıkla
            try:
                continue_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
                )
                
                continue_button.click()
                print("Continue butonuna tıklandı")
                return True
                
            except Exception as e:
                print(f"Continue butonu bulunamadı: {str(e)}")
                return False
            
        except Exception as e:
            print(f"Cloudflare işleme hatası: {str(e)}")
            return False

    def kayit_formu_doldur(self):
        """Codeium kayıt formunu doldurur"""
        try:
            print("Kayıt sayfası açılıyor...")
            # Codeium kayıt sayfasını aç
            self.driver.get("https://codeium.com/account/register")
            
            # Sayfanın yüklenmesini bekle (sabit bekleme yerine sayfa görünür olana kadar bekle)
            try:
                # İlk input elementinin görünür olmasını bekle
                WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.NAME, "firstName"))
                )
                print("Sayfa yüklendi, form doldurma başlıyor...")
            except Exception as e:
                print(f"Sayfa yüklenme hatası: {str(e)}")
                return False
            
            # Mail.tm hesabı oluştur
            print("Mail.tm hesabı oluşturuluyor...")
            mail_hesabi = self.mailTM_hesap_olustur()
            if not mail_hesabi:
                print("Mail.tm hesabı oluşturulamadı!")
                return False
            
            print(f"Oluşturulan mail: {mail_hesabi['email']}")
            time.sleep(0.5)
            
            # Form elemanlarını doldur
            print("İlk form dolduruluyor...")
            isim_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "firstName"))
            )
            soyisim_input = self.driver.find_element(By.NAME, "lastName")
            email_input = self.driver.find_element(By.NAME, "email")
            
            # Rastgele isim ve soyisim oluştur
            isim = self.random_isim_uret(6, 8)
            soyisim = self.random_isim_uret(4, 6)
            
            # Form elemanlarını doldur
            isim_input.send_keys(isim)
            time.sleep(0.1)
            soyisim_input.send_keys(soyisim)
            time.sleep(0.2)
            email_input.send_keys(mail_hesabi['email'])
            time.sleep(0.3)
            
            # Continue butonuna tıkla
            continue_button = self.driver.find_element(By.XPATH, "//button[text()='Continue']")
            continue_button.click()
            print("İlk form tamamlandı, devam ediliyor...")
            
            # Şifre sayfasını bekle (sabit bekleme yerine element görünür olana kadar bekle)
            print("Şifre sayfası bekleniyor...")
            
            sifre_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            sifre_tekrar_input = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.NAME, "confirmPassword"))
            )
            
            # Rastgele şifre oluştur ve doldur
            sifre = self.sifre_olustur()
            print(f"Oluşturulan şifre: {sifre}")
            
            # Şifre alanlarını doldur
            sifre_input.send_keys(sifre)
            time.sleep(0.1)
            sifre_tekrar_input.send_keys(sifre)
            time.sleep(0.2)
            
            # Continue butonuna tıkla
            continue_button = self.driver.find_element(By.XPATH, "//button[text()='Continue']")
            continue_button.click()
            print("Şifre formu tamamlandı, devam ediliyor...")
            
            # Cloudflare doğrulamasını işle (sabit bekleme yerine element görünür olana kadar bekle)
            # Cloudflare elementi görünür olana kadar kısa bir bekleme
            time.sleep(1)
            if not self.cloudflare_kontrol():
                print("Cloudflare doğrulaması başarısız!")
                return False
                
            # Mail.tm'den doğrulama kodunu al - burada kod girme ekranının görünür olmasını bekle
            print("\nDoğrulama kodu bekleniyor...")
            
            # Doğrulama kodunu girmek için input alanlarının yüklenmesini bekle
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
                )
            except:
                print("Doğrulama kodu ekranı yüklenemedi!")
                
            # Doğrulama kodunu al
            kod = None
            max_attempts = 10
            for attempt in range(max_attempts):
                print(f"Doğrulama kodu alınıyor... (Deneme {attempt+1}/{max_attempts})")
                time.sleep(5)  # Mailin gelmesi için bekle
                kod = self.mailTM_kod_al(mail_hesabi)
                if kod:
                    print(f"Doğrulama kodu alındı: {kod}")
                    break
                else:
                    print("Kod henüz gelmemiş, tekrar deneniyor...")
            
            if not kod:
                print("Doğrulama kodu alınamadı!")
                return False
            
            # Doğrulama kodunu gir
            if not self.dogrulama_kodu_gir(kod):
                print("Doğrulama kodu girilemedi!")
                return False
            
            # Hesap bilgilerini göster
            print("\nHesap Bilgileri:")
            print("-" * 30)
            print(f"Email: {mail_hesabi['email']}")
            print(f"Şifre: {sifre}")
            print("-" * 30)
            
            # Hesap bilgilerini TXT dosyasına kaydet (sadece email ve şifre)
            hesap_bilgileri = f"Email: {mail_hesabi['email']} | Şifre: {sifre}"
            
            # Tüm hesapları tek dosyaya kaydet
            dosya_adi = "codeium_hesaplar.txt"
            
            # Dosyaya ekle (append mode)
            try:
                with open(dosya_adi, "a", encoding="utf-8") as dosya:
                    dosya.write(hesap_bilgileri + "\n")
                print(f"\nHesap bilgileri başarıyla '{dosya_adi}' dosyasına eklendi.")
            except Exception as e:
                print(f"\nHesap bilgilerini kaydetme hatası: {str(e)}")
            
            print("\nİşlem başarıyla tamamlandı!")
            print("Çıkmak için Enter'a basın...")
            
            try:
                input()  # Kullanıcıdan Enter'a basmasını bekle
                print("Program sonlandırılıyor...")
            except KeyboardInterrupt:
                print("\nKullanıcı tarafından iptal edildi!")
            except Exception as e:
                print(f"\nBeklenmeyen hata: {str(e)}")
            
            # Program sonlandırma adımları
            self.temizle()
            # Programı tamamen sonlandır
            os._exit(0)  # sys.exit() yerine os._exit() kullanılıyor - bütün threadleri zorla kapatır
            
        except Exception as e:
            print(f"Kayıt formu doldurma hatası: {str(e)}")
            return False
        finally:
            try:
                self.temizle()
                os._exit(0)  # İşlem her koşulda sonlandırılsın
            except:
                os._exit(1)  # Temizleme başarısız olsa bile sonlandır

    def dogrulama_kodu_gir(self, kod):
        """
        6 haneli doğrulama kodunu web sayfasındaki giriş alanlarına doğal bir şekilde girer.
        
        İnsan davranışını taklit etmek için:
        - Her karakteri tek tek girer
        - İnsana benzer gecikmelerle yazar
        - Focus ve click olaylarını kullanır
        
        Args:
            kod: Girilecek 6 haneli doğrulama kodu
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            print("\nDoğrulama kodu giriliyor...")
            
            # Input alanlarını bul (doğrulama kodları genellikle 6 ayrı input alanına girilir)
            inputs = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']"))
            )
            
            # Doğru input sayısını kontrol et (6 adet olmalı - her rakam için bir alan)
            if len(inputs) != 6:
                print(f"Beklenen 6 input alanı, bulunan: {len(inputs)}")
                
                # İlk seçici başarısız olduysa, daha spesifik bir seçici dene
                inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[maxlength='1']")
                if len(inputs) != 6:
                    print(f"Alternatif seçici ile de bulunamadı. Bulunan: {len(inputs)}")
                    # Debugging için ekran görüntüsü al
                    self.driver.save_screenshot("verification_screen.png")
                    print("Ekran görüntüsü kaydedildi: verification_screen.png")
                    return False
            
            # Tek tek karakterleri doğal şekilde gir (insan davranışını taklit et)
            print("Kod karakterleri doğal şekilde giriliyor...")
            
            # İlk alana tıkla ve fokusla (kullanıcı ilk önce buraya tıklar)
            inputs[0].click()
            time.sleep(0.5)  # Fokuslamadan sonra kısa bir bekleme
            
            # Her bir karakteri doğal gecikmelerle gir (insan yazma hızını taklit et)
            for i, rakam in enumerate(str(kod)):
                # Mevcut alana odaklan ve tıkla (kullanıcı her alana tıklar)
                inputs[i].click()
                time.sleep(0.1)  # Tıklama ile yazma arasındaki insansı gecikme
                
                # Karakteri temizle ve gir
                inputs[i].clear()
                inputs[i].send_keys(rakam)
                
                # İnsansı bir bekleme (karakterler arası)
                time.sleep(0.1)
            
            # Son giriş alanına bir kez daha tıkla ve fokusla (kullanıcı son rakamı girdikten sonra)
            inputs[5].click()
            time.sleep(0.2)
            
            print("Doğrulama kodu doğal olarak girildi")
            time.sleep(0.3)  # Kodun işlenmesi için kısa bekleme
            
            # Create account butonuna tıkla
            try:
                # Önce 'Create account' yazılı butonu ara (daha spesifik seçici)
                try:
                    create_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Create account')]"))
                    )
                except:
                    # Eğer özel yazılı buton bulunamazsa, herhangi bir buton dene (genel seçici)
                    create_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
                    )
                
                # Buton etkin mi kontrol et (disabled olabilir)
                if not create_button.is_enabled():
                    print("Buton etkin değil, daha farklı bir yaklaşım deneniyor...")
                    
                    # Plan B: Klavye kullanarak tab ile ilerleyip enter basma yöntemi
                    # Bu yöntem bazı sitelerde daha iyi çalışır
                    # İlk input'a tıkla
                    inputs[0].click()
                    time.sleep(0.1)
                    
                    # Her bir rakamı tek tek gir ve TAB tuşuyla ilerle (klavye navigasyonu)
                    for i, rakam in enumerate(str(kod)):
                        if i > 0:  # İlk input hariç her input için tab'a bas
                            ActionChains(self.driver).send_keys(Keys.TAB).perform()
                            time.sleep(0.1)
                            
                        inputs[i].clear()
                        inputs[i].send_keys(rakam)
                        time.sleep(0.1)
                    
                    # Son giriş sonrası TAB ile butona git ve ENTER'a bas
                    time.sleep(0.5)
                    ActionChains(self.driver).send_keys(Keys.TAB).perform()  # Buton'a git
                    time.sleep(0.3)
                    ActionChains(self.driver).send_keys(Keys.ENTER).perform() # Butona bas
                    print("Enter tuşuna basıldı")
                    time.sleep(0.1)
                    
                    # Butonun tekrar etkinleşip etkinleşmediğini kontrol et
                    try:
                        create_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "button"))
                        )
                        if create_button.is_enabled():
                            create_button.click()
                            print("Buton şimdi etkin ve tıklandı")
                    except:
                        print("Buton kontrolü başarısız, ancak enter tuşuyla form gönderildi")
                else:
                    # Buton etkinse doğrudan tıkla
                    create_button.click()
                    print("Create account butonuna tıklandı")
                
                # İşlemin başarılı olup olmadığını kontrol et (hata mesajı var mı?)
                time.sleep(3)  # Sunucu yanıtı için bekle
                try:
                    # Hata mesajı var mı kontrol et
                    error_element = self.driver.find_element(By.CSS_SELECTOR, ".error-message")
                    if error_element.is_displayed():
                        print(f"Doğrulama hatası: {error_element.text}")
                        return False
                except:
                    # Hata elementi bulunamadı, büyük ihtimalle işlem başarılı
                    pass
                    
                return True
                
            except Exception as e:
                print(f"Create account butonu bulunamadı veya tıklanamadı: {str(e)}")
                return False
            
        except Exception as e:
            print(f"Doğrulama kodu girme hatası: {str(e)}")
            return False

    def temizle(self):
        """
        Tarayıcı verilerini temizler ve tarayıcıyı kapatır.
        Bu metod, programın temiz bir şekilde sonlanmasını sağlar.
        
        Temizlenen veriler:
        - localStorage (site verileri)
        - sessionStorage (oturum verileri)
        - Çerezler (cookies)
        - Tarayıcı oturumu
        """
        try:
            self.driver.execute_script("window.localStorage.clear();")  # Yerel depolama temizleme
            self.driver.execute_script("window.sessionStorage.clear();") # Oturum depolama temizleme
            self.driver.delete_all_cookies()  # Tüm çerezleri sil
            self.driver.quit()  # Tarayıcıyı tamamen kapat
        except Exception as e:
            print(f"Temizleme hatası: {str(e)}")

if __name__ == "__main__":
    try:
        # Ana program akışı
        bot = CodeiumKayit()
        if bot.kayit_formu_doldur():
            print("Kayıt formu başarıyla dolduruldu!")
        else:
            print("Kayıt formu doldurulurken hata oluştu!")
        
        # Programı zorla sonlandır (tüm threadleri kapat)
        bot.temizle()
        os._exit(0)  # Normal sys.exit() yerine os._exit() kullanılır çünkü daha güçlüdür
        
    except KeyboardInterrupt:
        # Ctrl+C ile program sonlandırıldığında
        print("\nProgram kullanıcı tarafından sonlandırıldı (Ctrl+C).")
        try:
            bot.temizle()
        except:
            pass
        os._exit(0)  # Programı zorla sonlandır
        
    except Exception as e:
        # Beklenmeyen bir hata oluştuğunda
        print(f"Beklenmeyen hata: {str(e)}")
        try:
            bot.temizle()
        except:
            pass
        os._exit(1)  # Hata kodu ile sonlandır (1 = hata)
