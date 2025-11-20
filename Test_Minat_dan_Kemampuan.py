import streamlit as st
import pandas as pd
import joblib
import numpy as np
from fpdf import FPDF

st.set_page_config(
    page_title="Cari Jurusan AI",
    page_icon="🤖"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

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
        text-align: center;
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

QUESTION_BANK = {
    "logika": [
        "Saya suka memecahkan teka-teki, puzzle, atau permainan strategi (seperti Catur/Sudoku).",
        "Ketika menghadapi masalah, saya lebih suka mencari akar penyebabnya secara sistematis.",
        "Saya penasaran bagaimana cara kerja mesin atau aplikasi komputer di balik layar."
    ],
    "verbal": [
        "Saya sering diminta teman untuk menjelaskan materi pelajaran karena penjelasan saya mudah dimengerti.",
        "Saya suka membaca buku, artikel, atau menulis cerita/esai di waktu luang.",
        "Saya merasa percaya diri saat harus berbicara atau presentasi di depan umum."
    ],
    "sosial": [
        "Saya lebih suka bekerja dalam kelompok (tim) daripada bekerja sendirian.",
        "Teman-teman sering curhat masalah pribadi kepada saya karena saya pendengar yang baik.",
        "Saya mudah bergaul dan memulai percakapan dengan orang yang baru dikenal."
    ],
    "kreatif": [
        "Saya sering memiliki ide-ide yang dianggap 'unik' atau 'out-of-the-box' oleh orang lain.",
        "Saya sangat peduli pada estetika, desain, warna, atau tampilan visual suatu benda.",
        "Saya suka menciptakan sesuatu (menggambar, bermusik, video) daripada sekadar menikmatinya."
    ],
    "analitis": [
        "Saya suka bekerja dengan angka, tabel, dan data statistik.",
        "Saya adalah orang yang teliti dan memperhatikan detail kecil yang sering dilewatkan orang lain.",
        "Saya suka menyusun rencana atau jadwal kegiatan secara terperinci."
    ]
}

def render_quiz_and_get_scores():
    """
    Menampilkan kuesioner di Streamlit dan mengembalikan dictionary skor 0.0 - 1.0
    """
    
    OPTIONS = ["Sangat Tidak Setuju", "Tidak Setuju", "Netral", "Setuju", "Sangat Setuju"]

    MAPPING = {
        "Sangat Tidak Setuju": 1,
        "Tidak Setuju": 2,
        "Netral": 3,
        "Setuju": 4,
        "Sangat Setuju": 5
    }
    
    final_scores = {}
    
    for category, questions in QUESTION_BANK.items():
        st.markdown(f"### Bidang: {category.capitalize()}")
        total_score_category = 0
        max_score_category = len(questions) * 5
        
        for i, q in enumerate(questions):
            answer = st.select_slider(
                label=f"{i+1}. {q}",
                options=OPTIONS,
                value="Netral", # Default
                key=f"{category}_{i}"
            )
            total_score_category += MAPPING[answer]
            
        normalized_score = total_score_category / max_score_category
        final_scores[category] = normalized_score
        
        st.markdown("---")

    return final_scores


st.sidebar.title("Cari Jurusan AI 🤖")
st.sidebar.write("Temukan jurusan kuliah yang paling cocok untukmu.")

st.sidebar.markdown("---") 

st.sidebar.subheader("🎉 Promo Launching")
st.sidebar.info("Fitur 'Analisis Rapor' Premium hanya Rp.19.000!")

st.sidebar.subheader("Dukung Proyek Ini")
SAWERIA_URL = "https://saweria.co/aldifrasetiya"
st.sidebar.link_button("Donasi via Saweria ☕", url=SAWERIA_URL)

st.sidebar.image("img/barcode_saweria.png")

model = joblib.load("model/model_cari_jurusan_v1.5.pkl")

st.set_page_config(page_title="Cari Jurusan AI", layout="wide")

st.title("💡 Test Minat & Kemampuan")
st.write("Jawablah pertanyaan berikut sejujur mungkin berdasarkan dirimu.")

scores_input = render_quiz_and_get_scores()

if st.button("Lihat Hasil & Rekomendasi Jurusan"):

    input_df = pd.DataFrame([scores_input])
    target_order = ['logika', 'verbal', 'sosial', 'kreatif', 'analitis']
    input_to = input_df[target_order]
    
    st.subheader("Profil Minat Kamu")
    st.json(scores_input)
    
    prediction = model.predict(input_to)[0]
    
    st.success(f"🎯 Rekomendasi Jurusan Utama: **{prediction}**")
    st.info("Ingat, ini hanya rekomendasi berdasarkan minat dan kemampuan yang kamu isi. "
            "Pertimbangkan juga faktor lain seperti passion, peluang karir, dan saran dari orang tua/guru.")
    st.write("Kurang puas dengan hasil dari fitur test minat dan kemampuan? Coba fitur Analisis Rapor!")
