import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidgetItem, QAbstractItemView
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt



DB_PATH_BAHCE = "hayvanat_bahcesi.db"
DB_PATH_CALISAN = "hayvanat_calisan.db"
DB_PATH_VETERINER = "hayvanat_veteriner.db"


def create_db_and_tables():
   
    
   
    conn_bahce = None
    try:
        conn_bahce = sqlite3.connect(DB_PATH_BAHCE)
        cursor_bahce = conn_bahce.cursor()
        
       
        cursor_bahce.execute('''
            CREATE TABLE IF NOT EXISTS BeslenmeSaatleri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hayvan_turu TEXT NOT NULL,
                beslenme_saati TEXT NOT NULL,
                yem_turu TEXT,
                miktar REAL,
                notlar TEXT
            )
        ''')
        
        
        cursor_bahce.execute('''
            CREATE TABLE IF NOT EXISTS AlanBilgileri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alan_adi TEXT NOT NULL,
                yerlesim TEXT,
                kapasite INTEGER
            )
        ''')

    
        cursor_bahce.execute("SELECT COUNT(*) FROM BeslenmeSaatleri")
        if cursor_bahce.fetchone()[0] == 0:
            print("Beslenme Saatleri tablosuna test verileri ekleniyor...")
            test_data = [
                ("Aslan", "09:00", "Kırmızı Et", 5.0, "Yetişkin aslanlara özel"),
                ("Zebra", "10:30", "Ot ve Saman", 10.0, "Grup beslenmesi"),
                ("Fil", "11:00", "Meyve ve Sebze", 50.0, "Günde iki kez"),
                ("Maymun", "13:00", "Meyve ve Kuruyemiş", 2.0, "Çeşitli atıştırmalıklar"),
                ("Kaplumbağa", "14:00", "Yeşillik", 1.5, "Yavaş yiyen tür")
            ]
            cursor_bahce.executemany("INSERT INTO BeslenmeSaatleri (hayvan_turu, beslenme_saati, yem_turu, miktar, notlar) VALUES (?, ?, ?, ?, ?)", test_data)
            conn_bahce.commit()
            print("Test verileri başarıyla eklendi.")
        else:
            print("Beslenme Saatleri tablosunda veri mevcut.")

        conn_bahce.commit()
        print("Hayvanat Bahçesi veritabanı ve tabloları kontrol edildi/oluşturuldu.")
    except sqlite3.Error as e:
        print(f"Hayvanat Bahçesi DB oluşturma hatası: {e}")
    finally:
        if conn_bahce:
            conn_bahce.close()

    conn_calisan = None
    try:
        conn_calisan = sqlite3.connect(DB_PATH_CALISAN)
        cursor_calisan = conn_calisan.cursor()
        
        
        cursor_calisan.execute('''
            CREATE TABLE IF NOT EXISTS CALISANLAR (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT NOT NULL UNIQUE,
                sifre TEXT NOT NULL,
                ad_soyad TEXT,
                telefon TEXT,
                email TEXT
            )
        ''')
        
        
        cursor_calisan.execute("SELECT COUNT(*) FROM CALISANLAR WHERE kullanici_adi = 'admin'")
        if cursor_calisan.fetchone()[0] == 0:
            cursor_calisan.execute("INSERT INTO CALISANLAR (kullanici_adi, sifre, ad_soyad) VALUES (?, ?, ?)",
                                ("admin", "admin", "Yönetici"))
            print("Varsayılan 'admin' kullanıcısı eklendi.")
        else:
            print("Varsayılan 'admin' kullanıcısı mevcut.")

       
        cursor_calisan.execute('''
            CREATE TABLE IF NOT EXISTS HAYVANLAR (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                tur TEXT NOT NULL,
                yas INTEGER,
                cinsiyet TEXT,
                saglik_durumu TEXT,
                beslenme_saati TEXT,
                alan TEXT
            )
        ''')
        
        
        cursor_calisan.execute("SELECT COUNT(*) FROM HAYVANLAR")
        if cursor_calisan.fetchone()[0] == 0:
            print("HAYVANLAR tablosuna test verileri ekleniyor...")
            test_data_hayvanlar = [
                ("Leo", "Aslan", 7, "Erkek", "İyi", "09:00", "Büyük Kediler Alanı"),
                ("Zoe", "Zebra", 3, "Dişi", "İyi", "10:30", "Savana Alanı"),
                ("Jumbo", "Fil", 15, "Erkek", "Kontrolde", "11:00", "Filler Vadisi"),
                ("Coco", "Maymun", 5, "Dişi", "İyi", "13:00", "Maymun Adası")
            ]
            cursor_calisan.executemany("INSERT INTO HAYVANLAR (ad, tur, yas, cinsiyet, saglik_durumu, beslenme_saati, alan) VALUES (?, ?, ?, ?, ?, ?, ?)", test_data_hayvanlar)
            conn_calisan.commit()
            print("Hayvanlar için test verileri başarıyla eklendi.")
        else:
            print("HAYVANLAR tablosunda veri mevcut.")
        
        
        cursor_calisan.execute('''
            CREATE TABLE IF NOT EXISTS DİYET_LİSTESİ (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hayvan_turu TEXT NOT NULL,
                diyet_adi TEXT NOT NULL,
                icerik TEXT,
                kalori INTEGER
            )
        ''')
        
       
        cursor_calisan.execute("SELECT COUNT(*) FROM DİYET_LİSTESİ")
        if cursor_calisan.fetchone()[0] == 0:
            print("DİYET_LİSTESİ tablosuna test verileri ekleniyor...")
            test_data_diyet = [
                ("Aslan", "Et Diyeti", "Kırmızı et, tavuk", 3000),
                ("Zebra", "Otçul Diyet", "Saman, taze ot", 2500),
                ("Fil", "Dev Otçul", "Meyve, sebze, ağaç dalları", 10000)
            ]
            cursor_calisan.executemany("INSERT INTO DİYET_LİSTESİ (hayvan_turu, diyet_adi, icerik, kalori) VALUES (?, ?, ?, ?)", test_data_diyet)
            conn_calisan.commit()
            print("Diyet listesi için test verileri başarıyla eklendi.")
        else:
            print("DİYET_LİSTESİ tablosunda veri mevcut.")
        
        conn_calisan.commit()
        print("Çalışan veritabanı ve tabloları kontrol edildi/oluşturuldu.")
    except sqlite3.Error as e:
        print(f"Çalışan DB oluşturma hatası: {e}")
    finally:
        if conn_calisan:
            conn_calisan.close()

  
    conn_veteriner = None
    try:
        conn_veteriner = sqlite3.connect(DB_PATH_VETERINER)
        cursor_veteriner = conn_veteriner.cursor()
        
       
        cursor_veteriner.execute('''
            CREATE TABLE IF NOT EXISTS VETERINERLER (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad_soyad TEXT NOT NULL,
                telefon TEXT,
                email TEXT,
                uzmanlik_alani TEXT
            )
        ''')

       
        cursor_veteriner.execute("SELECT COUNT(*) FROM VETERINERLER")
        if cursor_veteriner.fetchone()[0] == 0:
            print("VETERINERLER tablosuna test verileri ekleniyor...")
            test_data_veteriner = [
                ("Dr. Ayşe Yılmaz", "5551112233", "ayse@vet.com", "Genel Veterinerlik"),
                ("Dr. Can Demir", "5554445566", "can@vet.com", "Ekzotik Hayvanlar"),
                ("Dr. Elif Kaya", "5557778899", "elif@vet.com", "Büyük Baş Hayvanlar")
            ]
            cursor_veteriner.executemany("INSERT INTO VETERINERLER (ad_soyad, telefon, email, uzmanlik_alani) VALUES (?, ?, ?, ?)", test_data_veteriner)
            conn_veteriner.commit()
            print("Veterinerler için test verileri başarıyla eklendi.")
        else:
            print("VETERINERLER tablosunda veri mevcut.")
        
        conn_veteriner.commit()
        print("Veteriner veritabanı ve tabloları kontrol edildi/oluşturuldu.")
    except sqlite3.Error as e:
        print(f"Veteriner DB oluşturma hatası: {e}")
    finally:
        if conn_veteriner:
            conn_veteriner.close()


