import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# Config Halaman Dashboard
st.set_page_config(
    page_title="Executive Audit Dashboard - PT Pelindo Solusi Maritim",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling UI (Compact & Professional Card Style)
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
    .header-title {
        color: #ffffff;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 3px;
    }
    .header-subtitle {
        color: #94a3b8;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx")
    except:
        df = pd.read_excel("Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx")
    return df

try:
    df_master = load_data()
except Exception as e:
    st.error(f"Gagal memuat file Excel. Error: {e}")
    st.stop()

# PIN Admin Configuration
PIN_ADMIN = "1234"

# =========================================================
# SIDEBAR FILTER CONTROL PANEL (BERTINGKAT)
# =========================================================
st.sidebar.markdown("## 🎯 Filter Control Panel")
st.sidebar.markdown("---")

col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]
periode_list = ["Semua Periode"] + sorted(list(df_master[col_periode].dropna().astype(str).unique()))
selected_periode = st.sidebar.selectbox("📅 Periode Audit:", periode_list)

# 1. Saring DataFrame berdasarkan Periode terlebih dahulu agar bidang sinkron
if selected_periode != "Semua Periode":
    df_filtered_periode = df_master[df_master[col_periode].astype(str) == str(selected_periode)]
else:
    df_filtered_periode = df_master.copy()

# 2. Bidang Workgroup hanya menampilkan data yang ADA di periode tersebut
col_bidang = "Bidang" if "Bidang" in df_master.columns else df_master.columns[5]
bidang_list = ["Semua Bidang"] + sorted(list(df_filtered_periode[col_bidang].dropna().astype(str).unique()))
selected_bidang = st.sidebar.selectbox("📂 Bidang Workgroup:", bidang_list)

# 3. Filter akhir untuk aplikasi
if selected_bidang != "Semua Bidang":
    df_filtered = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(selected_bidang)]
else:
    df_filtered = df_filtered_periode.copy()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔐 Akses Admin (Editor)")
input_pin = st.sidebar.text_input("Masukkan PIN Admin untuk Edit Data:", type="password")

if input_pin == PIN_ADMIN:
    st.sidebar.success("🔓 Akses Editor Aktif")
    mode_edit = st.sidebar.checkbox("📝 Buka Mode Editor Status", value=True)
elif input_pin != "":
    st.sidebar.error("❌ PIN Salah")
    mode_edit = False
else:
    st.sidebar.info("🔒 Mode Read-Only (Hanya Lihat)")
    mode_edit = False

# ---------------------------------------------------------
# MAIN CONTENT HEADER
# ---------------------------------------------------------
header_label = f"DEPARTEMEN {selected_bidang.upper()}" if selected_bidang != "Semua Bidang" else "SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM"

