import streamlit as st
import pandas as pd
import os
import requests
from datetime import datetime

# --- KONFIGURASI & URL WEB APP ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzmvY3JE-NK_M-E1qlR_vQK59JEi5LqdV9ZHtIVaAk/exec"
VAULT_DIR = "audit_file_vault"
EXCEL_FILE = "Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx"

if not os.path.exists(VAULT_DIR):
    os.makedirs(VAULT_DIR)

# --- FUNGSI UPLOAD KE GOOGLE DRIVE VIA APPS SCRIPT ---
def upload_to_drive_via_script(file_path):
    try:
        with open(file_path, "rb") as f:
            file_content = f.read()
        params = {
            'filename': os.path.basename(file_path),
            'mimetype': 'application/octet-stream'
        }
        response = requests.post(WEB_APP_URL, params=params, data=file_content)
        return response.status_code == 200
    except Exception as e:
        return False

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Executive Audit Dashboard | PT Pelindo Solusi Maritim", page_icon="🛡️", layout="wide")

# Banner
st.markdown("""
<div style="background: linear-gradient(135deg, #991b1b 0%, #dc2626 50%); padding: 14px; border-radius: 8px; color: white; text-align: center; font-weight: 800; margin-bottom: 20px;">
    DIRGAHAYU REPUBLIK INDONESIA KE-81 — NUSANTARA BARU, INDONESIA MAJU!
</div>
""", unsafe_allow_html=True)

st.title("🛡️ SMART AUDIT MONITORING DASHBOARD")

# --- SIDEBAR NAVIGASI & PERAN ---
st.sidebar.title("Panel Navigasi")
access_role = st.sidebar.selectbox("Pilih Peran:", ["Auditee", "Admin SPI", "Direksi"])
chosen_unit = st.sidebar.selectbox("Pilih Unit / Bidang:", ["Semua Unit", "Operasional", "Teknik", "Keuangan", "SDM & Umum"])

menu = st.sidebar.radio("Pilih Menu:", [
    "Dashboard Utama", 
    "Unggah Dokumen (TL / KKA / LHA)", 
    "Database Temuan Audit", 
    "Status Koneksi Drive"
])

# --- KONTROL MENU ---
if menu == "Dashboard Utama":
    st.subheader(f"Selamat Datang, {access_role}")
    st.write("Sistem monitoring tindak lanjut temuan audit terintegrasi dengan Google Drive.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Temuan", "--", "Data Master")
    with col2:
        st.metric("Sudah Ditindak Lanjuti", "--", "Clear")
    with col3:
        st.metric("Status Koneksi Drive", "Aktif", "Web App Ready")

elif menu == "Unggah Dokumen (TL / KKA / LHA)":
    st.subheader("📤 Unggah Dokumen Bukti & Laporan Audit")
    st.info("Setiap file yang diunggah di sini akan otomatis tersimpan lokal dan terkirim langsung ke folder Google Drive.")

    upload_category = st.selectbox("Jenis Dokumen:", ["Tindak Lanjut (TL)", "Kertas Kerja Audit (KKA)", "Laporan Hasil Audit (LHA)"])
    uploaded_file = st.file_uploader("Pilih file (PDF, Word, Excel, Gambar):", type=["pdf", "docx", "xlsx", "png", "jpg"])

    if uploaded_file is not None:
        file_path = os.path.join(VAULT_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Proses Kirim ke Google Drive via Apps Script
        with st.spinner("Mengirim file otomatis ke Google Drive..."):
            success = upload_to_drive_via_script(file_path)
            
        if success:
            st.success(f"File **{uploaded_file.name}** berhasil diunggah dan masuk ke Google Drive!")
        else:
            st.warning(f"File tersimpan di server lokal, namun gagal terkirim ke Google Drive.")

elif menu == "Database Temuan Audit":
    st.subheader("📊 Database Temuan Audit")
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"File master database ({EXCEL_FILE}) belum ditemukan di direktori lokal.")

elif menu == "Status Koneksi Drive":
    st.subheader("🔗 Informasi Koneksi Google Drive")
    st.write("Aplikasi terhubung ke Google Drive menggunakan **Google Apps Script Web App**.")
    st.text(f"Target Endpoint: {WEB_APP_URL}")
    if st.button("Uji Koneksi Sekarang"):
        test_success = upload_to_drive_via_script(__file__) # uji kirim file python ini sendiri
        if test_success:
            st.success("Koneksi ke Google Drive Berhasil dan Responsif!")
        else:
            st.error("Koneksi gagal. Periksa kembali deployment Apps Script.")
