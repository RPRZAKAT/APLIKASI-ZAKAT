import streamlit as st

# =========================
# BUAT DATABASE OTOMATIS
# =========================

from create_db import create_database

# jalankan pembuatan database dan tabel
create_database()


# =========================
# IMPORT APLIKASI
# =========================

from config.sidebar import sidebar
from config.db_connection import get_connection
from config.auth import login

from modules.dashboard import dashboard
from modules.data_master import data_master
from modules.kategori_zakat import kategori_zakat
from modules.keuangan import keuangan
from modules.laporan import laporan
from modules.about import about



# =========================
# KONFIGURASI APLIKASI
# =========================

st.set_page_config(
    page_title="Sistem Zakat Masjid",
    page_icon="🕌",
    layout="wide"
)



# =========================
# HALAMAN LOGIN
# =========================

def login_page():

    st.title("🕌 Login Sistem Zakat Masjid")

    st.write(
        "Silakan login untuk mengelola data zakat."
    )


    username = st.text_input(
        "Username"
    )


    password = st.text_input(
        "Password",
        type="password"
    )


    if st.button("Login"):

        try:

            conn = get_connection()

            user = login(
                conn,
                username,
                password
            )

            conn.close()


            if user:

                st.session_state["login"] = True
                st.session_state["user"] = user

                st.success(
                    "Login berhasil"
                )

                st.rerun()


            else:

                st.error(
                    "Username atau password salah"
                )


        except Exception as e:

            st.error(
                f"Koneksi database gagal: {e}"
            )



# =========================
# SESSION LOGIN
# =========================

if "login" not in st.session_state:

    st.session_state["login"] = False



# =========================
# MENU UTAMA
# =========================

if st.session_state["login"] is False:

    login_page()


else:

    menu = sidebar()


    if menu == "Dashboard":

        dashboard()


    elif menu == "Data Master":

        data_master()


    elif menu == "Kategori Zakat":

        kategori_zakat()


    elif menu == "Keuangan":

        keuangan()


    elif menu == "Laporan":

        laporan()


    elif menu == "Tentang Aplikasi":

        about()