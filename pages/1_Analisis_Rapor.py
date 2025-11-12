import streamlit as st
import pandas as pd
import joblib
import numpy as np
from fpdf import FPDF

st.set_page_config(
    page_title="Analisis Rapor",
    page_icon="📄"
)

# --- Konfigurasi Sidebar ---

st.sidebar.title("Cari Jurusan AI 🤖")
st.sidebar.write("Temukan jurusan kuliah yang paling cocok untukmu.")

# Navigasi akan dibuat otomatis oleh Streamlit

st.sidebar.markdown("---") # Garis pemisah

# --- Promo Launching & Donasi ---
st.sidebar.subheader("🎉 Promo Launching (3 Hari!)")
st.sidebar.info("Fitur 'Analisis Rapor' GRATIS! Gunakan kode: FREETRIAL")

st.sidebar.subheader("Dukung Proyek Ini")
SAWERIA_URL = "https://saweria.co/aldifrasetiya"
st.sidebar.link_button("Donasi via Saweria ☕", url=SAWERIA_URL)

st.sidebar.image("img/barcode_saweria.png")

# -------------------------------------------------------------------
# BAGIAN 1: DEFINISI FUNGSI HELPER & KAMUS
# -------------------------------------------------------------------

if 'premium_unlocked' not in st.session_state:
    st.session_state.premium_unlocked = False
# --- BARU: Kamus untuk memetakan nama mapel ---
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
    # Tambahkan mapel inti lain jika perlu
}

def get_insight_from_scores(scores):

    insights = []

    # --- STEP 1: Hitung Rata-Rata Rumpun ---
    # (Kita harus hitung ini dulu)
    
    mapel_saintek = ['matematika', 'fisika', 'kimia', 'biologi']
    skor_saintek = [scores[mapel] for mapel in mapel_saintek if scores[mapel] > 0]
    avg_saintek = sum(skor_saintek) / len(skor_saintek) if len(skor_saintek) > 0 else 0
    
    mapel_soshum = ['ekonomi', 'sosiologi', 'geografi']
    skor_soshum = [scores[mapel] for mapel in mapel_soshum if scores[mapel] > 0]
    avg_soshum = sum(skor_soshum) / len(skor_soshum) if len(skor_soshum) > 0 else 0

    # --- STEP 2: Analisis Rumpun (Spesialis vs. Generalis) ---
    
    # Tentukan threshold 'bagus' (misal 80)
    THRESHOLD_BAGUS = 80
    
    # Cek apakah keduanya valid untuk dibandingkan
    if avg_saintek > 0 and avg_soshum > 0:
        # KASUS 1: Keduanya Tinggi (Generalis / All-Rounder)
        if avg_saintek >= THRESHOLD_BAGUS and avg_soshum >= THRESHOLD_BAGUS:
            insights.append(f"Kamu punya bakat seimbang! Nilai Saintek ({avg_saintek:.2f}) dan Soshum ({avg_soshum:.2f}) sama-sama kuat. Ini membuka banyak pilihan, dari Manajemen, Arsitektur, hingga Psikologi Industri.")
        
        # KASUS 2: Spesialis Saintek
        elif avg_saintek >= THRESHOLD_BAGUS and avg_saintek > (avg_soshum + 5): # +5 sbg 'margin'
            insights.append(f"Profilmu adalah **Spesialis Saintek**. Rata-rata Saintek-mu ({avg_saintek:.2f}) jelas lebih menonjol daripada Soshum ({avg_soshum:.2f}). Fokus pada jurusan rumpun Teknik & Sains Murni.")
            
        # KASUS 3: Spesialis Soshum
        elif avg_soshum >= THRESHOLD_BAGUS and avg_soshum > (avg_saintek + 5):
            insights.append(f"Profilmu adalah **Spesialis Soshum**. Rata-rata Soshum-mu ({avg_soshum:.2f}) jelas lebih menonjol daripada Saintek ({avg_saintek:.2f}). Jurusan rumpun Ekonomi, Bisnis, dan Hukum sangat cocok.")
        
        # KASUS 4: Rata-rata (Perlu eksplorasi)
        else:
            insights.append(f"Nilaimu cukup merata (Saintek: {avg_saintek:.2f}, Soshum: {avg_soshum:.2f}). Ini artinya pilihanmu sangat terbuka dan sebaiknya didasarkan pada tes minat & bakat.")
            
    # KASUS 5: Hanya input Saintek (Anak IPA)
    elif avg_saintek > 0 and avg_soshum == 0:
        if avg_saintek >= THRESHOLD_BAGUS:
            insights.append(f"Nilai Saintek-mu ({avg_saintek:.2f}) sangat kuat dan kompetitif. Ini modal besar untuk jurusan teknik atau kedokteran.")
        else:
             insights.append(f"Nilai Saintek-mu ({avg_saintek:.2f}) cukup baik. Terus tingkatkan untuk bersaing di jurusan favoritmu.")

    # (Bisa tambahkan KASUS 6: Hanya input Soshum)

    # --- STEP 3: Analisis "Spike" (Bakat Unik) ---
    # (Ini mencari nilai 'ajaib' yang mungkin beda dari rata-rata rumpunnya)
    
    if scores['bahasa_inggris'] > 90:
        insights.append(f"**Bakat Unik:** Nilai Bahasa Inggris-mu ({scores['bahasa_inggris']}) luar biasa! Apapun jurusanmu, ini adalah 'senjata rahasia'. Pertimbangkan jurusan yang butuh banyak literatur Inggris (Hukum, Hub. Internasional, Kedokteran, TI).")
        
    if scores['matematika'] > 95:
         insights.append(f"**Bakat Unik:** Nilai Matematika-mu ({scores['matematika']}) sangat istimewa. Ini adalah indikator kuat untuk jurusan yang sangat analitis seperti Statistika, Matematika Murni, atau Aktuaria.")
    
    if not insights:
        return ["Masukkan nilai dari beberapa mata pelajaran untuk melihat insight."]

    return insights

