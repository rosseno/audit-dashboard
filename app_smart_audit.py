import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(
    page_title="Executive Audit Dashboard - PT Pelindo Solusi Maritim",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk Kartu KPI Interaktif
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
    .header-title { color: #ffffff; font-size: 24px; font-weight: 700; margin-bottom: 3px; }
    
    div.stButton > button {
        width: 100% !important;
        height: 85px !important;
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 8px !important;
        text-align: left !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        transition: 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        border-color: #3b82f6 !important;
        background-color: #253348 !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        return pd.read_excel("Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx")
    except:
        return pd.read_excel("Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx")

df_master = load_data()
PIN_ADMIN = "1234"

# --- SIDEBAR: PENGATURAN HAK AKSES FLEKSIBEL ---
st.sidebar.markdown("## 🔐 Hak Akses Pengguna")
access_mode = st.sidebar.radio(
    "Pilih Mode Akses:", 
    ["Auditee (Per Bidang)", "Direksi / Manajemen (Semua Bidang)", "Admin SPI (Full Access)"]
)

# Inisialisasi session state login admin
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

list_bidang_available = sorted(list(df_master["Bidang"].dropna().astype(str).unique())) if "Bidang" in df_master.columns else []

if access_mode == "Admin SPI (Full Access)":
    if not st.session_state.admin_logged_in:
        entered_pin = st.sidebar.text_input("Masukkan PIN Admin:", type="password")
        if entered_pin == PIN_ADMIN:
            st.session_state.admin_logged_in = True
            st.sidebar.success("Login Admin Berhasil!")
            st.rerun()
        elif entered_pin:
            st.sidebar.error("PIN Salah!")
    else:
        st.sidebar.success("Status: Admin Aktif 🔓")
        if st.sidebar.button("Logout Admin"):
            st.session_state.admin_logged_in = False
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("## 🎯 Filter Control Panel")

col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]
selected_periode = st.sidebar.selectbox("📅 Periode Audit:", ["Semua Periode"] + sorted(list(df_master[col_periode].dropna().astype(str).unique())))

df_filtered_periode = df_master[df_master[col_periode].astype(str) == str(selected_periode)] if selected_periode != "Semua Periode" else df_master.copy()

col_bidang = "Bidang" if "Bidang" in df_master.columns else df_master.columns[5]

# --- LOGIKA PEMBATASAN BERDASARKAN PILIHAN FLEKSIBEL ---
if access_mode == "Auditee (Per Bidang)":
    st.sidebar.info("ℹ️ Mode Auditee: Silakan pilih bidang unit kerja Anda.")
    selected_bidang = st.sidebar.selectbox("📂 Pilih Bidang Anda:", list_bidang_available)
    df_base = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(selected_bidang)]

elif access_mode == "Direksi / Manajemen (Semua Bidang)":
    st.sidebar.info("ℹ️ Mode Direksi: Menampilkan ringkasan seluruh bidang.")
    # Direksi bisa melihat "Semua Bidang" secara default atau memfilter bidang tertentu jika ingin
    selected_bidang = st.sidebar.selectbox("📂 Pilih Bidang / Tinjau Semua:", ["Semua Bidang"] + list_bidang_available)
    df_base = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(selected_bidang)] if selected_bidang != "Semua Bidang" else df_filtered_periode.copy()

else:  # Admin SPI
    if st.session_state.admin_logged_in:
        selected_bidang = st.sidebar.selectbox("📂 Bidang Workgroup:", ["Semua Bidang"] + list_bidang_available)
        df_base = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(selected_bidang)] if selected_bidang != "Semua Bidang" else df_filtered_periode.copy()
    else:
        st.sidebar.warning("⚠️ Masukkan PIN Admin di atas untuk akses penuh.")
        selected_bidang = list_bidang_available[0] if list_bidang_available else "Semua Bidang"
        df_base = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(selected_bidang)]

# Header
header_label = f"DEPARTEMEN {selected_bidang.upper()}" if selected_bidang != "Semua Bidang" else "SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM"
st.markdown(f"""<div class="header-banner"><div class="header-title">📊 {header_label}</div></div>""", unsafe_allow_html=True)

# KPI Interaktif (Tombol Kartu)
st.markdown("### 📈 Ringkasan Eksekutif KPI (Klik Kartu untuk Filter Status)")
if 'filter_status' not in st.session_state: 
    st.session_state.filter_status = "Semua"

col_status = "Status" if "Status" in df_base.columns else "Status_TL"
total_temuan = len(df_base)
selesai = len(df_base[df_base[col_status].str.contains("Selesai|SLS", case=False, na=False)])
evaluasi = len(df_base[df_base[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)])
overdue = len(df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)])

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button(f"TOTAL TEMUAN\n\n{total_temuan} (Semua)", key="b_all"):
        st.session_state.filter_status = "Semua"
with c2:
    if st.button(f"POIN REKOMENDASI\n\n{total_temuan} (Total)", key="b_rec"):
        st.session_state.filter_status = "Semua"
with c3:
    if st.button(f"SELESAI (SLS)\n\n{selesai} Selesai", key="b_sls"):
        st.session_state.filter_status = "Selesai"
with c4:
    if st.button(f"EVALUASI (EVAL)\n\n{evaluasi} Proses", key="b_eval"):
        st.session_state.filter_status = "Evaluasi"
with c5:
    if st.button(f"OVERDUE (BD)\n\n{overdue} Belum TL", key="b_bd"):
        st.session_state.filter_status = "Overdue"

# TERAPKAN FILTER STATUS KE DATA UTAMA
df_filtered = df_base.copy()
if st.session_state.filter_status == "Selesai":
    df_filtered = df_base[df_base[col_status].str.contains("Selesai|SLS", case=False, na=False)]
elif st.session_state.filter_status == "Evaluasi":
    df_filtered = df_base[df_base[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)]
elif st.session_state.filter_status == "Overdue":
    df_filtered = df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)]

st.markdown(f"<p style='color: #3b82f6; font-size: 12px; margin-top: -10px;'>Status Filter Aktif: <b>{st.session_state.filter_status}</b></p>", unsafe_allow_html=True)
st.markdown("---")

# Konsistensi Warna Baku untuk Setiap Status
color_map = {
    'Selesai (SLS)': '#00BCD4',   
    'Selesai': '#00BCD4',
    'SLS': '#00BCD4',
    'Evaluasi (EVAL)': '#FFCA28', 
    'Evaluasi': '#FFCA28',
    'EVAL': '#FFCA28',
    'Overdue (BD)': '#FF7043',    
    'Overdue': '#FF7043',
    'BD': '#FF7043',
    'Belum TL': '#FF7043'
}

# Chart & Data
col_chart_bar, col_chart_pie = st.columns([3, 1.5])

with col_chart_bar:
    df_chart = df_filtered.groupby([col_bidang, col_status]).size().reset_index(name='Jumlah')
    fig_bar = px.bar(
        df_chart, x='Jumlah', y=col_bidang, color=col_status, orientation='h', barmode='stack', 
        title="Progres Status per Bidang", color_discrete_map=color_map, template='plotly_dark'
    )
    fig_bar.update_layout(height=300, margin=dict(l=0, r=10, t=30, b=0))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart_pie:
    df_pie = df_filtered.groupby(col_status).size().reset_index(name='Total')
    fig_pie = px.pie(
        df_pie, values='Total', names=col_status, hole=0.6, 
        title="Proporsi Status", color=col_status, color_discrete_map=color_map, template='plotly_dark'
    )
    fig_pie.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("### 📋 Detail Data")
st.dataframe(df_filtered, use_container_width=True)
