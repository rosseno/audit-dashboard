import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set page config
st.set_page_config(layout="wide", page_title="Executive Audit Dashboard")

# Load Data
EXCEL_FILE = "Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx"
@st.cache_data
def load_data():
    if os.path.exists(EXCEL_FILE):
        return pd.read_excel(EXCEL_FILE)
    return pd.DataFrame()

df = load_data()

# Sidebar
st.sidebar.title("🛡️ AUDIT CONTROL")
role = st.sidebar.selectbox("Pilih Peran:", ["Admin SPI", "Direktur Utama", "Auditee"])
periode = st.sidebar.selectbox("Periode:", ["Semua"] + sorted(df["Tahun Audit"].unique().tolist()))
unit = st.sidebar.selectbox("Pilih Unit:", ["Semua"] + sorted(df["Bidang"].unique().tolist()))

# Main Content
st.title("SMART AUDIT MONITORING")

# Metrics
col1, col2, col3, col4 = st.columns(4)
total = len(df)
sls = len(df[df["Status"].str.contains("Selesai|SLS", na=False)])
eval = len(df[df["Status"].str.contains("Evaluasi|EVAL", na=False)])
bd = len(df[df["Status"].str.contains("BD|Belum|Overdue", na=False)])

col1.metric("TOTAL", total)
col2.metric("SELESAI", sls)
col3.metric("EVALUASI", eval)
col4.metric("OVERDUE", bd)

# Filtering Data
dff = df.copy()
if periode != "Semua": dff = dff[dff["Tahun Audit"] == periode]
if unit != "Semua": dff = dff[dff["Bidang"] == unit]

# Chart
if not dff.empty:
    fig = px.bar(dff, x="Bidang", color="Status", title="Temuan per Unit")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(dff)
else:
    st.warning("Data tidak ditemukan.")