class AnaEkran(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            loadUi("ana_ekran.ui", self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"ana_ekran.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Hayvanat Bahçesi Otomasyonu")
        
        try:
            self.btn_ziyaretci.clicked.connect(self.ac_ziyaretci_ekrani)
            self.btn_calisan_giris.clicked.connect(self.ac_calisan_giris_ekrani)
            self.btn_cikis_ana.clicked.connect(self.close)
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"ana_ekran.ui'de beklenen buton bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)

        
        if hasattr(self, 'background_label'): 
            self.set_background_image("arka_plan2.jpg", self.background_label) 
        else:
            print("Uyarı: ana_ekran.ui'de 'background_label' bulunamadı.")


    def set_background_image(self, image_path, label_widget):
      
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label_widget.setPixmap(pixmap.scaled(label_widget.size(), Qt.KeepAspectRatioByExpanding))
            label_widget.setScaledContents(True)
        else:
            print(f"Uyarı: {image_path} bulunamadı veya geçersiz.")

    def ac_ziyaretci_ekrani(self):
        
        self.ziyaretci_ekrani = ZiyaretciEkran(self) 
        self.ziyaretci_ekrani.show()
        self.hide()

    def ac_calisan_giris_ekrani(self):
       
        self.calisan_giris_ekrani = CalisanGirisEkran(self) 
        self.calisan_giris_ekrani.exec_() 
        self.show()


class ZiyaretciEkran(QMainWindow): 
    def __init__(self, parent=None):
        super().__init__()
        try:
            loadUi("ziyaretci_ekrani.ui", self) 
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"ziyaretci_ekrani.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Ziyaretçi Ana Sayfası")
        self.parent_window = parent

        try:
            self.btn_beslenme_saatleri.clicked.connect(self.ac_beslenme_saatleri_ekrani)
            self.btn_alan_haritasi.clicked.connect(self.ac_alan_haritasi_ekrani) 
            self.btn_geri_ziyaretci.clicked.connect(self.geri_ana_ekrana)
            self.btn_cikis_ziyaretci.clicked.connect(self.close)
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"ziyaretci_ekrani.ui'de beklenen buton bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)

       
        if hasattr(self, 'label_2'): 
            self.set_background_image("arka_plan2.jpg", self.label_2) 
        else:
            print("Uyarı: ziyaretci_ekrani.ui'de 'label_2' bulunamadı.")


    def set_background_image(self, image_path, label_widget):
     
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label_widget.setPixmap(pixmap.scaled(label_widget.size(), Qt.KeepAspectRatioByExpanding))
            label_widget.setScaledContents(True)
        else:
            print(f"Uyarı: {image_path} bulunamadı veya geçersiz.")


    def ac_beslenme_saatleri_ekrani(self):
     
        self.beslenme_saatleri_ekrani = BeslenmeSaatleriEkran(self, from_ziyaretci=True)
        self.beslenme_saatleri_ekrani.show()
        self.hide()

    def ac_alan_haritasi_ekrani(self):
       
        self.alan_haritasi_ekrani = AlanHaritasiEkran(self) 
        self.alan_haritasi_ekrani.show()
        self.hide()

    def geri_ana_ekrana(self):
      
        if self.parent_window:
            self.parent_window.show()
        self.close()

