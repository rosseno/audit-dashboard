import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Smart Audit Dashboard", page_icon="📊", layout="wide")

# Direktori Lokal untuk Menyimpan Berkas Audit
VAULT_DIR = "vault_dokumen"
os.makedirs(VAULT_DIR, exist_ok=True)

# Fungsi Dummy untuk Pengiriman ke Google Drive via Script Apps Script
def upload_to_drive_via_script(file_path):
    # Ganti dengan logika atau URL Apps Script yang sesuai
    # Mengembalikan True jika berhasil, False jika gagal
    try:
        # Contoh placeholder koneksi
        return True
    except Exception:
        return False

# Sidebar Navigasi Utama
st.sidebar.title("📌 Navigasi Menu")
menu_pilihan = st.sidebar.radio("Pilih Halaman:", ["Dashboard Audit", "Unggah Dokumen Audit (Auto-Drive)"])

# Dummy DataFrame untuk Contoh Tampilan (Sesuaikan dengan data asli Bapak jika ada)
# Pastikan variabel df_global dan df_filtered sudah terdefinisi di skrip Anda sebelumnya
if 'df_global' not in globals():
    data_dummy = {
        'No': [1, 2, 3],
        'Poin': ['A', 'B', 'C'],
        'Nama Entitas': ['Entitas 1', 'Entitas 2', 'Entitas 3'],
        'Tahun Audit': [2024, 2025, 2026],
        'Bidang': ['Operasional', 'Keuangan', 'IT'],
        'Ringkasan Kondisi & Akar Masalah (Root Cause)': ['Kondisi A', 'Kondisi B', 'Kondisi C'],
        'Rekomendasi': ['Rekomendasi A', 'Rekomendasi B', 'Rekomendasi C']
    }
    df_global = pd.DataFrame(data_dummy)
    df_filtered = df_global.copy()

# --- HALAMAN 1: DASHBOARD AUDIT ---
if menu_pilihan == "Dashboard Audit":
    st.subheader("📊 Grafik Tren Perbandingan Temuan Audit")
    
    if not df_global.empty and 'Tahun Audit' in df_global.columns:
        fig_trend = px.histogram(df_global, x='Tahun Audit', color='Bidang' if 'Bidang' in df_global.columns else None, barmode='group', template="plotly_dark")
        fig_trend.update_layout(height=420, font=dict(size=12))
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Kolom 'Tahun Audit' tidak ditemukan dalam data.")

    st.markdown("---")
    st.subheader("Detail Data Temuan & Rekomendasi")
    
    if not df_filtered.empty:
        # --- TABEL DISEDERHANAKAN (MENGHAPUS KOLOM YANG TIDAK PERLU) ---
        kolom_dibuang = ['No', 'Poin', 'Nama Entitas', 'Ringkasan Kondisi & Akar Masalah (Root Cause)']
        
        # Buang kolom jika ada di dataframe
        df_tampil = df_filtered.drop(columns=[col for col in kolom_dibuang if col in df_filtered.columns])
        
        # Tampilkan dataframe yang sudah disederhanakan
        st.dataframe(df_tampil, use_container_width=True, hide_index=True)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

# --- HALAMAN 2: UNGGAH DOKUMEN DENGAN GOOGLE DRIVE ---
if menu_pilihan == "Unggah Dokumen Audit (Auto-Drive)":
    st.subheader("📁 Unggah Dokumen Bukti, KKA, atau LHA")
    st.info("File yang diunggah akan otomatis tersimpan di server lokal dan langsung terkirim ke Google Drive via Web App.")

    doc_type = st.selectbox("Jenis Dokumen:", ["Tindak Lanjut (TL)", "Kertas Kerja Audit (KKA)", "Laporan Hasil Audit (LHA)"])
    uploaded_file = st.file_uploader("Pilih file (PDF, Word, Excel, Gambar):", type=["pdf", "docx", "xlsx", "png", "jpg"])

    if uploaded_file is not None:
        file_path = os.path.join(VAULT_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Mengirim file otomatis ke Google Drive..."):
            success = upload_to_drive_via_script(file_path)
            
            if success:
                st.success("Koneksi Google Drive Aktif dan Responsif!")
            else:
                st.error("Koneksi gagal. Periksa kembali deployment Google Apps Script Anda.")
