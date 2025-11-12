import streamlit as st
import pandas as pd
import joblib
import numpy as np
from fpdf import FPDF

st.set_page_config(
    page_title="Cari Jurusan AI",
    page_icon="🤖"
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

# --- END OF SIDEBAR CODE ---

# -------------------------------------------------------------------
# BAGIAN 2: UI UTAMA STREAMLIT
# -------------------------------------------------------------------

# Load model
model = joblib.load("model/model_cari_jurusan_2.pkl")

st.set_page_config(page_title="Cari Jurusan AI", layout="wide")

st.title("💡 Test Minat & Kemampuan")
st.write("Isi nilai atau minat kamu di bawah ini, lalu dapatkan jurusan yang paling cocok.")

# Bagi layout jadi dua kolom
col1, col2 = st.columns(2)

# ======================
# KIRI: INPUT & ALASAN
# ======================
with col1:
    st.subheader("Masukkan Skor atau Minat Kamu (0.0 - 1.0)")

    logika = st.slider("Kemampuan Logika", 0.0, 1.0, 0.5)
    verbal = st.slider("Kemampuan Verbal", 0.0, 1.0, 0.5)
    sosial = st.slider("Kemampuan Sosial", 0.0, 1.0, 0.5)
    kreatif = st.slider("Kreativitas", 0.0, 1.0, 0.5)
    analitis = st.slider("Kemampuan Analitis", 0.0, 1.0, 0.5)

    input_data = pd.DataFrame([{
        'logika': logika,
        'verbal': verbal,
        'sosial': sosial,
        'kreatif': kreatif,
        'analitis': analitis
    }])

    if st.button("Lihat Rekomendasi Jurusan"):
        hasil_pred = model.predict(input_data)[0]
        probabilitas = model.predict_proba(input_data)[0]
        daftar_jurusan = model.classes_

        st.success(f"🎯 Jurusan yang paling cocok untuk kamu: **{hasil_pred}**")

        # Bagian alasan di bawah
        feature_importance = model.feature_importances_
        fitur_df = pd.DataFrame({
            'Fitur': ['logika', 'verbal', 'sosial', 'kreatif', 'analitis'],
            'Pentingnya': feature_importance
        }).sort_values(by='Pentingnya', ascending=False)

        top_fitur = ", ".join(fitur_df.head(2)['Fitur'])
        st.info(f"Rekomendasi ini dipengaruhi terutama oleh: {top_fitur}")

        # Simpan variabel global untuk sisi kanan
        st.session_state['hasil_pred'] = hasil_pred
        st.session_state['probabilitas'] = probabilitas
        st.session_state['daftar_jurusan'] = daftar_jurusan
        st.session_state['fitur_df'] = fitur_df

# ======================
# KANAN: HASIL & TABEL
# ======================
with col2:
    if 'hasil_pred' in st.session_state:
        st.subheader("Persentase Kecocokan Tiap Jurusan")

        hasil_pred = st.session_state['hasil_pred']
        probabilitas = st.session_state['probabilitas']
        daftar_jurusan = st.session_state['daftar_jurusan']
        fitur_df = st.session_state['fitur_df']

        for jurusan, prob in zip(daftar_jurusan, probabilitas):
            persen = round(prob * 100, 2)
            st.write(f"{jurusan}: {persen}%")
            st.progress(float(prob))

        st.markdown("---")
        st.subheader("Detail Bobot Fitur")
        st.dataframe(fitur_df)