import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime
import os

st.set_page_config(
    page_title="Executive Audit Dashboard | PT Pelindo Solusi Maritim",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Ultimate + Animasi Bergerak Kanan ke Kiri
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    
    /* Animasi Teks Berjalan dari Kanan ke Kiri */
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    .merdeka-banner-container {
        background: linear-gradient(135deg, #991b1b 0%, #dc2626 50%, #b91c1c 100%);
        padding: 14px 0;
        border-radius: 10px;
        margin-bottom: 20px;
        overflow: hidden;
        white-space: nowrap;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
        border: 2px solid #fca5a5;
    }
    
    .merdeka-text {
        display: inline-block;
        color: #ffffff !important;
        font-weight: 800;
        font-size: 17px;
        letter-spacing: 1px;
        animation: marquee 15s linear infinite;
    }
    
    .header-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px 25px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .header-title { color: #ffffff; font-size: 22px; font-weight: 700; }
    .header-subtitle { color: #94a3b8; font-size: 13px; margin-top: 5px; }

    .stTextArea textarea { min-height: 100px !important; }

    @keyframes blink-animation {
        0% { opacity: 1; border-color: #ef4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.6); }
        50% { opacity: 0.4; border-color: #7f1d1d; box-shadow: 0 0 2px rgba(239, 68, 68, 0.1); }
        100% { opacity: 1; border-color: #ef4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.6); }
    }

    .alert-blink {
        background: rgba(239, 68, 68, 0.15);
        border: 2px solid #ef4444;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 15px;
        animation: blink-animation 1.5s infinite ease-in-out;
    }

    .kpi-row { display: flex; gap: 14px; width: 100%; margin-bottom: 20px; }
    .kpi-card {
        flex: 1;
        background: linear-gradient(145deg, #161b22 0%, #0d1117 100%);
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        transition: transform 0.2s ease;
    }
    .kpi-card:hover { transform: translateY(-3px); }
    .card-blue { border: 2px solid #3b82f6; }
    .card-green { border: 2px solid #10b981; }
    .card-yellow { border: 2px solid #f59e0b; }
    .card-red { border: 2px solid #ef4444; }
    .kpi-title { color: #94a3b8; font-size: 10.5px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
    .kpi-value { color: #ffffff; font-size: 28px; font-weight: 800; line-height: 1.1; }
</style>
""", unsafe_allow_html=True)

# --- BANNER KEMERDEKAAN BERGERAK (MARQUEE) ---
st.markdown("""
<div class="merdeka-banner-container">
    <div class="merdeka-text">
        ★ DIRGAHAYU REPUBLIK INDONESIA KE-81 — NUSANTARA BARU, INDONESIA MAJU (MERDEKA!) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ★ SEMANGAT INTEGRITAS, PATUH & PROFESIONAL UNTUK PELINDO SOLUSI MARITIM
    </div>
</div>
""", unsafe_allow_html=True)

# --- CONFIG DATA ---
EXCEL_FILE = "Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx"
EXCEL_KKA_FILE = "Database_Vault_KKA_AP.xlsx"
EXCEL_LHA_FILE = "Database_Vault_LHA_Word.xlsx"
VAULT_DIR = "audit_file_vault"

if not os.path.exists(VAULT_DIR):
    os.makedirs(VAULT_DIR)

@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE)

if 'df_master' not in st.session_state:
    st.session_state.df_master = load_data()

# Memuat data vault
if 'vault_kka' not in st.session_state:
    if os.path.exists(EXCEL_KKA_FILE):
        st.session_state.vault_kka = pd.read_excel(EXCEL_KKA_FILE).to_dict('records')
    else:
        st.session_state.vault_kka = []

if 'vault_lha' not in st.session_state:
    if os.path.exists(EXCEL_LHA_FILE):
        st.session_state.vault_lha = pd.read_excel(EXCEL_LHA_FILE).to_dict('records')
    else:
        st.session_state.vault_lha = []

df_master = st.session_state.df_master
col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]

# --- SIDEBAR & AKSES ---
st.sidebar.markdown("## Filter Control Panel")
periode_options = ["Semua Periode"] + sorted(list(df_master[col_periode].dropna().astype(str).unique()))
selected_periode = st.sidebar.selectbox("Periode Audit:", periode_options)
df_filtered = df_master[df_master[col_periode].astype(str) == str(selected_periode)] if selected_periode != "Semua Periode" else df_master.copy()

access_role = st.sidebar.selectbox("Pilih Peran / Jabatan:", ["Direktur Utama", "Admin SPI", "Auditee"])
df_base = df_filtered.copy() if access_role == "Admin SPI" else df_filtered.head(0)

# --- HEADER & TAB ---
st.markdown("""
<div class="header-banner">
    <div class="header-title">SMART AUDIT MONITORING DASHBOARD</div>
    <div class="header-subtitle">Internal Audit Unit — PT Pelindo Solusi Maritim</div>
</div>
""", unsafe_allow_html=True)

tab_dash, tab_vault_kka, tab_vault_lha = st.tabs(["📊 Dashboard", "📋 Vault KKA/AP", "📁 Vault LHA"])

with tab_dash:
    st.markdown("### Ringkasan Eksekutif")
    total_temuan = len(df_base)
    st.markdown(f"**Total Temuan:** {total_temuan}")
    st.dataframe(df_base, use_container_width=True)

with tab_vault_kka:
    st.markdown("### Vault KKA & AP")
    st.info("Penyimpanan file KKA/AP.")

with tab_vault_lha:
    st.markdown("### Vault LHA Word")
    st.info("Penyimpanan file LHA.")
