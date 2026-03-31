import sqlite3
import os

DB_PATH_VETERINER = 'hayvanat_veteriner.db'

def create_veteriner_db():
    """Veteriner veritabanını ve VETERINERLER tablosunu oluşturur ve örnek verileri ekler."""
    print("Veteriner veritabanı oluşturuluyor/güncelleniyor...")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH_VETERINER)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS VETERINERLER (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                adi_soyadi TEXT NOT NULL,
                telefon TEXT,
                email TEXT UNIQUE,
                uzmanlik_alani TEXT
            );
        """)
        conn.commit()
        print("VETERINERLER tablosu oluşturuldu (veya zaten vardı).")

        # Örnek veteriner verileri ekleme (sadece email benzersizse ekler)
        veteriner_verileri = [
            ('Dr. Ayşe Yılmaz', '5551234567', 'ayse.yilmaz@vet.com', 'Genel Veterinerlik'),
            ('Uzm. Veteriner Can Demir', '5557654321', 'can.demir@vet.com', 'Cerrahi'),
            ('Dr. Elif Kaya', '5559876543', 'elif.kaya@vet.com', 'Dahiliye'),
            ('Uzm. Veteriner Burak Şahin', '5551112233', 'burak.sahin@vet.com', 'Vahşi Yaşam'),
            ('Dr. Zeynep Aksoy', '5554445566', 'zeynep.aksoy@vet.com', 'Kuş Bilim'),
            ('Dr. Mehmet Öztürk', '5552223344', 'mehmet.ozturk@vet.com', 'Acil Tıp'),
            ('Uzm. Veteriner Gökçe Aydın', '5556667788', 'gokce.aydin@vet.com', 'Beslenme Uzmanı'),
            ('Dr. Ali Can', '5559990011', 'ali.can@vet.com', 'Diş Hekimliği'),
            ('Uzm. Veteriner Deniz Arslan', '5553332211', 'deniz.arslan@vet.com', 'Hayvan Davranışları'),
            ('Dr. Selin Polat', '5558889900', 'selin.polat@vet.com', 'Dermatoloji'),
            ('Uzm. Veteriner Koray Yüce', '5557778899', 'koray.yuce@vet.com', 'Ortopedi')
        ]

        for veteriner in veteriner_verileri:
            # INSERT OR IGNORE, eğer email zaten varsa eklemeyi atlar
            cursor.execute("""
                INSERT OR IGNORE INTO VETERINERLER (adi_soyadi, telefon, email, uzmanlik_alani)
                VALUES (?, ?, ?, ?)
            """, veteriner)
        conn.commit()
        print("Veterinerlere örnek veri eklendi (varsa atlandı).")

    except sqlite3.Error as e:
        print(f"Veteriner DB oluşturulurken veya güncellenirken hata: {e}")
    finally:
        if conn:
            conn.close()