import streamlit as st
import pandas as pd
from config.db_connection import get_connection


def laporan():

    st.header("📑 Laporan Zakat")

    conn = get_connection()

    # Total zakat masuk
    masuk = pd.read_sql("""
        SELECT COALESCE(SUM(jumlah_bayar),0) AS total
        FROM transaksi_zakat
    """, conn)

    total_masuk = masuk["total"][0]


    # Total penyaluran
    keluar = pd.read_sql("""
        SELECT COALESCE(SUM(jumlah),0) AS total
        FROM penyaluran
    """, conn)

    total_keluar = keluar["total"][0]


    saldo = total_masuk - total_keluar


    # Ringkasan
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Zakat Masuk",
        f"Rp {total_masuk:,.0f}".replace(",", ".")
    )

    col2.metric(
        "🎁 Penyaluran",
        f"Rp {total_keluar:,.0f}".replace(",", ".")
    )

    col3.metric(
        "💳 Saldo",
        f"Rp {saldo:,.0f}".replace(",", ".")
    )


    st.divider()


    # Riwayat penerimaan
    st.subheader("📋 Data Penerimaan Zakat")

    data_masuk = pd.read_sql("""
        SELECT 
            tanggal,
            id_muzakki,
            id_kategori,
            jumlah_bayar,
            keterangan
        FROM transaksi_zakat
    """, conn)

    st.dataframe(
        data_masuk,
        use_container_width=True
    )


    # Riwayat penyaluran
    st.subheader("🎁 Data Penyaluran Zakat")

    data_keluar = pd.read_sql("""
        SELECT
            tanggal,
            id_mustahik,
            jumlah,
            keterangan
        FROM penyaluran
    """, conn)

    st.dataframe(
        data_keluar,
        use_container_width=True
    )


    conn.close()