class AlanHaritasiEkran(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        try:
            loadUi("alan_haritasi_ekrani.ui", self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"alan_haritasi_ekrani.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)
        
        self.setWindowTitle("Hayvanat Bahçesi Haritası")
        self.parent_window = parent

        try:
            self.btn_geri_alan.clicked.connect(self.geri_ziyaretci_ekrana)
            self.btn_cikis_alan.clicked.connect(self.close)
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"alan_haritasi_ekrani.ui'de beklenen butonlar bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)


        if hasattr(self, 'harita_resim_label'):
            pass 
        else:
            print("Uyarı: alan_haritasi_ekrani.ui'de 'harita_resim_label' bulunamadı.")

    def set_background_image(self, image_path, label_widget):
       
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label_widget.setPixmap(pixmap.scaled(label_widget.size(), Qt.KeepAspectRatioByExpanding))
            label_widget.setScaledContents(True)
        else:
            print(f"Uyarı: {image_path} bulunamadı veya geçersiz.")


    def geri_ziyaretci_ekrana(self):
       
        if self.parent_window:
            self.parent_window.show()
        self.close()


class BeslenmeSaatleriEkran(QMainWindow):
    def __init__(self, parent=None, from_ziyaretci=False):
        super().__init__()
        try:
            loadUi("beslenme_saatleri_ekrani.ui", self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"beslenme_saatleri_ekrani.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Beslenme Saatleri")
        self.parent_window = parent
        self.from_ziyaretci = from_ziyaretci 

        try:
            self.btn_geri_beslenme.clicked.connect(self.geri_ekrana)
            self.btn_cikis_beslenme.clicked.connect(self.close)
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"beslenme_saatleri_ekrani.ui'de beklenen buton bulunamadı: {e}. Lütfen objectName'i kontrol edin.")
            sys.exit(1)

        
        if hasattr(self, 'label'): 
            self.set_background_image("arka_plan7.jpg", self.label)
        else:
            print("Uyarı: beslenme_saatleri_ekrani.ui'de 'label' bulunamadı.")
            
        self.load_beslenme_saatleri()

    def set_background_image(self, image_path, label_widget):
    
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label_widget.setPixmap(pixmap.scaled(label_widget.size(), Qt.KeepAspectRatioByExpanding))
            label_widget.setScaledContents(True)
        else:
            print(f"Uyarı: {image_path} bulunamadı veya geçersiz.")

    def load_beslenme_saatleri(self):
       
        conn = None 
        try:
            conn = sqlite3.connect(DB_PATH_BAHCE) 
            cursor = conn.cursor()
            cursor.execute("SELECT hayvan_turu, beslenme_saati, yem_turu, miktar, notlar FROM BeslenmeSaatleri")
            rows = cursor.fetchall()
            print(f"Beslenme Saatleri tablosundan çekilen veri sayısı: {len(rows)}") 
            print(f"Çekilen veriler (ilk 5): {rows[:5]}") 
            
            self.tbl_beslenme_saatleri.setRowCount(0) 
            self.tbl_beslenme_saatleri.setColumnCount(5)

            headers = ["Hayvan Türü", "Beslenme Saati", "Yem Türü", "Miktar (kg)", "Notlar"]
            self.tbl_beslenme_saatleri.setHorizontalHeaderLabels(headers)

            for row_idx, row_data in enumerate(rows):
                self.tbl_beslenme_saatleri.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    if col_idx < 5: 
                        self.tbl_beslenme_saatleri.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
            self.tbl_beslenme_saatleri.resizeColumnsToContents()
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"Beslenme Saatleri tablosu (tbl_beslenme_saatleri) bulunamadı: {e}. Lütfen objectName'i kontrol edin.")
            print(f"UI Eleman Hatası (Beslenme Saatleri Tablosu): {e}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Beslenme saatleri yüklenirken hata oluştu: {e}")
            print(f"Veritabanı hatası (Beslenme Saatleri): {e}")
        finally:
            if conn:
                conn.close()

    def geri_ekrana(self):
        
        if self.parent_window:
            self.parent_window.show()
        self.close()

