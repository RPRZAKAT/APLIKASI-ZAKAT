import streamlit as st


def about():

    st.title("🕌 Tentang Aplikasi")

    st.markdown("""
### Sistem Informasi Pengelolaan Zakat Masjid

Sistem ini dikembangkan untuk membantu pengurus masjid dalam
mengelola administrasi zakat secara **efektif, transparan, dan
terintegrasi**. Seluruh data disimpan secara aman pada **Aiven MySQL
Cloud** sehingga dapat diakses secara online sesuai hak akses pengguna.
""")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📋 Fitur Utama")

        st.markdown("""
✅ Dashboard Statistik

✅ Manajemen Data Muzakki

✅ Manajemen Data Mustahik

✅ Manajemen Kategori Zakat

✅ Penerimaan Zakat

✅ Penyaluran Zakat

✅ Laporan Transaksi

✅ Sistem Login Pengguna
""")

    with col2:

        st.subheader("⚙️ Informasi Sistem")

        st.markdown("""
**Nama Aplikasi**

Sistem Informasi Pengelolaan Zakat Masjid

**Versi**

1.0.0

**Framework**

Streamlit

**Bahasa Pemrograman**

Python 3

**Database**

Aiven MySQL Cloud

**Status Sistem**

🟢 Online
""")

    st.divider()

    st.subheader("🎯 Tujuan Aplikasi")

    st.write("""
Aplikasi ini bertujuan untuk meningkatkan efektivitas pengelolaan
zakat di lingkungan masjid melalui proses pencatatan data,
pengelolaan transaksi, serta penyajian laporan yang cepat,
akurat, dan mudah dipahami.
""")

    st.divider()

    st.subheader("👨‍💻 Developer")

    st.info("""
**Rian Parlindungan Rumapea**

Developer Sistem Informasi Pengelolaan Zakat Masjid

Email : rianrumapea0103@gmail.com
""")

    st.divider()

    st.subheader("🛠️ Teknologi yang Digunakan")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success("""
**Frontend**

• Streamlit
""")

    with col2:
        st.info("""
**Backend**

• Python 3
""")

    with col3:
        st.warning("""
**Database**

• Aiven MySQL Cloud
""")

    st.divider()

    st.success("✅ Sistem berhasil berjalan dengan baik dan terhubung ke Aiven MySQL Cloud.")

    st.caption(
        "© 2026 Sistem Informasi Pengelolaan Zakat Masjid | "
        "Developed by Rian Parlindungan Rumapea"
    )