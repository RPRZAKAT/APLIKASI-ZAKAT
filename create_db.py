import mysql.connector
from mysql.connector import Error


def create_database():

    try:
        # koneksi awal tanpa database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )

        cursor = conn.cursor()

        # buat database
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS zakat_masjid"
        )

        cursor.execute(
            "USE zakat_masjid"
        )


        # =====================
        # TABLE USERS
        # =====================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(100) NOT NULL,
            nama_lengkap VARCHAR(100),
            role VARCHAR(20),
            status VARCHAR(20)
        )
        """)


        # =====================
        # TABLE MUZAKKI
        # =====================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS muzakki(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(100),
            alamat TEXT,
            no_hp VARCHAR(20),
            pekerjaan VARCHAR(50)
        )
        """)


        # =====================
        # TABLE MUSTAHIK
        # =====================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS mustahik(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(100),
            alamat TEXT,
            kategori VARCHAR(50),
            no_hp VARCHAR(20)
        )
        """)


        # =====================
        # TABLE KATEGORI
        # =====================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS kategori_zakat(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nama VARCHAR(50),
            keterangan TEXT
        )
        """)


        # =====================
        # TABLE TRANSAKSI
        # =====================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi_zakat(
            id INT AUTO_INCREMENT PRIMARY KEY,
            tanggal DATE,
            id_muzakki INT,
            id_kategori INT,
            jumlah_bayar INT,
            keterangan TEXT,

            FOREIGN KEY(id_muzakki)
            REFERENCES muzakki(id)
            ON DELETE CASCADE,

            FOREIGN KEY(id_kategori)
            REFERENCES kategori_zakat(id)
            ON DELETE CASCADE
        )
        """)


        # =====================
        # TABLE PENYALURAN
        # =====================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS penyaluran(
            id INT AUTO_INCREMENT PRIMARY KEY,
            tanggal DATE,
            id_mustahik INT,
            jumlah INT,
            keterangan TEXT,

            FOREIGN KEY(id_mustahik)
            REFERENCES mustahik(id)
            ON DELETE CASCADE
        )
        """)



        # =====================
        # USER ADMIN DEFAULT
        # =====================

        cursor.execute("""
        INSERT IGNORE INTO users
        (
            username,
            password,
            nama_lengkap,
            role,
            status
        )
        VALUES
        (
            'admin',
            'admin123',
            'Administrator',
            'admin',
            'aktif'
        )
        """)


        # =====================
        # DATA KATEGORI DEFAULT
        # =====================

        cursor.execute("""
        INSERT IGNORE INTO kategori_zakat
        (
            id,
            nama,
            keterangan
        )
        VALUES
        (1,'Zakat Fitrah','Zakat wajib Ramadan'),
        (2,'Zakat Mal','Zakat harta'),
        (3,'Infaq','Sumbangan sukarela'),
        (4,'Sedekah','Amal sosial')
        """)


        conn.commit()


        cursor.close()
        conn.close()


        print("================================")
        print("DATABASE BERHASIL DIBUAT")
        print("Database : zakat_masjid")
        print("User     : admin")
        print("Password : admin123")
        print("================================")


    except Error as e:

        print("Gagal membuat database")
        print(e)



if __name__ == "__main__":

    create_database()