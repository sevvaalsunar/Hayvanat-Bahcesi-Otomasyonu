import sqlite3
import hashlib
import os

DB_PATH_BAHCE = 'hayvanat_bahcesi.db'
DB_PATH_CALISAN = 'hayvanat_calisan.db'

def hash_password(password):
    """Verilen şifreyi SHA256 kullanarak hashler."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_db_bahce_calisan():
    """Hayvanat Bahçesi (HAYVANLAR) ve Çalışan (CALISANLAR) veritabanlarını oluşturur."""
    print("Hayvanat bahçesi ve çalışan veritabanları oluşturuluyor (veya güncelleniyor)...")

    # Hayvanat Bahçesi DB işlemleri
    conn_bahce = None
    try:
        conn_bahce = sqlite3.connect(DB_PATH_BAHCE)
        cursor_bahce = conn_bahce.cursor()

        # HAYVANLAR tablosu oluşturma (BESLENME_SAATLERI'nden önce bu oluşturulmalı!)
        cursor_bahce.execute("""
            CREATE TABLE IF NOT EXISTS HAYVANLAR (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT NOT NULL,
                tur TEXT NOT NULL,
                yas INTEGER,
                cinsiyet TEXT,
                saglik_durumu TEXT,
                gelis_tarihi TEXT
            );
        """)
        conn_bahce.commit()
        print("HAYVANLAR tablosu oluşturuldu (veya zaten vardı).")

        # Örnek hayvan verileri ekleme (sadece tablo boşsa)
        cursor_bahce.execute("SELECT COUNT(*) FROM HAYVANLAR;")
        if cursor_bahce.fetchone()[0] == 0:
            print("Hayvanlara örnek veri ekleniyor...")
            hayvan_verileri = [
                ('Aslan', 'Memeli', 5, 'Erkek', 'Sağlıklı', '2020-01-15'),
                ('Zebra', 'Memeli', 3, 'Dişi', 'Sağlıklı', '2021-03-20'),
                ('Penguen', 'Kuş', 2, 'Erkek', 'Sağlıklı', '2022-07-01'),
                ('Fil', 'Memeli', 10, 'Dişi', 'Sağlıklı', '2019-11-10'),
                ('Maymun', 'Memeli', 4, 'Erkek', 'Tedavide', '2023-05-01'),
                ('Kaplan', 'Memeli', 6, 'Erkek', 'Sağlıklı', '2018-09-01'),
                ('Leylek', 'Kuş', 3, 'Dişi', 'Sağlıklı', '2022-04-10'),
                ('Goril', 'Memeli', 8, 'Erkek', 'Sağlıklı', '2017-06-25'),
                ('Timsah', 'Sürüngen', 7, 'Erkek', 'Sağlıklı', '2019-02-18')
            ]
            cursor_bahce.executemany("INSERT INTO HAYVANLAR (ad, tur, yas, cinsiyet, saglik_durumu, gelis_tarihi) VALUES (?, ?, ?, ?, ?, ?)", hayvan_verileri)
            conn_bahce.commit()
            print("Hayvanlara örnek veri eklendi.")
        else:
            print("HAYVANLAR tablosu dolu, yeni hayvanlar eklenmiyor.")

    except sqlite3.Error as e:
        print(f"Hayvanat Bahçesi DB oluşturulurken hata: {e}")
    finally:
        if conn_bahce:
            conn_bahce.close()

    # Çalışan DB işlemleri
    conn_calisan = None
    try:
        conn_calisan = sqlite3.connect(DB_PATH_CALISAN)
        cursor_calisan = conn_calisan.cursor()

        # CALISANLAR tablosu oluşturma
        cursor_calisan.execute("""
            CREATE TABLE IF NOT EXISTS CALISANLAR (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanici_adi TEXT UNIQUE NOT NULL,
                sifre_hash TEXT NOT NULL,
                rol TEXT NOT NULL -- 'yonetici', 'veteriner', 'bakici'
            );
        """)
        conn_calisan.commit()
        print("CALISANLAR tablosu oluşturuldu (veya zaten vardı).")

        # Örnek çalışan verileri ekleme (sadece tablo boşsa)
        cursor_calisan.execute("SELECT COUNT(*) FROM CALISANLAR;")
        if cursor_calisan.fetchone()[0] == 0:
            print("Çalışanlara örnek veri ekleniyor...")
            # admin / admin123
            admin_sifre_hash = hash_password("admin123")
            calisan_verileri = [
                ('admin', admin_sifre_hash, 'yonetici'),
                ('ali_bakici', hash_password("bakici123"), 'bakici'),
                ('ayse_veteriner', hash_password("vet123"), 'veteriner'),
                ('cem_bakici', hash_password("bakici456"), 'bakici')
            ]
            cursor_calisan.executemany("INSERT INTO CALISANLAR (kullanici_adi, sifre_hash, rol) VALUES (?, ?, ?)", calisan_verileri)
            conn_calisan.commit()
            print("Çalışanlara örnek veri eklendi.")
        else:
            print("CALISANLAR tablosu dolu, yeni çalışanlar eklenmiyor.")

    except sqlite3.Error as e:
        print(f"Çalışan DB oluşturulurken hata: {e}")
    finally:
        if conn_calisan:
            conn_calisan.close()
    print("Tüm gerekli veritabanları oluşturuldu veya güncellendi.")


def create_beslenme_saatleri_table():
    """BESLENME_SAATLERI tablosunu oluşturur."""
    print("BESLENME_SAATLERI tablosu kontrol ediliyor/oluşturuluyor...")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH_BAHCE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS BESLENME_SAATLERI (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hayvan_id INTEGER NOT NULL,
                saat TEXT NOT NULL,
                yem_turu TEXT NOT NULL,
                miktar_kg REAL,
                notlar TEXT,
                FOREIGN KEY (hayvan_id) REFERENCES HAYVANLAR(id) ON DELETE CASCADE
            );
        """)
        conn.commit()
        print("BESLENME_SAATLERI tablosu oluşturuldu (veya zaten vardı).")
    except sqlite3.Error as e:
        print(f"BESLENME_SAATLERI tablosu oluşturulurken hata: {e}")
    finally:
        if conn:
            conn.close()

