import streamlit as st
import pandas as pd
from config.db_connection import get_connection


def keuangan():

    st.header("💰 Transaksi Keuangan Zakat")
    st.caption("Kelola transaksi penerimaan dan penyaluran zakat masjid.")

    conn = get_connection()
    cursor = conn.cursor()

    # ==========================
    # RINGKASAN KEUANGAN
    # ==========================

    total_masuk = pd.read_sql(
        "SELECT COALESCE(SUM(jumlah_bayar),0) total FROM transaksi_zakat",
        conn
    )["total"][0]

    total_keluar = pd.read_sql(
        "SELECT COALESCE(SUM(jumlah),0) total FROM penyaluran",
        conn
    )["total"][0]

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

    menu = st.selectbox(
        "Jenis Transaksi",
        (
            "Penerimaan Zakat",
            "Penyaluran Zakat"
        )
    )

    # ==================================================
    # PENERIMAAN ZAKAT
    # ==================================================

    if menu == "Penerimaan Zakat":

        muzakki = pd.read_sql(
            "SELECT id,nama FROM muzakki ORDER BY nama",
            conn
        )

        kategori = pd.read_sql(
            "SELECT id,nama FROM kategori_zakat ORDER BY nama",
            conn
        )

        if muzakki.empty:

            st.warning("Data muzakki belum tersedia.")
            cursor.close()
            conn.close()
            return

        if kategori.empty:

            st.warning("Data kategori zakat belum tersedia.")
            cursor.close()
            conn.close()
            return

        with st.expander("➕ Tambah Penerimaan Zakat", expanded=True):

            with st.form("form_penerimaan"):

                nama = st.selectbox(
                    "Nama Muzakki",
                    muzakki["nama"]
                )

                zakat = st.selectbox(
                    "Kategori Zakat",
                    kategori["nama"]
                )

                tanggal = st.date_input("Tanggal")

                jumlah = st.number_input(
                    "Jumlah (Rp)",
                    min_value=1000,
                    step=1000
                )

                ket = st.text_area("Keterangan")

                simpan = st.form_submit_button("💾 Simpan")

                if simpan:

                    id_muzakki = int(
                        muzakki.loc[
                            muzakki["nama"] == nama,
                            "id"
                        ].iloc[0]
                    )

                    id_kategori = int(
                        kategori.loc[
                            kategori["nama"] == zakat,
                            "id"
                        ].iloc[0]
                    )

                    cursor.execute(
                        """
                        INSERT INTO transaksi_zakat
                        (
                            tanggal,
                            id_muzakki,
                            id_kategori,
                            jumlah_bayar,
                            keterangan
                        )
                        VALUES
                        (%s,%s,%s,%s,%s)
                        """,
                        (
                            tanggal,
                            id_muzakki,
                            id_kategori,
                            jumlah,
                            ket
                        )
                    )

                    conn.commit()

                    st.success(
                        "✅ Data penerimaan berhasil disimpan."
                    )

                    st.rerun()

        # ==================================================
    # PENYALURAN ZAKAT
    # ==================================================

    else:

        mustahik = pd.read_sql(
            "SELECT id,nama FROM mustahik ORDER BY nama",
            conn
        )

        if mustahik.empty:

            st.warning("Data mustahik belum tersedia.")
            cursor.close()
            conn.close()
            return

        with st.expander("🎁 Tambah Penyaluran Zakat", expanded=True):

            with st.form("form_penyaluran"):

                nama = st.selectbox(
                    "Nama Mustahik",
                    mustahik["nama"]
                )

                tanggal = st.date_input("Tanggal Penyaluran")

                jumlah = st.number_input(
                    "Jumlah (Rp)",
                    min_value=1000,
                    step=1000
                )

                ket = st.text_area("Keterangan")

                simpan = st.form_submit_button(
                    "💾 Simpan Penyaluran"
                )

                if simpan:

                    id_mustahik = int(
                        mustahik.loc[
                            mustahik["nama"] == nama,
                            "id"
                        ].iloc[0]
                    )

                    cursor.execute(
                        """
                        INSERT INTO penyaluran
                        (
                            tanggal,
                            id_mustahik,
                            jumlah,
                            keterangan
                        )
                        VALUES
                        (%s,%s,%s,%s)
                        """,
                        (
                            tanggal,
                            id_mustahik,
                            jumlah,
                            ket
                        )
                    )

                    conn.commit()

                    st.success(
                        "✅ Data penyaluran berhasil disimpan."
                    )

                    st.rerun()

    st.divider()

    # ==========================================
    # RIWAYAT PENERIMAAN
    # ==========================================

    st.subheader("📋 Riwayat Penerimaan Zakat")

    cari = st.text_input(
        "🔍 Cari Nama Muzakki"
    )

    if cari:

        penerimaan = pd.read_sql(
            """
            SELECT
                t.id,
                t.tanggal,
                m.nama AS Muzakki,
                k.nama AS Kategori,
                t.jumlah_bayar AS Jumlah,
                t.keterangan AS Keterangan
            FROM transaksi_zakat t
            JOIN muzakki m
                ON t.id_muzakki=m.id
            JOIN kategori_zakat k
                ON t.id_kategori=k.id
            WHERE m.nama LIKE %s
            ORDER BY t.id DESC
            """,
            conn,
            params=(f"%{cari}%",)
        )

    else:

        penerimaan = pd.read_sql(
            """
            SELECT
                t.id,
                t.tanggal,
                m.nama AS Muzakki,
                k.nama AS Kategori,
                t.jumlah_bayar AS Jumlah,
                t.keterangan AS Keterangan
            FROM transaksi_zakat t
            JOIN muzakki m
                ON t.id_muzakki=m.id
            JOIN kategori_zakat k
                ON t.id_kategori=k.id
            ORDER BY t.id DESC
            """,
            conn
        )

    if not penerimaan.empty:

        penerimaan["Jumlah"] = penerimaan["Jumlah"].apply(
            lambda x: f"Rp {x:,.0f}".replace(",", ".")
        )

        st.dataframe(
            penerimaan,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Belum ada data penerimaan zakat.")

    st.caption(f"Total Data : {len(penerimaan)}")
       # ==========================================
    # RIWAYAT PENYALURAN
    # ==========================================

    st.divider()
    st.subheader("📋 Riwayat Penyaluran Zakat")

    cari2 = st.text_input(
        "🔍 Cari Nama Mustahik"
    )

    if cari2:

        penyaluran = pd.read_sql(
            """
            SELECT
                p.id,
                p.tanggal,
                m.nama AS Mustahik,
                p.jumlah AS Jumlah,
                p.keterangan AS Keterangan
            FROM penyaluran p
            JOIN mustahik m
                ON p.id_mustahik = m.id
            WHERE m.nama LIKE %s
            ORDER BY p.id DESC
            """,
            conn,
            params=(f"%{cari2}%",)
        )

    else:

        penyaluran = pd.read_sql(
            """
            SELECT
                p.id,
                p.tanggal,
                m.nama AS Mustahik,
                p.jumlah AS Jumlah,
                p.keterangan AS Keterangan
            FROM penyaluran p
            JOIN mustahik m
                ON p.id_mustahik = m.id
            ORDER BY p.id DESC
            """,
            conn
        )

    if not penyaluran.empty:

        penyaluran["Jumlah"] = penyaluran["Jumlah"].apply(
            lambda x: f"Rp {x:,.0f}".replace(",", ".")
        )

        st.dataframe(
            penyaluran,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Belum ada data penyaluran zakat.")

    st.caption(f"Total Data : {len(penyaluran)}")

    st.divider()

    # ==========================================
    # REFRESH DATA
    # ==========================================

    col1, col2 = st.columns([8, 2])

    with col2:

        if st.button("🔄 Refresh"):

            st.rerun()

    # ==========================================
    # INFORMASI
    # ==========================================

    st.info("""
ℹ️ Pastikan data Muzakki, Mustahik, dan Kategori Zakat telah tersedia
sebelum melakukan transaksi penerimaan maupun penyaluran zakat.
""")

    cursor.close()
    conn.close()