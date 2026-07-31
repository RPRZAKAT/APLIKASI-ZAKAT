import streamlit as st
import pandas as pd
from config.db_connection import get_connection


def kategori_zakat():

    st.header("📂 Kategori Zakat")

    st.write(
        "Kelola jenis zakat yang tersedia pada sistem."
    )

    conn = get_connection()
    cursor = conn.cursor()


    # ==========================
    # TAMBAH KATEGORI
    # ==========================

    with st.form("form_kategori"):

        nama = st.text_input(
            "Nama Zakat"
        )

        keterangan = st.text_input(
            "Keterangan"
        )

        simpan = st.form_submit_button(
            "Simpan"
        )


        if simpan:

            cursor.execute("""
                INSERT INTO kategori_zakat
                (nama, keterangan)
                VALUES (?,?)
            """,
            (
                nama,
                keterangan
            ))

            conn.commit()

            st.success(
                "Kategori zakat berhasil disimpan"
            )

            st.rerun()



    # ==========================
    # TAMPIL DATA
    # ==========================

    st.subheader("📋 Daftar Kategori Zakat")


    data = pd.read_sql(
        """
        SELECT *
        FROM kategori_zakat
        """,
        conn
    )


    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


    conn.close()