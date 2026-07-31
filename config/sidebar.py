import streamlit as st
import os


def sidebar():

    with st.sidebar:


        logo_path = "assets/logo.png"


        if os.path.exists(logo_path):

            st.image(
                logo_path,
                width=120
            )

        else:

            st.warning(
                "Logo belum tersedia"
            )


        st.title(
            "🕌 Sistem Zakat Masjid"
        )


        menu = st.radio(
            "Menu",
            [
                "Dashboard",
                "Data Master",
                "Kategori Zakat",
                "Keuangan",
                "Laporan",
                "Tentang Aplikasi"
            ]
        )


    return menu