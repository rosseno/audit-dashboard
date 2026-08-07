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

# Custom Styling UI (Desain Kartu Elegan & Proporsional)
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
    
    /* Styling Kartu KPI yang Rapih dan Lebar */
    .kpi-card {
        background-color: #1e293b;
        border-radius: 8px;
        padding: 12px 15px;
        border: 1px solid #334155;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
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

# Sidebar Filters
st.sidebar.markdown("## 🎯 Filter Control Panel")
col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]
selected_periode = st.sidebar.selectbox("📅 Periode Audit:", ["Semua Periode"] + sorted(list(df_master[col_periode].dropna().astype(str).unique())))

df_filtered_periode = df_master[df_master[col_periode].astype(str) == str(selected_periode)] if selected_periode != "Semua Periode" else df_master.copy()

col_bidang = "Bidang" if "Bidang" in df_master.columns else df_master.columns[5]
selected_bidang = st.sidebar.selectbox("📂 Bidang Workgroup:", ["Semua Bidang"] + sorted(list(df_filtered_periode[col_bidang].dropna().astype(str).unique())))

df_filtered = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(selected_bidang)] if selected_bidang != "Semua Bidang" else df_filtered_periode.copy()

# Header
header_label = f"DEPARTEMEN {selected_bidang.upper()}" if selected_bidang != "Semua Bidang" else "SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM"
st.markdown(f"""<div class="header-banner"><div class="header-title">📊 {header_label}</div></div>""", unsafe_allow_html=True)

# KPI Cards (Desain Lebar dan Proporsional)
st.markdown("### 📈 Ringkasan Eksekutif KPI")

col_status = "Status" if "Status" in df_filtered.columns else "Status_TL"
total_temuan = len(df_filtered)
selesai = len(df_filtered[df_filtered[col_status].str.contains("Selesai|SLS", case=False, na=False)])
evaluasi = len(df_filtered[df_filtered[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)])
overdue = len(df_filtered[df_filtered[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)])

p_selesai = (selesai / total_temuan * 100) if total_temuan > 0 else 0
p_evaluasi = (evaluasi / total_temuan * 100) if total_temuan > 0 else 0
p_overdue = (overdue / total_temuan * 100) if total_temuan > 0 else 0

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 3px solid #3b82f6;">
        <span style="color: #94a3b8; font-size: 11px; font-weight: bold;">TOTAL TEMUAN</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{total_temuan}</h3>
        <span style="color: #64748b; font-size: 10px;">Judul LHP Utama</span>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 3px solid #8b5cf6;">
        <span style="color: #94a3b8; font-size: 11px; font-weight: bold;">POIN REKOMENDASI</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{total_temuan}</h3>
        <span style="color: #64748b; font-size: 10px;">Butir Granular</span>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 3px solid #00CC96;">
        <span style="color: #00CC96; font-size: 11px; font-weight: bold;">🟢 SELESAI (SLS)</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{selesai}</h3>
        <span style="color: #00CC96; font-size: 10px;">{p_selesai:.1f}% dari Total</span>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 3px solid #FFA15A;">
        <span style="color: #FFA15A; font-size: 11px; font-weight: bold;">🟡 EVALUASI (EVAL)</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{evaluasi}</h3>
        <span style="color: #FFA15A; font-size: 10px;">{p_evaluasi:.1f}% Dalam Proses</span>
    </div>""", unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="kpi-card" style="border-top: 3px solid #EF553B;">
        <span style="color: #EF553B; font-size: 11px; font-weight: bold;">🔴 OVERDUE (BD)</span>
        <h3 style="color: #ffffff; margin: 2px 0 0 0; font-size: 22px;">{overdue}</h3>
        <span style="color: #EF553B; font-size: 10px;">{p_overdue:.1f}% Belum TL</span>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# Chart & Data
color_map = {'Selesai (SLS)': '#00CC96', 'Evaluasi (EVAL)': '#FFA15A', 'Overdue (BD)': '#EF553B', 'Belum TL': '#EF553B'}
col_chart_bar, col_chart_pie = st.columns([3, 1.5])

with col_chart_bar:
    df_chart = df_filtered.groupby([col_bidang, col_status]).size().reset_index(name='Jumlah')
    fig_bar = px.bar(df_chart, x='Jumlah', y=col_bidang, color=col_status, orientation='h', barmode='stack', title="Progres Status per Bidang", color_discrete_map=color_map, template='plotly_dark')
    fig_bar.update_layout(height=300, margin=dict(l=0, r=10, t=30, b=0))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart_pie:
    df_pie = df_filtered.groupby(col_status).size().reset_index(name='Total')
    fig_pie = px.pie(df_pie, values='Total', names=col_status, hole=0.6, title="Proporsi Status", color=col_status, color_discrete_map=color_map, template='plotly_dark')
    fig_pie.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("### 📋 Detail Data")
st.dataframe(df_filtered, use_container_width=True)
