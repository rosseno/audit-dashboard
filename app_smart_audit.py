import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests
from datetime import datetime

# --- KONFIGURASI ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzmvY3JE-NK_M-E1qlR_vQK59JEi5LqdV9ZHtIVaAk/exec"
VAULT_DIR = "audit_file_vault"
EXCEL_FILE = "Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx"

if not os.path.exists(VAULT_DIR):
    os.makedirs(VAULT_DIR)

# --- FUNGSI UPLOAD KE GOOGLE DRIVE ---
def upload_to_drive_via_script(file_path):
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
        params = {'filename': os.path.basename(file_path), 'mimetype': 'application/octet-stream'}
        response = requests.post(WEB_APP_URL, params=params, data=file_content)
        return response.status_code == 200
    except:
        return False

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Executive Audit Dashboard | PT Pelindo Solusi Maritim", page_icon="🛡️", layout="wide")

# Banner
st.markdown("""
<div style="background: linear-gradient(135deg, #991b1b 0%, #dc2626 50%); padding: 14px; border-radius: 8px; color: white; text-align: center; font-weight: 800; margin-bottom: 20px;">
    DIRGAHAYU REPUBLIK INDONESIA KE-81 — NUSANTARA BARU, INDONESIA MAju!
</div>
""", unsafe_allow_html=True)

st.title("🛡️ SMART AUDIT MONITORING DASHBOARD")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame()

df_global = load_data()

# --- SIDEBAR FILTER & NAVIGASI ---
st.sidebar.title("Panel Navigasi & Filter")
access_role = st.sidebar.selectbox("Pilih Peran:", ["Auditee", "Admin SPI", "Direksi"])
chosen_unit = st.sidebar.selectbox("Pilih Unit / Bidang:", ["Semua Unit", "Operasional", "Teknik", "Keuangan", "SDM & Umum"])
periode_audit = st.sidebar.selectbox("Periode Audit:", ["Semua Periode", "2024", "2025", "2026"])

menu = st.sidebar.radio("Pilih Menu:", [
    "Dashboard Utama & Grafik", 
    "Unggah Dokumen (TL / KKA / LHA)", 
    "Database Temuan Audit", 
    "Status Koneksi Drive"
])

# --- LOGIKA FILTER DATA ---
df_filtered = df_global.copy()
if not df_filtered.empty:
    if chosen_unit != "Semua Unit" and 'Bidang' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Bidang'].str.contains(chosen_unit, case=False, na=False)]

# --- KONTROL MENU UTAMA ---
if menu == "Dashboard Utama & Grafik":
    st.subheader(f"📊 Ringkasan Eksekutif - {access_role}")
    
    # Kartu Metrik (Cards)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Temuan", len(df_filtered) if not df_filtered.empty else 0)
    with col2:
        st.metric("Status Dokumen Drive", "Terhubung", "Web App")
    with col3:
        st.metric("Periode Aktif", periode_audit)
    with col4:
        st.metric("Unit Dipilih", chosen_unit)
    
    st.markdown("---")
    
    # Grafik Interaktif (Chart)
    if not df_filtered.empty and 'Bidang' in df_filtered.columns:
        st.subheader("📈 Statistik Temuan Berdasarkan Bidang")
        fig = px.histogram(df_filtered, x='Bidang', color='Bidang' if 'Tingkat' not in df_filtered.columns else 'Tingkat', 
                           title="Distribusi Temuan Audit", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Grafik akan otomatis muncul saat data master tersedia.")

elif menu == "Unggah Dokumen (TL / KKA / LHA)":
    st.subheader("📤 Unggah Dokumen Bukti & Laporan Audit")
    st.info("File yang diunggah akan otomatis disimpan secara lokal dan dikirim langsung ke Google Drive.")

    upload_category = st.selectbox("Jenis Dokumen:", ["Tindak Lanjut (TL)", "Kertas Kerja Audit (KKA)", "Laporan Hasil Audit (LHA)"])
    uploaded_file = st.file_uploader("Pilih file (PDF, Word, Excel, Gambar):", type=["pdf", "docx", "xlsx", "png", "jpg"])

    if uploaded_file is not None:
        file_path = os.path.join(VAULT_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Mengirim file otomatis ke Google Drive..."):
            success = upload_to_drive_via_script(file_path)
            
        if success:
            st.success(f"File **{uploaded_file.name}** berhasil diunggah dan masuk ke Google Drive!")
        else:
            st.warning(f"File tersimpan di server lokal, namun gagal terkirim ke Google Drive.")

elif menu == "Database Temuan Audit":
    st.subheader("📋 Tabel Database Temuan Audit")
    if not df_filtered.empty:
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.warning(f"File master database ({EXCEL_FILE}) belum ditemukan atau kosong.")

elif menu == "Status Koneksi Drive":
    st.subheader("🔗 Informasi Koneksi Google Drive")
    st.write("Aplikasi menggunakan **Google Apps Script Web App** untuk integrasi tanpa batas.")
    st.text(f"Endpoint: {WEB_APP_URL}")
    if st.button("Uji Koneksi Sekarang"):
        if upload_to_drive_via_script(__file__):
            st.success("Koneksi Google Drive Beraktifitas Normal!")
        else:
            st.error("Koneksi gagal. Periksa kembali deployment Apps Script.")
