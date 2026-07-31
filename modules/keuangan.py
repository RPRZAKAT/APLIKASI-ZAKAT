import streamlit as st
import pandas as pd
from config.db_connection import get_connection


def keuangan():

    st.header("💰 Transaksi Zakat")

    conn = get_connection()
    cursor = conn.cursor()

    menu = st.selectbox(
        "Jenis Transaksi",
        ["Penerimaan Zakat", "Penyaluran Zakat"]
    )


    # ===== PENERIMAAN =====
    if menu == "Penerimaan Zakat":

        st.subheader("💰 Zakat Masuk")

        muzakki = pd.read_sql(
            "SELECT id,nama FROM muzakki", conn
        )

        kategori = pd.read_sql(
            "SELECT id,nama FROM kategori_zakat", conn
        )

        if muzakki.empty or kategori.empty:
            st.warning("Data muzakki/kategori belum tersedia.")
            return


        nama = st.selectbox(
            "Muzakki",
            muzakki.nama
        )

        zakat = st.selectbox(
            "Kategori Zakat",
            kategori.nama
        )

        tanggal = st.date_input("Tanggal")
        jumlah = st.number_input(
            "Jumlah (Rp)",
            min_value=0
        )

        ket = st.text_area("Keterangan")


        if st.button("Simpan"):

            id_muzakki = int(
                muzakki[muzakki.nama == nama].id.iloc[0]
            )

            id_kategori = int(
                kategori[kategori.nama == zakat].id.iloc[0]
            )


            cursor.execute("""
                INSERT INTO transaksi_zakat
                (tanggal,id_muzakki,id_kategori,jumlah_bayar,keterangan)
                VALUES (?,?,?,?,?)
            """,
            (
                tanggal,
                id_muzakki,
                id_kategori,
                jumlah,
                ket
            ))

            conn.commit()
            st.success("Zakat berhasil disimpan")
            st.rerun()


    # ===== PENYALURAN =====
    else:

        st.subheader("🎁 Penyaluran Zakat")

        mustahik = pd.read_sql(
            "SELECT id,nama FROM mustahik", conn
        )


        if mustahik.empty:
            st.warning("Data mustahik belum tersedia.")
            return


        nama = st.selectbox(
            "Mustahik",
            mustahik.nama
        )

        tanggal = st.date_input("Tanggal")
        jumlah = st.number_input(
            "Jumlah (Rp)",
            min_value=0
        )

        ket = st.text_area("Keterangan")


        if st.button("Simpan Penyaluran"):

            id_mustahik = int(
                mustahik[mustahik.nama == nama].id.iloc[0]
            )


            cursor.execute("""
                INSERT INTO penyaluran
                (tanggal,id_mustahik,jumlah,keterangan)
                VALUES (?,?,?,?)
            """,
            (
                tanggal,
                id_mustahik,
                jumlah,
                ket
            ))

            conn.commit()
            st.success("Penyaluran berhasil disimpan")
            st.rerun()


    st.divider()

    st.subheader("📋 Riwayat Transaksi")

    data = pd.read_sql(
        "SELECT * FROM transaksi_zakat",
        conn
    )

    st.dataframe(
        data,
        use_container_width=True
    )

    conn.close()