import streamlit as st
import pandas as pd
from config.db_connection import get_connection


def laporan():

    st.header("📑 Laporan Zakat")

    conn = get_connection()

    # ==========================
    # TOTAL PENERIMAAN
    # ==========================

    masuk = pd.read_sql(
        """
        SELECT COALESCE(SUM(jumlah_bayar),0) AS total
        FROM transaksi_zakat
        """,
        conn
    )

    total_masuk = float(masuk.iloc[0]["total"])

    # ==========================
    # TOTAL PENYALURAN
    # ==========================

    keluar = pd.read_sql(
        """
        SELECT COALESCE(SUM(jumlah),0) AS total
        FROM penyaluran
        """,
        conn
    )

    total_keluar = float(keluar.iloc[0]["total"])

    saldo = total_masuk - total_keluar

    # ==========================
    # RINGKASAN
    # ==========================

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total Zakat Masuk",
        f"Rp {total_masuk:,.0f}".replace(",", ".")
    )

    col2.metric(
        "🎁 Total Penyaluran",
        f"Rp {total_keluar:,.0f}".replace(",", ".")
    )

    col3.metric(
        "💳 Saldo",
        f"Rp {saldo:,.0f}".replace(",", ".")
    )

    st.divider()

    # ==========================
    # DATA PENERIMAAN
    # ==========================

    st.subheader("📋 Riwayat Penerimaan Zakat")

    data_masuk = pd.read_sql(
        """
        SELECT
            t.id,
            t.tanggal,
            m.nama AS muzakki,
            k.nama AS kategori_zakat,
            t.jumlah_bayar,
            t.keterangan
        FROM transaksi_zakat t
        JOIN muzakki m
            ON t.id_muzakki = m.id
        JOIN kategori_zakat k
            ON t.id_kategori = k.id
        ORDER BY t.id DESC
        """,
        conn
    )

    st.dataframe(
        data_masuk,
        use_container_width=True,
        hide_index=True
    )

    # ==========================
    # DATA PENYALURAN
    # ==========================

    st.subheader("🎁 Riwayat Penyaluran Zakat")

    data_keluar = pd.read_sql(
        """
        SELECT
            p.id,
            p.tanggal,
            m.nama AS mustahik,
            p.jumlah,
            p.keterangan
        FROM penyaluran p
        JOIN mustahik m
            ON p.id_mustahik = m.id
        ORDER BY p.id DESC
        """,
        conn
    )

    st.dataframe(
        data_keluar,
        use_container_width=True,
        hide_index=True
    )

    # ==========================
    # REKAPITULASI
    # ==========================

    st.divider()

    st.subheader("📊 Rekapitulasi")

    rekap = pd.DataFrame(
        {
            "Keterangan": [
                "Total Penerimaan",
                "Total Penyaluran",
                "Saldo Akhir"
            ],
            "Nominal": [
                f"Rp {total_masuk:,.0f}".replace(",", "."),
                f"Rp {total_keluar:,.0f}".replace(",", "."),
                f"Rp {saldo:,.0f}".replace(",", ".")
            ]
        }
    )

    st.table(rekap)

    conn.close()