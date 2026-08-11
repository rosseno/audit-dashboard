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

# Custom CSS Ultimate + Banner HUT RI Besar & Bergerak
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    .merdeka-banner-container {
        background: linear-gradient(135deg, #991b1b 0%, #dc2626 50%, #b91c1c 100%);
        padding: 14px 0;
        border-radius: 8px;
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
        font-size: 18px;
        letter-spacing: 1px;
        animation: marquee 18s linear infinite;
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
col_bidang = "Bidang" if "Bidang" in df_master.columns else df_master.columns[5]
col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]
col_status = "Status" if "Status" in df_master.columns else "Status_TL"

PIN_ADMIN = "1234"

# --- SIDEBAR & FILTER PERIODE ---
st.sidebar.markdown("## Filter Control Panel")
existing_periods = sorted(list(df_master[col_periode].dropna().astype(str).unique()))
if "2026" not in existing_periods:
    existing_periods.append("2026")

periode_options = ["Semua Periode"] + existing_periods
selected_periode = st.sidebar.selectbox("Periode Audit:", periode_options)

if selected_periode == "2026":
    df_filtered_periode = df_master.head(0).copy()
else:
    df_filtered_periode = df_master[df_master[col_periode].astype(str) == str(selected_periode)] if selected_periode != "Semua Periode" else df_master.copy()

current_available_bidang = sorted(list(df_filtered_periode[col_bidang].dropna().astype(str).unique())) if not df_filtered_periode.empty else sorted(list(df_master[col_bidang].dropna().astype(str).unique()))

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

# Logika Akses Berdasarkan Peran
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

else:
    if st.session_state.admin_logged_in:
        chosen_admin_filter = st.sidebar.selectbox("Filter Bidang:", ["Semua Bidang"] + current_available_bidang)
        if chosen_admin_filter == "Semua Bidang":
            df_base = df_filtered_periode.copy()
        else:
            df_base = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(chosen_admin_filter)]
    else:
        df_base = df_filtered_periode.head(0)

# --- HEADER UTAMA ---
st.markdown("""
<div class="header-banner">
    <div class="header-title">SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM</div>
    <div class="header-subtitle">Sistem Pemantauan Granular Hasil Audit Kepatuhan & Performansi — Internal Audit Unit</div>
</div>
""", unsafe_allow_html=True)

# --- TAB UTAMA ---
tab_dash, tab_vault_kka, tab_vault_lha = st.tabs([
    "📊 Dashboard Monitoring Eksekutif", 
    "📋 Vault KKA & AP (Penyimpanan File)", 
    "📁 Vault LHA Word (Penyimpanan File)"
])

with tab_dash:
    if not df_base.empty:
        overdue_df = df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)]
        overdue_count = len(overdue_df)
        if overdue_count > 0:
            st.markdown(f"""
            <div class="alert-blink">
                <div style="font-size: 24px;">🚨</div>
                <div>
                    <div style="color: #f87171; font-weight: 700; font-size: 15px;">PERINGATAN: ADA {overdue_count} REKOMENDASI OVERDUE (BELUM DITINDAKLANJUTI)</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### Ringkasan Eksekutif KPI")
    total_temuan = len(df_base)
    selesai = len(df_base[df_base[col_status].str.contains("Selesai|SLS", case=False, na=False)]) if not df_base.empty else 0
    evaluasi = len(df_base[df_base[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)]) if not df_base.empty else 0
    overdue = len(df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)]) if not df_base.empty else 0

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card card-blue"><div class="kpi-title">TOTAL TEMUAN</div><div class="kpi-value">{total_temuan}</div></div>
        <div class="kpi-card card-green"><div class="kpi-title">SELESAI (SLS)</div><div class="kpi-value">{selesai}</div></div>
        <div class="kpi-card card-yellow"><div class="kpi-title">EVALUASI (EVAL)</div><div class="kpi-value">{evaluasi}</div></div>
        <div class="kpi-card card-red"><div class="kpi-title">OVERDUE (BD)</div><div class="kpi-value">{overdue}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # --- TABEL REKAPITULASI MATRIKS TINDAK LANJUT ---
    if not df_base.empty:
        st.markdown("### Rekapitulasi Matriks Tindak Lanjut Hasil Audit")
        
        # Membuat ringkasan rekapitulasi per bidang
        rekap_data = []
        unique_bidangs = sorted(df_base[col_bidang].dropna().astype(str).unique())
        
        for idx, b in enumerate(unique_bidangs, 1):
            sub_df = df_base[df_base[col_bidang].astype(str) == str(b)]
            j_temuan = len(sub_df)
            j_selesai = len(sub_df[sub_df[col_status].str.contains("Selesai|SLS", case=False, na=False)])
            j_eval = len(sub_df[sub_df[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)])
            j_bd = len(sub_df[sub_df[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)])
            
            rekap_data.append({
                "No": chr(64 + idx),
                "Objek Audit": f"Bidang {b}",
                "Jumlah Temuan": j_temuan,
                "Jumlah Rekomendasi": j_temuan,
                "Selesai (SLS)": j_selesai,
                "EVALUASI AUDITOR": j_eval,
                "Belum Ditindaklanjuti (BD)": j_bd,
                "TPTD": 0
            })
            
        df_rekap = pd.DataFrame(rekap_data)
        st.dataframe(df_rekap, use_container_width=True, hide_index=True)

    # --- GRAFIK ANALITIK PENDUKUNG ---
    if not df_base.empty:
        st.markdown("---")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("#### Distribusi Status Tindak Lanjut")
            status_counts = df_base[col_status].value_counts().reset_index()
            status_counts.columns = ['Status', 'Jumlah']
            fig_status = px.pie(status_counts, names='Status', values='Jumlah', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            fig_status.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig_status, use_container_width=True)
            
        with col_g2:
            st.markdown("#### Temuan Berdasarkan Bidang")
            bidang_counts = df_base[col_bidang].value_counts().reset_index()
            bidang_counts.columns = ['Bidang', 'Jumlah']
            fig_bidang = px.bar(bidang_counts, x='Bidang', y='Jumlah', color='Bidang', color_discrete_sequence=px.colors.sequential.Plasma)
            fig_bidang.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False)
            st.plotly_chart(fig_bidang, use_container_width=True)

    st.markdown("---")
    st.markdown("### Detail Data Temuan & Rekomendasi")
    st.dataframe(df_base, use_container_width=True, hide_index=True)

with tab_vault_kka:
    st.markdown("### Vault Penyimpanan File KKA & Program Audit (AP)")
    st.info("💡 **Penyimpanan Aman:** Unggah file asli KKA atau Program Audit (.xlsx, .docx, .pdf) dari auditor induk di sini.")

with tab_vault_lha:
    st.markdown("### Vault Penyimpanan File LHA (.docx / .pdf)")
    st.info("💡 **Pusat Arsip LHA:** Unggah file laporan hasil audit resmi dari auditor induk di sini.")