class CalisanGirisEkran(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        try:
            loadUi("calisan_ekrani.ui", self) 
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"calisan_ekrani.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Çalışan Giriş Ekranı")
        self.parent_window = parent

        try:
            self.btn_giris_yap.clicked.connect(self.giris_yap)
            self.btn_geri_calisan_giris.clicked.connect(self.geri_ana_ekrana)
            self.btn_cikis_calisan_giris.clicked.connect(self.close)
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"calisan_ekrani.ui'de beklenen butonlar bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)

        
        self.background_label = None
        if hasattr(self, 'label'): 
            self.background_label = self.label
        elif hasattr(self, 'label_2'): 
            self.background_label = self.label_2
        
        if self.background_label:
            self.set_background_image("arka_plan2.jpg", self.background_label)
        else:
            print("Uyarı: calisan_ekrani.ui'de arka plan QLabel'i ('label' veya 'label_2') bulunamadı.")


    def set_background_image(self, image_path, label_widget):
        
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label_widget.setPixmap(pixmap.scaled(label_widget.size(), Qt.KeepAspectRatioByExpanding))
            label_widget.setScaledContents(True)
        else:
            print(f"Uyarı: {image_path} bulunamadı veya geçersiz.")

    def giris_yap(self):
       
        kullanici_adi = self.txt_kullanici_adi.text()
        sifre = self.txt_sifre.text()

        conn = None
        try:
            conn = sqlite3.connect(DB_PATH_CALISAN)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM CALISANLAR WHERE kullanici_adi = ? AND sifre = ?", (kullanici_adi, sifre))
            calisan = cursor.fetchone()
            
            if calisan:
                QMessageBox.information(self, "Giriş Başarılı", "Hoş geldiniz, " + kullanici_adi + "!")
                self.calisan_menu_ekrani = CalisanMenuEkran(self)
                self.calisan_menu_ekrani.show()
                self.accept() 
            else:
                QMessageBox.warning(self, "Giriş Başarısız", "Kullanıcı adı veya şifre yanlış!")
                self.txt_sifre.clear()
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"Çalışan giriş ekranında (txt_kullanici_adi, txt_sifre) gibi beklenen giriş alanları bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            print(f"UI Eleman Hatası (Çalışan Giriş): {e}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Giriş yapılırken veritabanı hatası oluştu: {e}")
            print(f"Veritabanı hatası (Çalışan Giriş): {e}")
        finally:
            if conn:
                conn.close()

    def geri_ana_ekrana(self):
       
        if self.parent_window:
            self.parent_window.show()
        self.reject() 


