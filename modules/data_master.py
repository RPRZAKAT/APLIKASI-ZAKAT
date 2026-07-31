import streamlit as st
import pandas as pd
from config.db_connection import get_connection


def data_master():

    st.header("📂 Data Master Zakat")

    pilihan = st.selectbox(
        "Pilih Data",
        ["Muzakki", "Mustahik"]
    )

    conn = get_connection()
    cursor = conn.cursor()


    # ================= MUZAKKI =================

    if pilihan == "Muzakki":

        st.subheader("👤 Data Muzakki")

        with st.form("form_muzakki"):

            nama = st.text_input("Nama")
            alamat = st.text_input("Alamat")
            no_hp = st.text_input("No HP")

            simpan = st.form_submit_button("Simpan")

            if simpan:

                cursor.execute("""
                    INSERT INTO muzakki
                    (nama, alamat, no_hp)
                    VALUES (?,?,?)
                """,
                (nama, alamat, no_hp))

                conn.commit()
                st.success("Data muzakki tersimpan")
                st.rerun()


        data = pd.read_sql(
            "SELECT * FROM muzakki",
            conn
        )

        st.dataframe(
            data,
            use_container_width=True
        )


    # ================= MUSTAHIK =================

    else:

        st.subheader("🤝 Data Mustahik")

        with st.form("form_mustahik"):

            nama = st.text_input("Nama")
            alamat = st.text_input("Alamat")

            kategori = st.selectbox(
                "Kategori",
                [
                    "Fakir",
                    "Miskin",
                    "Amil",
                    "Muallaf",
                    "Fisabilillah",
                    "Ibnu Sabil"
                ]
            )

            simpan = st.form_submit_button("Simpan")

            if simpan:

                cursor.execute("""
                    INSERT INTO mustahik
                    (nama, alamat, kategori)
                    VALUES (?,?,?)
                """,
                (nama, alamat, kategori))

                conn.commit()
                st.success("Data mustahik tersimpan")
                st.rerun()


        data = pd.read_sql(
            "SELECT * FROM mustahik",
            conn
        )

        st.dataframe(
            data,
            use_container_width=True
        )


    conn.close()