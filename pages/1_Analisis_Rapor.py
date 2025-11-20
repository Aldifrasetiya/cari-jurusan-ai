import streamlit as st
import pandas as pd
import joblib
import numpy as np
from fpdf import FPDF

st.set_page_config(
    page_title="Analisis Rapor",
    page_icon="📄"
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

if 'premium_unlocked' not in st.session_state:
    st.session_state.premium_unlocked = False

MAPEL_INTI = {
    'matematika': 'Matematika (Wajib/Umum)',
    'bahasa_indonesia': 'Bahasa Indonesia',
    'bahasa_inggris': 'Bahasa Inggris',
    'fisika': 'Fisika',
    'kimia': 'Kimia',
    'biologi': 'Biologi',
    'ekonomi': 'Ekonomi',
    'sosiologi': 'Sosiologi',
    'geografi': 'Geografi'
}

def get_insight_from_scores(scores):

    insights = []
    
    mapel_saintek = ['matematika', 'fisika', 'kimia', 'biologi']
    skor_saintek = [scores[mapel] for mapel in mapel_saintek if scores[mapel] > 0]
    avg_saintek = sum(skor_saintek) / len(skor_saintek) if len(skor_saintek) > 0 else 0
    
    mapel_soshum = ['ekonomi', 'sosiologi', 'geografi']
    skor_soshum = [scores[mapel] for mapel in mapel_soshum if scores[mapel] > 0]
    avg_soshum = sum(skor_soshum) / len(skor_soshum) if len(skor_soshum) > 0 else 0

    THRESHOLD_BAGUS = 80
    
    if avg_saintek > 0 and avg_soshum > 0:

        if avg_saintek >= THRESHOLD_BAGUS and avg_soshum >= THRESHOLD_BAGUS:
            insights.append(f"Kamu punya bakat seimbang! Nilai Saintek ({avg_saintek:.2f}) dan Soshum ({avg_soshum:.2f}) sama-sama kuat. Ini membuka banyak pilihan, dari Manajemen, Arsitektur, hingga Psikologi Industri.")
        
        elif avg_saintek >= THRESHOLD_BAGUS and avg_saintek > (avg_soshum + 5): # +5 sbg 'margin'
            insights.append(f"Profilmu adalah **Spesialis Saintek**. Rata-rata Saintek-mu ({avg_saintek:.2f}) jelas lebih menonjol daripada Soshum ({avg_soshum:.2f}). Fokus pada jurusan rumpun Teknik & Sains Murni.")
            
        elif avg_soshum >= THRESHOLD_BAGUS and avg_soshum > (avg_saintek + 5):
            insights.append(f"Profilmu adalah **Spesialis Soshum**. Rata-rata Soshum-mu ({avg_soshum:.2f}) jelas lebih menonjol daripada Saintek ({avg_saintek:.2f}). Jurusan rumpun Ekonomi, Bisnis, dan Hukum sangat cocok.")
        
        else:
            insights.append(f"Nilaimu cukup merata (Saintek: {avg_saintek:.2f}, Soshum: {avg_soshum:.2f}). Ini artinya pilihanmu sangat terbuka dan sebaiknya didasarkan pada tes minat & bakat.")
            
    # KASUS 5: Hanya input Saintek (Anak IPA)
    elif avg_saintek > 0 and avg_soshum == 0:
        if avg_saintek >= THRESHOLD_BAGUS:
            insights.append(f"Nilai Saintek-mu ({avg_saintek:.2f}) sangat kuat dan kompetitif. Ini modal besar untuk jurusan teknik atau kedokteran.")
        else:
             insights.append(f"Nilai Saintek-mu ({avg_saintek:.2f}) cukup baik. Terus tingkatkan untuk bersaing di jurusan favoritmu.")
    
    if scores['bahasa_inggris'] > 90:
        insights.append(f"**Bakat Unik:** Nilai Bahasa Inggris-mu ({scores['bahasa_inggris']}) luar biasa! Apapun jurusanmu, ini adalah 'senjata rahasia'. Pertimbangkan jurusan yang butuh banyak literatur Inggris (Hukum, Hub. Internasional, Kedokteran, TI).")
        
    if scores['matematika'] > 95:
         insights.append(f"**Bakat Unik:** Nilai Matematika-mu ({scores['matematika']}) sangat istimewa. Ini adalah indikator kuat untuk jurusan yang sangat analitis seperti Statistika, Matematika Murni, atau Aktuaria.")
    
    if not insights:
        return ["Masukkan nilai dari beberapa mata pelajaran untuk melihat insight."]

    return insights

def create_report_pdf(scores, insights):
    """
    Membuat file PDF dari hasil analisis dan mengembalikannya sebagai bytes.
    """
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- HEADER ---
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Laporan Analisis Premium", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "Cari Jurusan AI (by Kulonit)", ln=True, align="C")
    pdf.ln(10) # Kasih jarak
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Ringkasan Nilai Rapor Kamu", ln=True)
    pdf.set_font("Arial", "", 10)
    
    for mapel_key, mapel_label in MAPEL_INTI.items():
        nilai = scores.get(mapel_key, 0)
        if nilai > 0: 
            pdf.cell(0, 8, f"- {mapel_label}: {nilai}", ln=True)
    
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Insight & Analisis Kecenderungan Bidang", ln=True)
    pdf.set_font("Arial", "", 10)
    
    for insight in insights:
        pdf.multi_cell(0, 6, f"- {insight}", ln=True)
        pdf.ln(2)
        
    pdf.ln(10)
    
    # --- FOOTER ---
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, "Laporan ini digenerate oleh AI. Gunakan sebagai bahan pertimbangan.", ln=True, align="C")

    return bytes(pdf.output(dest='S'))
    
