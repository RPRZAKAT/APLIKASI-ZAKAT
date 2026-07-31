import streamlit as st
from config.db_connection import get_connection


def dashboard():

    st.title("🕌 Dashboard Sistem Informasi Zakat Masjid")
    st.caption("Sistem Informasi Pengelolaan Zakat, Infaq, dan Sedekah")

    st.divider()

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================
    # JUMLAH MUZAKKI
    # =====================================

    cursor.execute("SELECT COUNT(*) FROM muzakki")
    jumlah_muzakki = cursor.fetchone()[0]

    # =====================================
    # JUMLAH MUSTAHIK
    # =====================================

    cursor.execute("SELECT COUNT(*) FROM mustahik")
    jumlah_mustahik = cursor.fetchone()[0]

    # =====================================
    # TOTAL ZAKAT MASUK
    # =====================================

    cursor.execute("""
        SELECT COALESCE(SUM(jumlah_bayar),0)
        FROM transaksi_zakat
    """)

    total_zakat = cursor.fetchone()[0]

    if total_zakat is None:
        total_zakat = 0

    # =====================================
    # TOTAL PENYALURAN
    # =====================================

    cursor.execute("""
        SELECT COALESCE(SUM(jumlah),0)
        FROM penyaluran
    """)

    total_penyaluran = cursor.fetchone()[0]

    if total_penyaluran is None:
        total_penyaluran = 0

    # =====================================
    # SALDO
    # =====================================

    saldo = total_zakat - total_penyaluran

    # =====================================
    # TOTAL TRANSAKSI
    # =====================================

    cursor.execute("SELECT COUNT(*) FROM transaksi_zakat")
    jumlah_transaksi = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    # =====================================
    # KARTU DASHBOARD
    # =====================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👤 Muzakki",
            jumlah_muzakki
        )

    with col2:
        st.metric(
            "🤝 Mustahik",
            jumlah_mustahik
        )

    with col3:
        st.metric(
            "💰 Zakat Masuk",
            f"Rp {total_zakat:,.0f}".replace(",", ".")
        )

    with col4:
        st.metric(
            "💳 Saldo",
            f"Rp {saldo:,.0f}".replace(",", ".")
        )

    st.divider()

    # =====================================
    # RINGKASAN
    # =====================================

    st.subheader("📊 Ringkasan Sistem")

    col1, col2 = st.columns(2)

    with col1:

        st.success(f"""
Jumlah Muzakki

**{jumlah_muzakki} Orang**

Jumlah Mustahik

**{jumlah_mustahik} Orang**
""")

    with col2:

        st.info(f"""
Jumlah Transaksi

**{jumlah_transaksi} Transaksi**

Saldo Saat Ini

**Rp {saldo:,.0f}**
""".replace(",", "."))

    st.divider()

    # =====================================
    # INFORMASI KEUANGAN
    # =====================================

    st.subheader("💰 Informasi Keuangan")

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"Total Penerimaan\n\nRp {total_zakat:,.0f}".replace(",", ".")
        )

    with col2:

        st.warning(
            f"Total Penyaluran\n\nRp {total_penyaluran:,.0f}".replace(",", ".")
        )

    st.divider()

    # =====================================
    # STATUS DATABASE
    # =====================================

    st.subheader("📌 Status Sistem")

    if jumlah_muzakki == 0:

        st.warning(
            "Belum ada data muzakki. Silakan tambahkan data terlebih dahulu."
        )

    elif jumlah_mustahik == 0:

        st.warning(
            "Belum ada data mustahik. Silakan tambahkan data terlebih dahulu."
        )

    else:

        st.success(
            "✅ Sistem berhasil terhubung dengan database MySQL."
        )

    st.divider()

    # =====================================
    # PETUNJUK PENGGUNAAN
    # =====================================

    st.subheader("📖 Petunjuk Penggunaan")

    st.markdown("""
1. Tambahkan data **Muzakki**.
2. Tambahkan data **Mustahik**.
3. Tambahkan **Kategori Zakat**.
4. Input transaksi penerimaan zakat.
5. Input transaksi penyaluran zakat.
6. Lihat laporan pada menu **Laporan**.
""")