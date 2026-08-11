import streamlit as st
import os
import requests

# --- KONFIGURASI ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzmvY3JE-NK_M-E1qlR_vQK59JEi5LqdV9ZHtIVaAk/exec"
VAULT_DIR = "audit_file_vault"

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
    except Exception as e:
        return False

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Executive Audit Dashboard", layout="wide")

# Banner Merdeka
st.markdown("""
<div style="background: #dc2626; color: white; padding: 15px; text-align: center; font-weight: bold; border-radius: 8px; margin-bottom: 20px;">
    DIRGAHAYU REPUBLIK INDONESIA KE-81 — NUSANTARA BARU, INDONESIA MAJU!
</div>
""", unsafe_allow_html=True)

st.title("🛡️ SMART AUDIT MONITORING DASHBOARD")

# Sidebar Navigasi
st.sidebar.title("Navigasi")
menu = st.sidebar.selectbox("Pilih Menu:", ["Dashboard Utama", "Unggah Dokumen Audit"])

if menu == "Dashboard Utama":
    st.subheader("Selamat Datang di Executive Audit Dashboard")
    st.write("Sistem monitoring audit terintegrasi dengan Google Drive.")
    st.metric("Status Koneksi Drive", "Terhubung via Web App", "Aktif")

elif menu == "Unggah Dokumen Audit":
    st.subheader("📤 Unggah File Bukti / KKA / LHA")
    
    uploaded_file = st.file_uploader("Pilih dokumen untuk diunggah:", type=["pdf", "docx", "xlsx", "png", "jpg"])
    
    if uploaded_file is not None:
        file_path = os.path.join(VAULT_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Proses Kirim ke Google Drive
        with st.spinner("Sedang mengirim file otomatis ke Google Drive..."):
            success = upload_to_drive_via_script(file_path)
            
        if success:
            st.success(f"File **{uploaded_file.name}** berhasil disimpan lokal dan sukses terunggah ke Google Drive!")
        else:
            st.warning(f"File **{uploaded_file.name}** tersimpan di lokal, namun gagal terkirim ke Google Drive.")
