import streamlit as st
from config.db_connection import get_connection


def dashboard():

    st.title("🕌 Dashboard Zakat Masjid")
    st.caption("Sistem Informasi Pengelolaan Zakat, Infaq, dan Sedekah")

    st.divider()

    # Koneksi database
    conn = get_connection()
    cursor = conn.cursor()

    # ==========================
    # DATA STATISTIK
    # ==========================

    # Jumlah Muzakki
    cursor.execute("SELECT COUNT(*) FROM muzakki")
    jumlah_muzakki = cursor.fetchone()[0]

    # Jumlah Mustahik
    cursor.execute("SELECT COUNT(*) FROM mustahik")
    jumlah_mustahik = cursor.fetchone()[0]

    # Total Zakat Masuk
    cursor.execute("""
        SELECT COALESCE(SUM(jumlah_bayar),0)
        FROM transaksi_zakat
    """)
    total_zakat = cursor.fetchone()[0]

    # Total Penyaluran
    cursor.execute("""
        SELECT COALESCE(SUM(jumlah),0)
        FROM penyaluran
    """)
    total_penyaluran = cursor.fetchone()[0]

    conn.close()


    # Hitung saldo
    saldo_zakat = total_zakat - total_penyaluran


    # ==========================
    # KARTU STATISTIK
    # ==========================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👤 Muzakki",
        jumlah_muzakki
    )

    col2.metric(
        "🤝 Mustahik",
        jumlah_mustahik
    )

    col3.metric(
        "💰 Zakat Masuk",
        f"Rp {total_zakat:,.0f}".replace(",", ".")
    )

    col4.metric(
        "💳 Saldo Zakat",
        f"Rp {saldo_zakat:,.0f}".replace(",", ".")
    )


    st.divider()


    # ==========================
    # SELAMAT DATANG
    # ==========================

    st.subheader("📋 Selamat Datang")

    st.write("""
Aplikasi Pengelolaan Zakat Masjid membantu pengurus masjid dalam
melakukan pencatatan dan pengelolaan zakat secara mudah dan terstruktur.

Sistem ini mencakup:

- 👤 Data Muzakki
- 🤝 Data Mustahik
- 📂 Kategori Zakat
- 💰 Transaksi Zakat
- 🎁 Penyaluran Zakat
- 📑 Laporan Zakat
    """)


    st.divider()


    # ==========================
    # INFORMASI KEUANGAN
    # ==========================

    st.subheader("📊 Ringkasan Keuangan")

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"""
💰 Total Penerimaan Zakat

Rp {total_zakat:,.0f}
""".replace(",", ".")
        )


    with col2:
        st.info(
            f"""
🎁 Total Penyaluran Zakat

Rp {total_penyaluran:,.0f}
""".replace(",", ".")
        )


    st.divider()


    # ==========================
    # STATUS DATA
    # ==========================

    if jumlah_muzakki == 0:

        st.warning(
            "Belum ada data muzakki. Silakan tambahkan data terlebih dahulu."
        )

    else:

        st.success(
            "✅ Data zakat berhasil terhubung dengan database."
        )