st.markdown(f"""
<div class="header-banner">
    <div class="header-title">📊 {header_label}</div>
    <div class="header-subtitle">Sistem Pemantauan Granular Hasil Audit Kepatuhan & Performa — Internal Audit Unit</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# RINGKASAN EKSEKUTIF KPI (COMPACT & SLEEK CARDS)
# ---------------------------------------------------------
st.markdown("### 📈 Ringkasan Eksekutif KPI")

total_temuan = len(df_filtered)
col_status = "Status" if "Status" in df_filtered.columns else "Status_TL"

selesai = len(df_filtered[df_filtered[col_status].str.contains("Selesai|SLS", case=False, na=False)]) if col_status in df_filtered.columns else 0
evaluasi = len(df_filtered[df_filtered[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)]) if col_status in df_filtered.columns else 0
overdue = len(df_filtered[df_filtered[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)]) if col_status in df_filtered.columns else 0
persen_selesai = (selesai / total_temuan * 100) if total_temuan > 0 else 0
persen_evaluasi = (evaluasi / total_temuan * 100) if total_temuan > 0 else 0
persen_overdue = (overdue / total_temuan * 100) if total_temuan > 0 else 0

col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)

with col_kpi1:
    st.markdown(f"""
    <div style="background-color: #1e293b; border-radius: 8px; padding: 12px 15px; border-top: 3px solid #3b82f6; border: 1px solid #334155;">
        <span style="color: #94a3b8; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;">TOTAL TEMUAN</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{total_temuan}</h3>
        <span style="color: #64748b; font-size: 10px;">Judul LHP Utama</span>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div style="background-color: #1e293b; border-radius: 8px; padding: 12px 15px; border-top: 3px solid #8b5cf6; border: 1px solid #334155;">
        <span style="color: #94a3b8; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;">POIN REKOMENDASI</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{total_temuan}</h3>
        <span style="color: #64748b; font-size: 10px;">Butir Granular</span>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div style="background-color: #1e293b; border-radius: 8px; padding: 12px 15px; border-top: 3px solid #00CC96; border: 1px solid #334155;">
        <span style="color: #00CC96; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;">🟢 SELESAI (SLS)</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{selesai}</h3>
        <span style="color: #00CC96; font-size: 10px;">{persen_selesai:.1f}% dari Total</span>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div style="background-color: #1e293b; border-radius: 8px; padding: 12px 15px; border-top: 3px solid #FFA15A; border: 1px solid #334155;">
        <span style="color: #FFA15A; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;">🟡 EVALUASI (EVAL)</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{evaluasi}</h3>
        <span style="color: #FFA15A; font-size: 10px;">{persen_evaluasi:.1f}% Dalam Proses</span>
    </div>
    """, unsafe_allow_html=True)

with col_kpi5:
    st.markdown(f"""
    <div style="background-color: #1e293b; border-radius: 8px; padding: 12px 15px; border-top: 3px solid #EF553B; border: 1px solid #334155;">
        <span style="color: #EF553B; font-size: 11px; font-weight: bold; letter-spacing: 0.5px;">🔴 OVERDUE (BD)</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{overdue}</h3>
        <span style="color: #EF553B; font-size: 10px;">{persen_overdue:.1f}% Belum TL</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------------
# PALET WARNA KLASIK (PLOTLY STANDARD)
# ---------------------------------------------------------
color_map = {
    'Selesai (SLS)': '#00CC96',   # Hijau Toska
    'Evaluasi (EVAL)': '#FFA15A', # Oranye
    'Overdue (BD)': '#EF553B',    # Merah/Pink
    'Belum TL': '#EF553B'         # Cadangan Merah/Pink
}

# ---------------------------------------------------------
# VISUALISASI DISTRIBUSI & PROGRES TINDAK LANJUT (OPTIMIZED SIZE)
# ---------------------------------------------------------
st.markdown("### 📊 Visualisasi Distribusi & Progres Tindak Lanjut")

if not df_filtered.empty and col_status in df_filtered.columns:
    col_chart_bar, col_chart_pie = st.columns([3, 1.5])

    # --- KIRI: Grafik Batang Horizontal (Tinggi Proporsional) ---
    with col_chart_bar:
        df_chart = df_filtered.groupby([col_bidang, col_status]).size().reset_index(name='Jumlah')
        
        fig_bar = px.bar(
            df_chart, 
            x='Jumlah', 
            y=col_bidang, 
            color=col_status, 
            orientation='h',
            barmode='stack',
            title="Progres Status per Bidang Workgroup",
            color_discrete_map=color_map,
            template='plotly_dark'
        )
        fig_bar.update_layout(
            height=320,  # Membatasi tinggi agar tidak terlalu besar/panjang ke bawah
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=10, t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title="")
        )
        fig_bar.update_xaxes(title="Jumlah Temuan")
        fig_bar.update_yaxes(title="")
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- KANAN: Donut Chart (Proporsi Total - Ukuran Pas) ---
    with col_chart_pie:
        df_pie = df_filtered.groupby(col_status).size().reset_index(name='Total')
        
        fig_pie = px.pie(
            df_pie, 
            values='Total', 
            names=col_status, 
            hole=0.6,
            title="Proporsi Status Total",
            color=col_status,
            color_discrete_map=color_map,
            template='plotly_dark'
        )
        fig_pie.update_layout(
            height=320,  # Menyamakan tinggi agar seimbang dengan chart sebelah kiri
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=False
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.info("Data grafik belum tersedia untuk filter yang dipilih.")

st.markdown("---")

# ---------------------------------------------------------
# TABEL DATA & MONITORING
# ---------------------------------------------------------
st.markdown("### 📋 Detail Data Temuan & Tindak Lanjut Audit")

if mode_edit and input_pin == PIN_ADMIN:
    st.warning("⚠️ Anda berada dalam Mode Edit. Perubahan langsung pada tabel di bawah dapat disesuaikan.")
    edited_df = st.data_editor(df_filtered, num_rows="dynamic", use_container_width=True)
else:
    st.dataframe(df_filtered, use_container_width=True)

# Footer info
st.markdown("---")
st.caption("Internal Audit Unit — PT Pelindo Solusi Maritim © 2026 | Didukung oleh Streamlit Cloud")
