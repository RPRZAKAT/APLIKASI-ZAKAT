import streamlit as st


def about():

    st.title("ℹ️ Tentang Aplikasi")

    st.divider()

    st.subheader("🕌 Sistem Informasi Pengelolaan Zakat Masjid")

    st.write("""
Aplikasi ini membantu pengurus masjid dalam mengelola data zakat,
mulai dari data muzakki, mustahik, transaksi zakat, hingga laporan.
    """)

    st.divider()

    st.subheader("📋 Fitur")

    st.markdown("""
- 👤 Data Muzakki
- 🤝 Data Mustahik
- 💰 Transaksi Zakat
- 📑 Laporan Zakat
- 📤 Export Data
    """)

    st.divider()

    st.caption("© 2026 Sistem Informasi Pengelolaan Zakat Masjid")