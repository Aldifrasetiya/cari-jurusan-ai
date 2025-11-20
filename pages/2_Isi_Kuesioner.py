import streamlit as st

st.set_page_config(
    page_title="Kuesioner",
    page_icon="📝"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    div.stButton > button:first-child {
        background-color: #2ecc71;
        color: white;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #27ae60;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }
    
    [data-testid="stSidebar"] h1 {
        color: #ffffff;
        font-size: 24px;
    }

    div.stSlider > div[data-baseweb = "slider"] > div > div {
        background-color: #2ecc71 !important;
    }
            
    h1 {
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D); /* Efek Gradasi */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 30px;
    }
    
    div.stInfo, div.stSuccess, div.stWarning {
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    </style>
    """, unsafe_allow_html=True)

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