st.header("Fitur Premium: Analisis Rapor Mendalam 🎓")

if st.session_state.premium_unlocked:
    st.success("Fitur Premium Terbuka! Silakan masukkan nilaimu.")
    st.write("Dapatkan rekomendasi kedua yang 100% akurat berdasarkan nilai akademis-mu.")
    st.write("Masukkan nilai rapor terakhirmu di bawah ini (isi '0' jika tidak ada).")

    input_scores = {}

    with st.form("form_nilai_rapor"):
    
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Rumpun Saintek & Umum")
            input_scores['matematika'] = st.number_input(MAPEL_INTI['matematika'], min_value=0, max_value=100, value=0)
            input_scores['fisika'] = st.number_input(MAPEL_INTI['fisika'], min_value=0, max_value=100, value=0)
            input_scores['kimia'] = st.number_input(MAPEL_INTI['kimia'], min_value=0, max_value=100, value=0)
            input_scores['biologi'] = st.number_input(MAPEL_INTI['biologi'], min_value=0, max_value=100, value=0)

        with col2:
            st.subheader("Rumpun Soshum & Bahasa")
            input_scores['ekonomi'] = st.number_input(MAPEL_INTI['ekonomi'], min_value=0, max_value=100, value=0)
            input_scores['sosiologi'] = st.number_input(MAPEL_INTI['sosiologi'], min_value=0, max_value=100, value=0)
            input_scores['geografi'] = st.number_input(MAPEL_INTI['geografi'], min_value=0, max_value=100, value=0)
            input_scores['bahasa_indonesia'] = st.number_input(MAPEL_INTI['bahasa_indonesia'], min_value=0, max_value=100, value=0)
            input_scores['bahasa_inggris'] = st.number_input(MAPEL_INTI['bahasa_inggris'], min_value=0, max_value=100, value=0)
            
        submitted = st.form_submit_button("Analisis Nilaiku Sekarang!")

    if submitted:
        st.subheader("Hasil Analisis Kecenderungan Bidang:")
        
        list_of_insights = get_insight_from_scores(input_scores)
        
        total_score = sum(input_scores.values())
    
        if total_score == 0:
            st.warning("Kamu belum memasukkan nilai apapun. Coba masukkan beberapa nilaimu.")
        else:
            st.success("Berikut adalah insight berdasarkan nilai rapormu:")
            for insight in list_of_insights:
                st.markdown(f"- {insight}")
                
            st.markdown("---")

            pdf_bytes = create_report_pdf(input_scores, list_of_insights)
            
            # 2. Tampilkan tombol download
            st.download_button(
                label="Download Laporan PDF Lengkap 📄",
                data=pdf_bytes,
                file_name="Laporan_Analisis_CariJurusanAI.pdf",
                mime="application/pdf"
            )
        
else:
    st.warning("🔒 Fitur ini terkunci. Buka untuk mendapatkan analisis mendalam.")
    st.write(
        "Dapatkan analisis kecenderungan bidangmu berdasarkan nilai rapor. "
        "Ini akan membantumu memvalidasi pilihan jurusanmu dengan data akademis."
    )
    
    st.markdown("---")
    
    st.subheader("🚀 Cara Membuka Fitur Premium:")
    
    col_step1, col_step2, col_step3 = st.columns(3)
    
    with col_step1:
        st.info("**Langkah 1**\n\nKlik tombol Chat Admin di bawah.")
    with col_step2:
        st.info("**Langkah 2**\n\nLakukan pembayaran (Rp 19.000).")
    with col_step3:
        st.info("**Langkah 3**\n\nDapatkan **Kode Akses** via chat.")
        
    NOMOR_WA = "6288290449738" 
    
    PESAN_WA = "Halo%20Kak%20Aldi,%20saya%20mau%20beli%20akses%20premium%20Cari%20Jurusan%20AI%20dong!"
    LINK_WA = f"https://wa.me/{NOMOR_WA}?text={PESAN_WA}"
    
    # Tampilkan tombol besar
    st.link_button("👉 Beli Akses Premium (Chat Admin) 💬", url=LINK_WA, type="primary")
    
    st.caption("💡 **Harga Promo Launching:** Rp 19.000 (Sekali bayar, akses selamanya!)")
    
    st.markdown("---")

    st.subheader("🔑 Masukkan Kode Akses")
    st.write("Sudah punya kode dari Admin atau Kode Promo?")
    
    kode_input = st.text_input("Ketik kode di sini:")
    
    if st.button("Buka Fitur 🔓"):
        try:

            KODE_VALID_PREMIUM = st.secrets["KODE_PREMIUM"]
            KODE_VALID_PROMO = st.secrets["KODE_PROMO"]
            
            # Cek apakah input cocok dengan salah satu kode
            if kode_input == KODE_VALID_PREMIUM or kode_input == KODE_VALID_PROMO:
                st.session_state.premium_unlocked = True
                st.success("✅ Kode Benar! Selamat datang di fitur Premium.")
                st.balloons()

                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Kode salah. Cek kembali atau hubungi Admin.")
                
        except FileNotFoundError:
            # Error handling jika lupa setting secrets di dashboard
            st.error("⚠️ Konfigurasi server belum lengkap (Secrets not found). Hubungi developer.")