def insert_beslenme_saatleri_data():
    """BESLENME_SAATLERI tablosuna örnek verileri ekler (sadece varsa eklemez)."""
    print("BESLENME_SAATLERI tablosuna örnek veri ekleniyor (varsa eklemez)...")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH_BAHCE)
        cursor = conn.cursor()

        # Hayvan id'lerini almak için HAYVANLAR tablosundan verileri çek
        cursor.execute("SELECT id, ad, tur FROM HAYVANLAR")
        hayvanlar = cursor.fetchall()
        hayvan_map = {h[1]: h[0] for h in hayvanlar} # Hayvan adını ID'ye eşle

        beslenme_verileri = []
        # Örnek verileri, hayvan id'lerini kullanarak oluştur
        # Sadece yeni ve benzersiz verileri ekle (INSERT OR IGNORE sayesinde)
        if 'Aslan' in hayvan_map:
            beslenme_verileri.append((hayvan_map['Aslan'], '09:00', 'Et', 5.0, 'Sabah beslenmesi'))
            beslenme_verileri.append((hayvan_map['Aslan'], '17:00', 'Et', 4.5, 'Akşam beslenmesi'))
        if 'Zebra' in hayvan_map:
            beslenme_verileri.append((hayvan_map['Zebra'], '10:00', 'Ot', 8.0, 'Günlük ot takviyesi'))
        if 'Penguen' in hayvan_map:
            beslenme_verileri.append((hayvan_map['Penguen'], '11:00', 'Balık', 0.5, 'Öğle balık öğünü'))
        if 'Fil' in hayvan_map:
            beslenme_verileri.append((hayvan_map['Fil'], '08:30', 'Meyve', 10.0, 'Vitamin takviyeli'))
        if 'Maymun' in hayvan_map:
            beslenme_verileri.append((hayvan_map['Maymun'], '12:00', 'Meyve/Sebze', 1.0, 'Çeşitli atıştırmalıklar'))
        if 'Kaplan' in hayvan_map:
            beslenme_verileri.append((hayvan_map['Kaplan'], '09:30', 'Kırmızı Et', 6.0, 'Yeni Kaplan beslenmesi'))
            beslenme_verileri.append((hayvan_map['Kaplan'], '18:00', 'Beyaz Et', 5.5, 'Akşam beslenmesi'))
        if 'Leylek' in hayvan_map:
            beslenme_verileri.append((hayvan_map['Leylek'], '14:00', 'Balık', 0.2, 'Öğleden sonra atıştırmalığı'))
        if 'Goril' in hayvan_map:
            beslenme_verileri.append((hayvan_map['Goril'], '10:30', 'Yaprak', 7.0, 'Lifli besinler'))
        if 'Timsah' in hayvan_map:
            beslenme_verileri.append((hayvan_map['Timsah'], '16:00', 'Et', 3.0, 'Haftada 2 kez'))

        for data in beslenme_verileri:
            # INSERT OR IGNORE, eğer aynı hayvan_id, saat ve yem_turu kombinasyonu varsa eklemeyi atlar
            cursor.execute("""
                INSERT OR IGNORE INTO BESLENME_SAATLERI (hayvan_id, saat, yem_turu, miktar_kg, notlar)
                VALUES (?, ?, ?, ?, ?)
            """, data)
        conn.commit()
        print("BESLENME_SAATLERI tablosuna örnek veri eklendi (varsa atlandı).")

    except sqlite3.Error as e:
        print(f"BESLENME_SAATLERI tablosuna veri eklenirken hata: {e}")
    finally:
        if conn:
            conn.close()