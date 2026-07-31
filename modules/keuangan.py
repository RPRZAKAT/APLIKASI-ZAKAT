import streamlit as st
import pandas as pd
from config.db_connection import get_connection


def keuangan():

    st.header("💰 Transaksi Keuangan Zakat")

    conn = get_connection()
    cursor = conn.cursor()

    menu = st.selectbox(
        "Jenis Transaksi",
        ["Penerimaan Zakat", "Penyaluran Zakat"]
    )

    # =====================================================
    # PENERIMAAN ZAKAT
    # =====================================================

    if menu == "Penerimaan Zakat":

        st.subheader("💰 Penerimaan Zakat")

        muzakki = pd.read_sql(
            "SELECT id, nama FROM muzakki",
            conn
        )

        kategori = pd.read_sql(
            "SELECT id, nama FROM kategori_zakat",
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

        with st.form("form_penerimaan"):

            nama = st.selectbox(
                "Muzakki",
                muzakki["nama"]
            )

            zakat = st.selectbox(
                "Kategori Zakat",
                kategori["nama"]
            )

            tanggal = st.date_input("Tanggal")

            jumlah = st.number_input(
                "Jumlah (Rp)",
                min_value=0,
                step=1000
            )

            ket = st.text_area("Keterangan")

            simpan = st.form_submit_button("Simpan")

            if simpan:

                if jumlah <= 0:

                    st.warning("Jumlah harus lebih dari 0.")

                else:

                    id_muzakki = int(
                        muzakki.loc[muzakki["nama"] == nama, "id"].iloc[0]
                    )

                    id_kategori = int(
                        kategori.loc[kategori["nama"] == zakat, "id"].iloc[0]
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
                        VALUES (%s, %s, %s, %s, %s)
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

                    st.success("✅ Data penerimaan zakat berhasil disimpan")

                    st.rerun()

    # =====================================================
    # PENYALURAN
    # =====================================================

    else:

        st.subheader("🎁 Penyaluran Zakat")

        mustahik = pd.read_sql(
            "SELECT id, nama FROM mustahik",
            conn
        )

        if mustahik.empty:

            st.warning("Data mustahik belum tersedia.")

            cursor.close()
            conn.close()
            return

        with st.form("form_penyaluran"):

            nama = st.selectbox(
                "Mustahik",
                mustahik["nama"]
            )

            tanggal = st.date_input("Tanggal")

            jumlah = st.number_input(
                "Jumlah (Rp)",
                min_value=0,
                step=1000
            )

            ket = st.text_area("Keterangan")

            simpan = st.form_submit_button("Simpan Penyaluran")

            if simpan:

                if jumlah <= 0:

                    st.warning("Jumlah harus lebih dari 0.")

                else:

                    id_mustahik = int(
                        mustahik.loc[mustahik["nama"] == nama, "id"].iloc[0]
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
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            tanggal,
                            id_mustahik,
                            jumlah,
                            ket
                        )
                    )

                    conn.commit()

                    st.success("✅ Data penyaluran berhasil disimpan")

                    st.rerun()

    # =====================================================
    # RIWAYAT PENERIMAAN
    # =====================================================

    st.divider()

    st.subheader("📋 Riwayat Penerimaan Zakat")

    penerimaan = pd.read_sql(
        """
        SELECT
            t.id,
            t.tanggal,
            m.nama AS muzakki,
            k.nama AS kategori,
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
        penerimaan,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # RIWAYAT PENYALURAN
    # =====================================================

    st.subheader("📋 Riwayat Penyaluran")

    penyaluran = pd.read_sql(
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
        penyaluran,
        use_container_width=True,
        hide_index=True
    )

    cursor.close()
    conn.close()