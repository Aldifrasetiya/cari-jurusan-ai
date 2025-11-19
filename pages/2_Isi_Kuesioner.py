import streamlit as st

st.set_page_config(
    page_title="Kuesioner",
    page_icon="📝"
)

st.sidebar.title("Cari Jurusan AI 🤖")
st.sidebar.write("Temukan jurusan kuliah yang paling cocok untukmu.")


st.sidebar.markdown("---") 

st.sidebar.subheader("🎉 Promo Launching")
st.sidebar.info("Fitur 'Analisis Rapor' Premium hanya Rp.19.000!")

st.sidebar.subheader("Dukung Proyek Ini")
SAWERIA_URL = "https://saweria.co/aldifrasetiya"
st.sidebar.link_button("Donasi via Saweria ☕", url=SAWERIA_URL)

st.sidebar.image("img/barcode_saweria.png")


st.title("📝 Bantu Kembangkan AI Ini")
st.write(
    "AI kami belajar dari data. Semakin banyak data berkualitas yang kami miliki, "
    "semakin akurat rekomendasi jurusan yang bisa kami berikan. "
    "Bantuanmu sangat berarti!"
)
st.info(
    "Survei ini **100% anonim** dan hanya butuh 2-3 menit. "
    "Data ini akan digunakan untuk melatih model AI 'Cari Jurusan AI' V2."
)


GOOGLE_FORM_URL = "https://forms.gle/7RfjtcMb3J6sjKvR6"

st.link_button("Mulai Isi Kuesioner Sekarang! 🚀", url=GOOGLE_FORM_URL)

st.markdown("---")
st.write("Terima kasih banyak atas partisipasimu, kamu keren! 🤩")

# st.markdown(f'<iframe src="{GOOGLE_FORM_URL}?embedded=true" width="100%" height="800" frameborder="0" marginheight="0" marginwidth="0">Memuat…</iframe>', unsafe_allow_html=True)