# --- BARU: Fungsi untuk membuat PDF ---
def create_report_pdf(scores, insights):
    """
    Membuat file PDF dari hasil analisis dan mengembalikannya sebagai bytes.
    """
    
    # Inisialisasi PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # --- HEADER ---
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Laporan Analisis Premium", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "Cari Jurusan AI (by Kulonit)", ln=True, align="C")
    pdf.ln(10) # Kasih jarak
    
    # --- BAGIAN 1: NILAI YANG DIINPUT ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "1. Ringkasan Nilai Rapor Kamu", ln=True)
    pdf.set_font("Arial", "", 10)
    
    for mapel_key, mapel_label in MAPEL_INTI.items():
        nilai = scores.get(mapel_key, 0)
        if nilai > 0: # Hanya tampilkan nilai yang diisi
            pdf.cell(0, 8, f"- {mapel_label}: {nilai}", ln=True)
    
    pdf.ln(5) # Kasih jarak
    
    # --- BAGIAN 2: INSIGHT AI ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "2. Insight & Analisis Kecenderungan Bidang", ln=True)
    pdf.set_font("Arial", "", 10)
    
    for insight in insights:
        # multi_cell() untuk text yang panjang/wrapping
        pdf.multi_cell(0, 6, f"- {insight}", ln=True)
        pdf.ln(2) # Jarak antar poin
        
    pdf.ln(10)
    
    # --- FOOTER ---
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, "Laporan ini digenerate oleh AI. Gunakan sebagai bahan pertimbangan.", ln=True, align="C")

    # --- KEMBALIKAN SEBAGAI BYTES ---
    # Ini penting agar bisa di-download via Streamlit
    return bytes(pdf.output(dest='S'))
    
    # # Skor Rumpun Saintek
    # skor_saintek = 0
    # mapel_saintek_count = 0
    # if scores['matematika'] > 0:
    #     skor_saintek += scores['matematika']
    #     mapel_saintek_count += 1
    # if scores['fisika'] > 0:
    #     skor_saintek += scores['fisika']
    #     mapel_saintek_count += 1
    # if scores['kimia'] > 0:
    #     skor_saintek += scores['kimia']
    #     mapel_saintek_count += 1
        
    # if mapel_saintek_count > 0:
    #     avg_saintek = skor_saintek / mapel_saintek_count
    #     if avg_saintek > 85:
    #         insights.append(f"Rata-rata Saintek (Mat, Fis, Kim) kamu sangat tinggi ({avg_saintek:.2f}). Kamu punya bakat kuat di jurusan teknik atau sains murni.")
    #     elif avg_saintek > 75:
    #         insights.append(f"Nilai Saintek-mu ({avg_saintek:.2f}) cukup baik dan kompetitif untuk jurusan teknik.")
            
    # # Skor Rumpun Soshum
    # skor_soshum = 0
    # mapel_soshum_count = 0
    # if scores['ekonomi'] > 0:
    #     skor_soshum += scores['ekonomi']
    #     mapel_soshum_count += 1
    # if scores['sosiologi'] > 0:
    #     skor_soshum += scores['sosiologi']
    #     mapel_soshum_count += 1
        
    # if mapel_soshum_count > 0:
    #     avg_soshum = skor_soshum / mapel_soshum_count
    #     if avg_soshum > 85:
    #         insights.append(f"Rata-rata Soshum (Eko, Sos) kamu sangat kuat ({avg_soshum:.2f}). Jurusan rumpun Ekonomi dan Bisnis sangat cocok untukmu.")

    
    # if scores['bahasa_inggris'] > 90:
    #     insights.append("Nilai Bahasa Inggris-mu luar biasa! Ini modal besar untuk jurusan Sastra Inggris, Hubungan Internasional, atau Jurnalisme.")

    # if not insights:
    #     return ["Masukkan nilai dari beberapa mata pelajaran untuk melihat insight."]

    # return insights

    st.markdown("---")
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
        
        # Panggil fungsi 'AI' rule-based kita
        list_of_insights = get_insight_from_scores(input_scores)
        
        # Cek apakah pengguna memasukkan nilai
        total_score = sum(input_scores.values())
    
        if total_score == 0:
            st.warning("Kamu belum memasukkan nilai apapun. Coba masukkan beberapa nilaimu.")
        else:
            st.success("Berikut adalah insight berdasarkan nilai rapormu:")
            for insight in list_of_insights:
                st.markdown(f"- {insight}")
                
            # (Di sini nanti kamu bisa tambahkan tombol "Cetak PDF" berbayarnya)
            st.markdown("---")
            # 1. Panggil fungsi generator PDF untuk membuat file-nya di memori
            pdf_bytes = create_report_pdf(input_scores, list_of_insights)
            
            # 2. Tampilkan tombol download
            st.download_button(
                label="Download Laporan PDF Lengkap 📄",
                data=pdf_bytes,
                file_name="Laporan_Analisis_CariJurusanAI.pdf",
                mime="application/pdf"
            )
        