class CalisanMenuEkran(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        try:
            loadUi("calisan_menu_ekrani.ui", self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"calisan_menu_ekrani.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Çalışan Menü Paneli")
        self.parent_window = parent

        try:
            self.btn_hayvan_bilgileri.clicked.connect(self.ac_hayvan_bilgileri_ekrani)
            self.btn_beslenme_saatleri.clicked.connect(self.ac_beslenme_saatleri_ekrani)
            self.btn_diyetler.clicked.connect(self.ac_diyetler_ekrani)
            self.btn_veteriner_bilgileri.clicked.connect(self.ac_veteriner_listesi_ekrani)
            self.btn_geri_menu.clicked.connect(self.geri_calisan_giris_ekrana)
            self.btn_cikis_calisan_menu.clicked.connect(self.close)
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"calisan_menu_ekrani.ui'de beklenen butonlar bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)

        
        if hasattr(self, 'label_2'): 
            self.set_background_image("arka_plan2.jpg", self.label_2)
        else:
            print("Uyarı: calisan_menu_ekrani.ui'de 'label_2' bulunamadı.")


    def set_background_image(self, image_path, label_widget):
       
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label_widget.setPixmap(pixmap.scaled(label_widget.size(), Qt.KeepAspectRatioByExpanding))
            label_widget.setScaledContents(True)
        else:
            print(f"Uyarı: {image_path} bulunamadı veya geçersiz.")

    def ac_hayvan_bilgileri_ekrani(self):
        
        self.hayvan_bilgileri_ekrani = HayvanBilgileriEkran(self)
        self.hayvan_bilgileri_ekrani.show()
        self.hide()

    def ac_beslenme_saatleri_ekrani(self):
    
        self.beslenme_saatleri_ekrani = BeslenmeSaatleriEkran(self, from_ziyaretci=False)
        self.beslenme_saatleri_ekrani.show()
        self.hide()

    def ac_diyetler_ekrani(self):
      
        self.diyetler_ekrani = DiyetlerEkran(self)
        self.diyetler_ekrani.show()
        self.hide()

    def ac_veteriner_listesi_ekrani(self):
        
        self.veteriner_listesi_ekrani = VeterinerListesiEkran(self)
        self.veteriner_listesi_ekrani.show()
        self.hide()

    def geri_calisan_giris_ekrana(self):
       
        if self.parent_window:
            self.parent_window.show()
        self.close()

class DiyetlerEkran(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        try:
            loadUi("diyetler_ekrani.ui", self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"diyetler_ekrani.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Diyet Listeleri")
        self.parent_window = parent

        try:
            self.btn_geri_diyetler.clicked.connect(self.geri_calisan_menu_ekrana)
            self.btn_cikis_diyetler.clicked.connect(self.close)
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"diyetler_ekrani.ui'de beklenen butonlar bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)

        
        if hasattr(self, 'label'): 
            self.set_background_image("arka_plan2.jpg", self.label)
        else:
            print("Uyarı: diyetler_ekrani.ui'de 'label' bulunamadı.")
            
        self.load_diyet_listeleri()

    def set_background_image(self, image_path, label_widget):
      
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label_widget.setPixmap(pixmap.scaled(label_widget.size(), Qt.KeepAspectRatioByExpanding))
            label_widget.setScaledContents(True)
        else:
            print(f"Uyarı: {image_path} bulunamadı veya geçersiz.")

    def load_diyet_listeleri(self):
        
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH_CALISAN)
            cursor = conn.cursor()
            cursor.execute("SELECT hayvan_turu, diyet_adi, icerik, kalori FROM DİYET_LİSTESİ")
            rows = cursor.fetchall()
            conn.close()

            self.tbl_diyetler.setRowCount(0)
            self.tbl_diyetler.setColumnCount(4)
            headers = ["Hayvan Türü", "Diyet Adı", "İçerik", "Kalori"]
            self.tbl_diyetler.setHorizontalHeaderLabels(headers)

            for row_idx, row_data in enumerate(rows):
                self.tbl_diyetler.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    self.tbl_diyetler.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
            self.tbl_diyetler.resizeColumnsToContents()
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"Diyetler tablosu (tbl_diyetler) bulunamadı: {e}. Lütfen objectName'i kontrol edin.")
            print(f"UI Eleman Hatası (Diyetler Tablosu): {e}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Diyet listeleri yüklenirken hata oluştu: {e}")
            print(f"Veritabanı hatası (Diyetler): {e}")
        finally:
            if conn:
                conn.close()


    def geri_calisan_menu_ekrana(self):
       
        if self.parent_window:
            self.parent_window.show()
        self.close()

