import streamlit as st
import pandas as pd
from datetime import datetime
from config.db_connection import get_connection


def laporan():

    st.header("📑 Laporan Zakat")
    st.caption("Laporan penerimaan dan penyaluran dana zakat.")

    conn = get_connection()

    # ==========================
    # FILTER
    # ==========================

    col1, col2 = st.columns(2)

    with col1:
        periode = st.selectbox(
            "Periode",
            [
                "Semua Data",
                "Bulan Ini",
                "Tahun Ini"
            ]
        )

    with col2:
        cari = st.text_input(
            "🔍 Cari Nama"
        )

    # ==========================
    # RINGKASAN
    # ==========================

    total_masuk = pd.read_sql(
        """
        SELECT COALESCE(SUM(jumlah_bayar),0) total
        FROM transaksi_zakat
        """,
        conn
    ).iloc[0]["total"]

    total_keluar = pd.read_sql(
        """
        SELECT COALESCE(SUM(jumlah),0) total
        FROM penyaluran
        """,
        conn
    ).iloc[0]["total"]

    saldo = total_masuk - total_keluar

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Penerimaan",
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

        # ==========================
    # DATA PENERIMAAN
    # ==========================

    st.subheader("📋 Laporan Penerimaan")

    sql = """
    SELECT
        t.tanggal,
        m.nama AS Muzakki,
        k.nama AS Kategori,
        t.jumlah_bayar AS Jumlah,
        t.keterangan
    FROM transaksi_zakat t
    JOIN muzakki m ON t.id_muzakki=m.id
    JOIN kategori_zakat k ON t.id_kategori=k.id
    ORDER BY t.tanggal DESC
    """

    masuk = pd.read_sql(sql, conn)

    if cari:

        masuk = masuk[
            masuk["Muzakki"].str.contains(
                cari,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        masuk,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "📥 Export Penerimaan",
        masuk.to_csv(index=False).encode("utf-8"),
        "laporan_penerimaan.csv",
        "text/csv"
    )

    st.divider()

    # ==========================
    # DATA PENYALURAN
    # ==========================

    st.subheader("🎁 Laporan Penyaluran")

    sql = """
    SELECT
        p.tanggal,
        m.nama AS Mustahik,
        p.jumlah AS Jumlah,
        p.keterangan
    FROM penyaluran p
    JOIN mustahik m ON p.id_mustahik=m.id
    ORDER BY p.tanggal DESC
    """

    keluar = pd.read_sql(sql, conn)

    if cari:

        keluar = keluar[
            keluar["Mustahik"].str.contains(
                cari,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        keluar,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "📥 Export Penyaluran",
        keluar.to_csv(index=False).encode("utf-8"),
        "laporan_penyaluran.csv",
        "text/csv"
    )

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

    st.caption(
        f"Laporan diperbarui : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

    if st.button("🔄 Refresh"):

        st.rerun()

    conn.close()