else:
    
    # --- AREA TERKUNCI (UI BARU) ---
    # Jika masih 'terkunci', tampilkan 'paywall' (dinding pembayaran)
    
    st.warning("🔒 Fitur ini terkunci. Buka untuk mendapatkan analisis mendalam.")
    st.write(
        "Dapatkan analisis kecenderungan bidangmu berdasarkan nilai rapor. "
        "Ini akan membantumu memvalidasi pilihan jurusanmu dengan data akademis."
    )
    
    # --- INI ADALAH SIMULASI PEMBAYARAN ---
    st.markdown("---")
    st.subheader("Promo Launching (Gratis!)")
    st.success("🎉 **GRATIS 3 HARI!** Untuk merayakan launching, gunakan kode akses di bawah ini untuk free trial:")
    st.code("FREETRIAL", language=None)
    
    st.markdown("---")

    # --- Area Input Kode (Untuk Opsi 1 & 2) ---
    st.subheader("Masukkan Kode Akses")
    
    # Tentukan kode rahasiamu di sini
    KODE_PROMO = "FREETRIAL" 
    
    kode_akses = st.text_input("Kode Akses", label_visibility="collapsed")
    
    if kode_akses: # Jika pengguna memasukkan sesuatu
        if kode_akses == KODE_PROMO:
            st.session_state.premium_unlocked = True
            st.success("Kode valid! Fitur premium terbuka. Halaman akan me-refresh...")
            st.balloons()
            # Tunggu 2 detik agar pengguna bisa baca pesan, lalu refresh
            import time
            time.sleep(2)
            st.rerun()
        else:
            st.error("Kode akses salah. Silakan coba lagi.")