class HayvanBilgileriEkran(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        try:
            loadUi("hayvan_bilgileri_ekrani.ui", self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"hayvan_bilgileri_ekrani.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Hayvan Bilgileri")
        self.parent_window = parent

        try:
            self.btn_geri_hayvan.clicked.connect(self.geri_calisan_menu_ekrana)
            self.btn_cikis_hayvan.clicked.connect(self.close)
            self.btn_hayvan_ekle.clicked.connect(self.ac_hayvan_ekle_dialog)
            self.btn_hayvan_duzenle.clicked.connect(self.ac_hayvan_duzenle_dialog) 

            
            self.tbl_hayvan_bilgileri.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.tbl_hayvan_bilgileri.setSelectionMode(QAbstractItemView.SingleSelection)

        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"hayvan_bilgileri_ekrani.ui'de beklenen butonlar bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)

        
        if hasattr(self, 'label'): 
            self.set_background_image("arka_plan2.jpg", self.label)
        else:
            print("Uyarı: hayvan_bilgileri_ekrani.ui'de 'label' bulunamadı.")
            
        self.load_hayvan_bilgileri()

    def set_background_image(self, image_path, label_widget):
       
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label_widget.setPixmap(pixmap.scaled(label_widget.size(), Qt.KeepAspectRatioByExpanding))
            label_widget.setScaledContents(True)
        else:
            print(f"Uyarı: {image_path} bulunamadı veya geçersiz.")

    def load_hayvan_bilgileri(self):
        
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH_CALISAN)
            cursor = conn.cursor()
            cursor.execute("SELECT id, ad, tur, yas, cinsiyet, saglik_durumu, beslenme_saati, alan FROM HAYVANLAR") 
            rows = cursor.fetchall()
            conn.close()

            self.tbl_hayvan_bilgileri.setRowCount(0)
            self.tbl_hayvan_bilgileri.setColumnCount(8) 
            headers = ["ID", "Adı", "Türü", "Yaş", "Cinsiyet", "Sağlık Durumu", "Beslenme Saati", "Alan"]
            self.tbl_hayvan_bilgileri.setHorizontalHeaderLabels(headers)

            for row_idx, row_data in enumerate(rows):
                self.tbl_hayvan_bilgileri.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    self.tbl_hayvan_bilgileri.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
            self.tbl_hayvan_bilgileri.resizeColumnsToContents()
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"Hayvan Bilgileri tablosu (tbl_hayvan_bilgileri) bulunamadı: {e}. Lütfen objectName'i kontrol edin.")
            print(f"UI Eleman Hatası (Hayvan Bilgileri Tablosu): {e}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Hayvan bilgileri yüklenirken hata oluştu: {e}")
            print(f"Veritabanı hatası (Hayvan Bilgileri): {e}")
        finally:
            if conn:
                conn.close()

    def ac_hayvan_ekle_dialog(self):
      
        self.hayvan_ekle_dialog = HayvanEkleDialog(self)
        self.hayvan_ekle_dialog.exec_() 
        self.load_hayvan_bilgileri()  

    def ac_hayvan_duzenle_dialog(self):
     
        selected_items = self.tbl_hayvan_bilgileri.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir hayvan seçiniz.")
            return

        
        row = selected_items[0].row()
        hayvan_id = int(self.tbl_hayvan_bilgileri.item(row, 0).text())

        self.hayvan_duzenle_dialog = HayvanDuzenleDialog(hayvan_id, self)
        self.hayvan_duzenle_dialog.exec_()
        self.load_hayvan_bilgileri()


    def geri_calisan_menu_ekrana(self):
       
        if self.parent_window:
            self.parent_window.show()
        self.close()

class HayvanEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        try:
            loadUi("hayvan_ekle.ui", self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"hayvan_ekle.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Yeni Hayvan Ekle")
        self.parent_window = parent

        try:
            self.btn_kaydet.clicked.connect(self.kaydet_hayvan)
            self.btn_iptal.clicked.connect(self.reject) 
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"hayvan_ekle.ui'de beklenen butonlar bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)

    def kaydet_hayvan(self):
      
        ad = self.txt_ad.text()
        tur = self.txt_tur.text()
        yas = self.txt_yas.text()
        cinsiyet = self.txt_cinsiyet.text()
        saglik_durumu = self.txt_saglik_durumu.text()
        beslenme_saati = self.txt_beslenme_saati.text()
        alan = self.txt_alan.text()

        if not all([ad, tur, yas, cinsiyet, saglik_durumu, beslenme_saati, alan]):
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurunuz!")
            return

        try:
            yas = int(yas)
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Yaş alanı sayı olmalıdır!")
            return

        conn = None
        try:
            conn = sqlite3.connect(DB_PATH_CALISAN)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO HAYVANLAR (ad, tur, yas, cinsiyet, saglik_durumu, beslenme_saati, alan) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (ad, tur, yas, cinsiyet, saglik_durumu, beslenme_saati, alan))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Hayvan başarıyla eklendi.")
            self.accept()
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"Hayvan ekle formunda (txt_ad, txt_tur, vb.) gibi beklenen giriş alanları bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            print(f"UI Eleman Hatası (Hayvan Ekle): {e}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Hayvan eklenirken bir hata oluştu: {e}")
            print(f"Veritabanı hatası (Hayvan Ekle): {e}")
        finally:
            if conn:
                conn.close()


class HayvanDuzenleDialog(QDialog):
    def __init__(self, hayvan_id, parent=None):
        super().__init__()
        try:
            loadUi("hayvan_ekle.ui", self) 
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"hayvan_ekle.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Hayvan Bilgilerini Düzenle")
        self.parent_window = parent
        self.hayvan_id = hayvan_id
        
        try:
            self.btn_kaydet.clicked.connect(self.kaydet_hayvan_duzenle)
            self.btn_iptal.clicked.connect(self.reject)
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"hayvan_ekle.ui'de beklenen butonlar bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)

        self.load_hayvan_data() 

    def load_hayvan_data(self):
      
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH_CALISAN)
            cursor = conn.cursor()
            cursor.execute("SELECT ad, tur, yas, cinsiyet, saglik_durumu, beslenme_saati, alan FROM HAYVANLAR WHERE id = ?", (self.hayvan_id,))
            hayvan_data = cursor.fetchone()
            conn.close()

            if hayvan_data:
                self.txt_ad.setText(hayvan_data[0])
                self.txt_tur.setText(hayvan_data[1])
                self.txt_yas.setText(str(hayvan_data[2]))
                self.txt_cinsiyet.setText(hayvan_data[3])
                self.txt_saglik_durumu.setText(hayvan_data[4])
                self.txt_beslenme_saati.setText(hayvan_data[5])
                self.txt_alan.setText(hayvan_data[6])
            else:
                QMessageBox.warning(self, "Hata", "Seçilen hayvan bulunamadı.")
                self.reject()
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"Hayvan düzenle formunda (txt_ad, txt_tur, vb.) gibi beklenen giriş alanları bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            print(f"UI Eleman Hatası (Hayvan Düzenle Yükleme): {e}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Hayvan bilgileri yüklenirken hata oluştu: {e}")
            print(f"Veritabanı hatası (Hayvan Düzenle Yükleme): {e}")
        finally:
            if conn:
                conn.close()

    def kaydet_hayvan_duzenle(self):
        
        ad = self.txt_ad.text()
        tur = self.txt_tur.text()
        yas = self.txt_yas.text()
        cinsiyet = self.txt_cinsiyet.text()
        saglik_durumu = self.txt_saglik_durumu.text()
        beslenme_saati = self.txt_beslenme_saati.text()
        alan = self.txt_alan.text()

        if not all([ad, tur, yas, cinsiyet, saglik_durumu, beslenme_saati, alan]):
            QMessageBox.warning(self, "Uyarı", "Lütfen tüm alanları doldurunuz!")
            return

        try:
            yas = int(yas)
        except ValueError:
            QMessageBox.warning(self, "Uyarı", "Yaş alanı sayı olmalıdır!")
            return

        conn = None
        try:
            conn = sqlite3.connect(DB_PATH_CALISAN)
            cursor = conn.cursor()
            cursor.execute("UPDATE HAYVANLAR SET ad = ?, tur = ?, yas = ?, cinsiyet = ?, saglik_durumu = ?, beslenme_saati = ?, alan = ? WHERE id = ?",
                            (ad, tur, yas, cinsiyet, saglik_durumu, beslenme_saati, alan, self.hayvan_id))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Hayvan bilgileri başarıyla güncellendi.")
            self.accept() 
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"Hayvan düzenle formunda (txt_ad, txt_tur, vb.) gibi beklenen giriş alanları bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            print(f"UI Eleman Hatası (Hayvan Düzenle Kaydet): {e}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Hata", f"Hayvan bilgileri güncellenirken bir hata oluştu: {e}")
            print(f"Veritabanı hatası (Hayvan Düzenle Kaydet): {e}")
        finally:
            if conn:
                conn.close()


