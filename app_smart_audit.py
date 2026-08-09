import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime

st.set_page_config(
    page_title="Executive Audit Dashboard - PT Pelindo Solusi Maritim",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Ultimate untuk Card KPI Proporsional, Neon Glow, & Styling Global
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .header-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .header-title { color: #ffffff; font-size: 22px; font-weight: 700; }
    .header-subtitle { color: #94a3b8; font-size: 13px; margin-top: 5px; }

    /* Container Card KPI agar rapat berjejer rapi & proporsional */
    .kpi-row {
        display: flex;
        gap: 14px;
        width: 100%;
        margin-bottom: 20px;
    }

    /* Desain Card 3D Hidup dengan Proporsi Ukuran Pas & Estetik */
    .kpi-card {
        flex: 1;
        background: linear-gradient(145deg, #161b22 0%, #0d1117 100%);
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        transition: transform 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-3px);
    }

    /* Siluet Garis Warna Neon Spesifik per Card */
    .card-blue { border: 2px solid #3b82f6; box-shadow: 0 0 12px rgba(59, 130, 246, 0.35); }
    .card-purple { border: 2px solid #8b5cf6; box-shadow: 0 0 12px rgba(139, 92, 246, 0.35); }
    .card-green { border: 2px solid #10b981; box-shadow: 0 0 12px rgba(16, 185, 129, 0.35); }
    .card-yellow { border: 2px solid #f59e0b; box-shadow: 0 0 12px rgba(245, 158, 11, 0.35); }
    .card-red { border: 2px solid #ef4444; box-shadow: 0 0 12px rgba(239, 68, 68, 0.35); }

    .kpi-title {
        color: #94a3b8;
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 2px;
        line-height: 1.1;
    }

    .kpi-desc {
        color: #cbd5e1;
        font-size: 11.5px;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        return pd.read_excel("Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx")
    except:
        return pd.read_excel("Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx")

if 'df_master' not in st.session_state:
    st.session_state.df_master = load_data()

df_master = st.session_state.df_master
PIN_ADMIN = "1234"  # <-- PIN Admin SPI

col_bidang = "Bidang" if "Bidang" in df_master.columns else df_master.columns[5]
col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]
col_status = "Status" if "Status" in df_master.columns else "Status_TL"

if "Catatan_Auditor" not in df_master.columns:
    df_master["Catatan_Auditor"] = "-"

# --- SIDEBAR: PENGATURAN HAK AKSES & PERIODE ---
st.sidebar.markdown("## Filter Control Panel")
selected_periode = st.sidebar.selectbox("Periode Audit:", ["Semua Periode"] + sorted(list(df_master[col_periode].dropna().astype(str).unique())))

df_filtered_periode = df_master[df_master[col_periode].astype(str) == str(selected_periode)] if selected_periode != "Semua Periode" else df_master.copy()
current_available_bidang = sorted(list(df_filtered_periode[col_bidang].dropna().astype(str).unique()))

st.sidebar.markdown("---")
st.sidebar.markdown("## Hak Akses & Portofolio")
access_role = st.sidebar.selectbox(
    "Pilih Peran / Jabatan:",
    [
        "Direktur Utama",
        "Direktur Operasi & Komersial",
        "Direktur Keuangan, SDM, HSSE, IT, PAP, Umum & RT",
        "Auditee",
        "Admin SPI"
    ]
)

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

# --- LOGIKA INPUT PIN ADMIN ---
if access_role == "Admin SPI":
    if not st.session_state.admin_logged_in:
        entered_pin = st.sidebar.text_input("Masukkan PIN Admin:", type="password")
        if entered_pin == PIN_ADMIN:
            st.session_state.admin_logged_in = True
            st.sidebar.success("Login Admin Berhasil!")
            st.rerun()
        elif entered_pin:
            st.sidebar.error("PIN Salah!")
    else:
        st.sidebar.success("Status: Admin Aktif")
        if st.sidebar.button("Logout Admin"):
            st.session_state.admin_logged_in = False
            st.rerun()

# --- PEMETAAN DATA BERDASARKAN PERAN ---
if access_role == "Direktur Utama":
    sub_choice = st.sidebar.selectbox("Tinjau Cakupan:", ["Semua Bidang (Keseluruhan)", "SPI", "Hukum", "Sekper", "Pengadaan"])
    if sub_choice == "Semua Bidang (Keseluruhan)":
        df_base = df_filtered_periode.copy()
    else:
        df_base = df_filtered_periode[df_filtered_periode[col_bidang].str.contains(sub_choice, case=False, na=False)]

elif access_role == "Direktur Operasi & Komersial":
    ops_choices = ["Operasi", "Teknik", "Pemasaran"]
    df_base = df_filtered_periode[df_filtered_periode[col_bidang].str.contains('|'.join(ops_choices), case=False, na=False)]

elif access_role == "Direktur Keuangan, SDM, HSSE, IT, PAP, Umum & RT":
    fin_choices = ["Keuangan", "SDM", "HSSE", "IT", "PAP", "Umum", "Rumah Tangga"]
    df_base = df_filtered_periode[df_filtered_periode[col_bidang].str.contains('|'.join(fin_choices), case=False, na=False)]

elif access_role == "Auditee":
    chosen_unit = st.sidebar.selectbox("Pilih Bidang:", current_available_bidang if current_available_bidang else ["Tidak ada data"])
    df_base = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(chosen_unit)]

else:  # Admin SPI
    if st.session_state.admin_logged_in:
        chosen_admin_filter = st.sidebar.selectbox("Filter Bidang:", ["Semua Bidang"] + current_available_bidang)
        if chosen_admin_filter == "Semua Bidang":
            df_base = df_filtered_periode.copy()
        else:
            df_base = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(chosen_admin_filter)]
    else:
        df_base = df_filtered_periode.head(0)

# --- MENAMPILKAN KEDUA LOGO BERJEJER DI POJOK KANAN ATAS ---
col_space, col_logo1, col_logo2 = st.columns([5, 1.5, 1.5])

with col_space:
    st.empty()

with col_logo1:
    # Memanggil file logo Danantara
    st.image("logo.png", width=140)

with col_logo2:
    # Memanggil file logo Pelindo (Pastikan file gambar Pelindo dinamai "logo_pelindo.png" di folder yang sama)
    st.image("logo_pelindo.png", width=140)

# Header Banner Judul Aplikasi
st.markdown("""
<div class="header-banner">
    <div class="header-title">SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM</div>
    <div class="header-subtitle">Sistem Pemantauan Granular Hasil Audit Kepatuhan & Performansi — Internal Audit Unit</div>
</div>
""", unsafe_allow_html=True)
