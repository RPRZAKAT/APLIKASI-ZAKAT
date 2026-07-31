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

    # =======================
    # DATA MUZAKKI
    # =======================
    if pilihan == "Muzakki":

        st.subheader("👤 Data Muzakki")

        with st.form("form_muzakki"):

            nama = st.text_input("Nama")
            alamat = st.text_input("Alamat")
            no_hp = st.text_input("No HP")
            pekerjaan = st.text_input("Pekerjaan")

            simpan = st.form_submit_button("Simpan")

            if simpan:

                if nama == "":
                    st.warning("Nama wajib diisi.")

                else:

                    cursor.execute(
                        """
                        INSERT INTO muzakki
                        (nama, alamat, no_hp, pekerjaan)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (nama, alamat, no_hp, pekerjaan)
                    )

                    conn.commit()

                    st.success("✅ Data muzakki berhasil disimpan")

                    st.rerun()

        data = pd.read_sql(
            "SELECT * FROM muzakki",
            conn
        )

        st.dataframe(
            data,
            use_container_width=True
        )

    # =======================
    # DATA MUSTAHIK
    # =======================
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

            no_hp = st.text_input("No HP")

            simpan = st.form_submit_button("Simpan")

            if simpan:

                if nama == "":
                    st.warning("Nama wajib diisi.")

                else:

                    cursor.execute(
                        """
                        INSERT INTO mustahik
                        (nama, alamat, kategori, no_hp)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (nama, alamat, kategori, no_hp)
                    )

                    conn.commit()

                    st.success("✅ Data mustahik berhasil disimpan")

                    st.rerun()

        data = pd.read_sql(
            "SELECT * FROM mustahik",
            conn
        )

        st.dataframe(
            data,
            use_container_width=True
        )

    cursor.close()
    conn.close()