class VeterinerListesiEkran(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        try:
            loadUi("veteriner_listesi_ekrani.ui", self)
        except Exception as e:
            QMessageBox.critical(self, "UI Yükleme Hatası", f"veteriner_listesi_ekrani.ui yüklenirken bir hata oluştu: {e}")
            sys.exit(1)

        self.setWindowTitle("Veteriner Bilgileri")
        self.parent_window = parent

        try:
            self.btn_geri_veteriner.clicked.connect(self.geri_calisan_menu_ekrana)
            self.btn_cikis_veteriner.clicked.connect(self.close)
            if not hasattr(self, 'tbl_veterinerler'):
                raise AttributeError("tbl_veterinerler QTableWidget not found in veteriner_listesi_ekrani.ui")
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"veteriner_listesi_ekrani.ui'de beklenen butonlar veya tablo bulunamadı: {e}. Lütfen objectName'leri kontrol edin.")
            sys.exit(1)


        if hasattr(self, 'label_2'): 
            self.set_background_image("arka_plan2.jpg", self.label_2)
        else:
            print("Uyarı: veteriner_listesi_ekrani.ui'de 'label_2' bulunamadı.")
            
        self.load_veteriner_bilgileri()

    def set_background_image(self, image_path, label_widget):
        
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            label_widget.setPixmap(pixmap.scaled(label_widget.size(), Qt.KeepAspectRatioByExpanding))
            label_widget.setScaledContents(True)
        else:
            print(f"Uyarı: {image_path} bulunamadı veya geçersiz.")

    def load_veteriner_bilgileri(self):
       
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH_VETERINER)
            cursor = conn.cursor()
            cursor.execute("SELECT ad_soyad, telefon, email, uzmanlik_alani FROM VETERINERLER")
            rows = cursor.fetchall()
            conn.close()

            self.tbl_veterinerler.setRowCount(0)
            self.tbl_veterinerler.setColumnCount(4)
            headers = ["Adı Soyadı", "Telefon", "Email", "Uzmanlık Alanı"]
            self.tbl_veterinerler.setHorizontalHeaderLabels(headers)

            for row_idx, row_data in enumerate(rows):
                self.tbl_veterinerler.insertRow(row_idx)
                for col_idx, data in enumerate(row_data):
                    self.tbl_veterinerler.setItem(row_idx, col_idx, QTableWidgetItem(str(data)))
            self.tbl_veterinerler.resizeColumnsToContents()
        except AttributeError as e:
            QMessageBox.critical(self, "UI Eleman Hatası", f"Veterinerler tablosu (tbl_veterinerler) bulunamadı: {e}. Lütfen objectName'i kontrol edin.")
            print(f"UI Eleman Hatası (Veteriner Listesi Tablosu): {e}")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veteriner bilgileri yüklenirken hata oluştu: {e}")
            print(f"Veritabanı hatası (Veteriner Listesi): {e}")
        finally:
            if conn:
                conn.close()

    def geri_calisan_menu_ekrana(self):
        
        if self.parent_window:
            self.parent_window.show()
        self.close()


if __name__ == "__main__":
    create_db_and_tables() 
    app = QApplication(sys.argv)
    main_window = AnaEkran()
    main_window.show()
    sys.exit(app.exec_())