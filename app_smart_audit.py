import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests
from datetime import datetime

# --- KONFIGURASI WEB APP GOOGLE DRIVE ---
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

# --- CUSTOM CSS UNTUK KARTU (CARDS) & TAMPILAN ---
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    .metric-value {
        color: #f8fafc;
        font-size: 24px;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# Banner Merdeka
st.markdown("""
<div style="background: linear-gradient(135deg, #991b1b 0%, #dc2626 50%); padding: 12px; border-radius: 8px; color: white; text-align: center; font-weight: 800; margin-bottom: 15px;">
    DIRGAHAYU REPUBLIK INDONESIA KE-81 — NUSANTARA BARU, INDONESIA MAJU!
</div>
""", unsafe_allow_html=True)
# --- BANNER PERINGATAN MERAH PEKAT & FONT KUNING MENYALA (DIJAMIN TEMBUS) ---
if 'jml_bd' in locals() and jml_bd > 0:
    st.markdown(
        f"""
        <style>
        @keyframes scary-blink {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
            100% {{ opacity: 1; }}
        }}
        .my-scary-banner {{
            background-color: #8b0000;
            padding: 16px 20px;
            border-radius: 8px;
            text-align: center;
            animation: scary-blink 1s infinite ease-in-out;
            margin-bottom: 20px;
            border: 3px solid #ffcc00;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.8);
        }}
        </style>
        <div class="my-scary-banner">
            <span style="color: #ffff00 !important; font-weight: 900 !important; font-size: 19px !important; letter-spacing: 0.5px;">
                🚨 PERINGATAN KERAS: Terdapat {jml_bd} Temuan dengan Status BD (Belum Ditindaklanjuti) yang Memerlukan Perhatian & Tindak Lanjut Segera! 🚨
            </span>
        </div>
        
        <audio autoplay style="display:none;">
            <source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg">
        </audio>
        """,
        unsafe_allow_html=True
    )
st.title("🛡️ SMART AUDIT MONITORING DASHBOARD")

# --- LOAD DATA EXCEL ---
@st.cache_data
def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame()

df_global = load_data()

# --- SIDEBAR FILTER & MENU ---
st.sidebar.title("Panel Navigasi & Filter")
access_role = st.sidebar.selectbox("Pilih Peran:", ["Auditee", "Admin SPI", "Direksi"])
chosen_unit = st.sidebar.selectbox("Pilih Unit / Bidang:", ["Semua Unit", "Bidang Operasi Dan Teknik", "Bidang SDM", "Bidang Pengadaan", "Bidang Pemasaran", "Bidang Keuangan", "Bidang HSSE"])

# Filter Periode / Tahun Audit
list_periode = ["Semua Periode"]
if not df_global.empty and 'Tahun Audit' in df_global.columns:
    tahun_unik = sorted(df_global['Tahun Audit'].dropna().unique().astype(str).tolist())
    list_periode.extend(tahun_unik)
selected_periode = st.sidebar.selectbox("Pilih Periode (Tahun):", list_periode)

menu_pilihan = st.sidebar.radio("Menu Utama:", [
    "Dashboard Visualisasi & Tabel", 
    "Unggah Dokumen Audit (Auto-Drive)", 
    "Status Koneksi Drive"
])

# --- LOGIKA FILTER DATA ---
# --- LOGIKA FILTER DATA ---
df_filtered = df_global.copy()
if not df_filtered.empty:
    if chosen_unit != "Semua Unit" and 'Bidang' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Bidang'].str.contains(chosen_unit, case=False, na=False)]
    if selected_periode != "Semua Periode" and 'Tahun Audit' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Tahun Audit'].astype(str) == selected_periode]
    if 'filter_status' not in st.session_state:
       st.session_state.filter_status = "Semua"       
    if st.session_state.filter_status != "Semua" and 'Status' in df_filtered.columns:
        df_filtered = df_filtered[df_filtered['Status'].str.contains(st.session_state.filter_status, case=False, na=False)]
    
   

# --- HALAMAN 1: DASHBOARD UTAMA ---
if menu_pilihan == "Dashboard Visualisasi & Tabel":
    
    # KARTU METRIK (CARDS) RAPI & ELEGAN
    total_temuan = len(df_filtered) if not df_filtered.empty else 0
    jml_bd = len(df_filtered[df_filtered['Status'].str.contains('BD', case=False, na=False)]) if not df_filtered.empty and 'Status' in df_filtered.columns else 0
    jml_eval = len(df_filtered[df_filtered['Status'].str.contains('EVAL', case=False, na=False)]) if not df_filtered.empty and 'Status' in df_filtered.columns else 0
    jml_sls = len(df_filtered[df_filtered['Status'].str.contains('SLS', case=False, na=False)]) if not df_filtered.empty and 'Status' in df_filtered.columns else 0
# --- BANNER PERINGATAN BLINKING STATUS BD ---
if 'jml_bd' in locals() and jml_bd > 0:
    st.markdown(
        f"""
        <style>
        @keyframes blink-animation {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
            100% {{ opacity: 1; }}
        }}
        .blinking-banner {{
            background-color: #ff4b4b;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            font-size: 16px;
            animation: blink-animation 1.5s infinite;
            margin-bottom: 20px;
        }}
        </style>
        <div class="blinking-banner">
            🚨 PERINGATAN: Terdapat {jml_bd} Temuan dengan Status BD (Belum Ditindaklanjuti) yang memerlukan perhatian segera!
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3, col4 = st.columns(4)
    with col1:
            if st.button(f"TOTAL TEMUAN\n\n{total_temuan}", use_container_width=True):
                st.session_state.filter_status = "Semua"
                st.rerun()
    with col2:
            if st.button(f"STATUS BD\n\n{jml_bd}", use_container_width=True):
                st.session_state.filter_status = "BD"
                st.rerun()
    with col3:
            if st.button(f"STATUS EVAL\n\n{jml_eval}", use_container_width=True, key="btn_eval"):
                st.session_state.filter_status = "EVAL"
                st.rerun()
    with col4:
            if st.button(f"STATUS SLS\n\n{jml_sls}", use_container_width=True, key="btn_sls"):
                st.session_state.filter_status = "SLS"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Visualisasi Grafik Progres & Sebaran", "Grafik Tren Perbandingan Antar Tahun"])
    
    with tab1:
        col_chart1, col_chart2 = st.columns([2, 1])
        
        with col_chart1:
            st.subheader("Progres Status per Bidang")
            if not df_filtered.empty and 'Bidang' in df_filtered.columns and 'Status' in df_filtered.columns:
                fig_bar = px.histogram(df_filtered, y='Bidang', color='Status', barmode='stack', template="plotly_dark")
                # Mengatur tinggi agar bar tidak terlalu raksasa, serta memperbesar ukuran font label
                fig_bar.update_layout(
                    height=400, 
                    xaxis_title="Jumlah", 
                    yaxis_title="Bidang", 
                    legend_title="Status",
                    font=dict(size=12)
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Data grafik bar belum tersedia pada filter ini.")
                
        with col_chart2:
            st.subheader("Proporsi Status")
            if not df_filtered.empty and 'Status' in df_filtered.columns:
                fig_pie = px.pie(df_filtered, names='Status', hole=0.5, template="plotly_dark")
                fig_pie.update_layout(height=400, font=dict(size=12))
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("Data proporsi belum tersedia.")

    with tab2:
        st.subheader("Grafik Tren Perbandingan Antar Tahun Temuan Audit")
        if not df_global.empty and 'Tahun Audit' in df_global.columns:
            fig_trend = px.histogram(df_global, x='Tahun Audit', color='Bidang' if 'Bidang' in df_global.columns else None, barmode='group', template="plotly_dark")
            fig_trend.update_layout(height=420, font=dict(size=12))
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("Kolom 'Tahun Audit' tidak ditemukan dalam data.")

    st.markdown("---")
    st.subheader("Detail Data Temuan & Rekomendasi")
    if not df_filtered.empty:
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")

# --- HALAMAN 2: UNGGAH DOKUMEN DENGAN GOOGLE DRIVE ---
elif menu_pilihan == "Unggah Dokumen Audit (Auto-Drive)":
    st.subheader("📤 Unggah Dokumen Bukti, KKA, atau LHA")
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
            st.success(f"File **{uploaded_file.name}** berhasil diunggah lokal dan sukses masuk ke Google Drive!")
        else:
            st.warning(f"File tersimpan di lokal, namun gagal terkirim ke Google Drive.")

# --- HALAMAN 3: STATUS KONEKSI ---
elif menu_pilihan == "Status Koneksi Drive":
    st.subheader("🔗 Status Koneksi Google Drive Apps Script")
    st.write(f"Endpoint URL: `{WEB_APP_URL}`")
    if st.button("Uji Koneksi Sekarang"):
        if upload_to_drive_via_script(__file__):
            st.success("Koneksi Google Drive Aktif dan Responsif!")
        else:
            st.error("Koneksi gagal. Periksa kembali deployment Google Apps Script Anda.")
