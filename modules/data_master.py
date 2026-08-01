import streamlit as st
import pandas as pd
from config.db_connection import get_connection


def data_master():

    st.header("📂 Data Master")
    st.caption("Kelola data Muzakki dan Mustahik.")

    conn = get_connection()
    cursor = conn.cursor()

    menu = st.selectbox(
        "Pilih Data",
        ["Muzakki", "Mustahik"]
    )

    # ====================================================
    # DATA MUZAKKI
    # ====================================================

    if menu == "Muzakki":

        st.subheader("👤 Data Muzakki")

        with st.expander("➕ Tambah Data Muzakki", expanded=True):

            with st.form("form_muzakki"):

                nama = st.text_input("Nama Lengkap")
                alamat = st.text_area("Alamat")
                no_hp = st.text_input("Nomor HP")
                pekerjaan = st.text_input("Pekerjaan")

                simpan = st.form_submit_button("💾 Simpan")

                if simpan:

                    if not nama.strip():

                        st.warning("Nama wajib diisi.")

                    else:

                        cursor.execute(
                            """
                            INSERT INTO muzakki
                            (nama,alamat,no_hp,pekerjaan)
                            VALUES(%s,%s,%s,%s)
                            """,
                            (
                                nama,
                                alamat,
                                no_hp,
                                pekerjaan
                            )
                        )

                        conn.commit()

                        st.success(
                            "Data muzakki berhasil disimpan."
                        )

                        st.rerun()

        cari = st.text_input(
            "🔍 Cari Nama Muzakki"
        )

        if cari:

            data = pd.read_sql(
                """
                SELECT *
                FROM muzakki
                WHERE nama LIKE %s
                ORDER BY id DESC
                """,
                conn,
                params=(f"%{cari}%",)
            )

        else:

            data = pd.read_sql(
                """
                SELECT *
                FROM muzakki
                ORDER BY id DESC
                """,
                conn
            )

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total Data : {len(data)}"
        )
            # ====================================================
    # DATA MUSTAHIK
    # ====================================================

    else:

        st.subheader("🤝 Data Mustahik")

        with st.expander("➕ Tambah Data Mustahik", expanded=True):

            with st.form("form_mustahik"):

                nama = st.text_input("Nama Lengkap")
                alamat = st.text_area("Alamat")

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

                no_hp = st.text_input("Nomor HP")

                simpan = st.form_submit_button("💾 Simpan")

                if simpan:

                    if not nama.strip():

                        st.warning("Nama wajib diisi.")

                    else:

                        cursor.execute(
                            """
                            INSERT INTO mustahik
                            (nama,alamat,kategori,no_hp)
                            VALUES(%s,%s,%s,%s)
                            """,
                            (
                                nama,
                                alamat,
                                kategori,
                                no_hp
                            )
                        )

                        conn.commit()

                        st.success(
                            "Data mustahik berhasil disimpan."
                        )

                        st.rerun()

        cari = st.text_input(
            "🔍 Cari Nama Mustahik"
        )

        if cari:

            data = pd.read_sql(
                """
                SELECT *
                FROM mustahik
                WHERE nama LIKE %s
                ORDER BY id DESC
                """,
                conn,
                params=(f"%{cari}%",)
            )

        else:

            data = pd.read_sql(
                """
                SELECT *
                FROM mustahik
                ORDER BY id DESC
                """,
                conn
            )

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total Data : {len(data)}"
        )

    # ====================================================
    # MENU AKSI
    # ====================================================

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:

        if st.button("🔄 Refresh Data"):

            st.rerun()

    with col2:

        st.download_button(
            "📥 Export CSV",
            data.to_csv(index=False).encode("utf-8"),
            file_name=f"{menu.lower()}.csv",
            mime="text/csv"
        )

    cursor.close()
    conn.close()