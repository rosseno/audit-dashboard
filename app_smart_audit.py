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

# Custom CSS
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

if 'df_master' not in st.session_state:
    st.session_state.df_master = load_data()

df_master = st.session_state.df_master
PIN_ADMIN = "1234"  # <-- PIN Admin SPI

col_bidang = "Bidang" if "Bidang" in df_master.columns else df_master.columns[5]
col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]
col_status = "Status" if "Status" in df_master.columns else "Status_TL"

# Pastikan kolom verifikasi auditor ada di dataframe
if "Verifikasi_Auditor" not in df_master.columns:
    df_master["Verifikasi_Auditor"] = "Belum Diverifikasi"
if "Catatan_Auditor" not in df_master.columns:
    df_master["Catatan_Auditor"] = "-"

# --- SIDEBAR: PENGATURAN HAK AKSES & PERIODE ---
st.sidebar.markdown("## 🎯 Filter Control Panel")
selected_periode = st.sidebar.selectbox("📅 Periode Audit:", ["Semua Periode"] + sorted(list(df_master[col_periode].dropna().astype(str).unique())))

df_filtered_periode = df_master[df_master[col_periode].astype(str) == str(selected_periode)] if selected_periode != "Semua Periode" else df_master.copy()
current_available_bidang = sorted(list(df_filtered_periode[col_bidang].dropna().astype(str).unique()))

st.sidebar.markdown("---")
st.sidebar.markdown("## 🔐 Hak Akses & Portofolio")
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

role_title = "SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM"

# --- LOGIKA INPUT PIN ADMIN ---
if access_role == "Admin SPI":
    if not st.session_state.admin_logged_in:
        entered_pin = st.sidebar.text_input("🔑 Masukkan PIN Admin:", type="password")
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

# --- PEMETAAN DATA BERDASARKAN PERAN ---
if access_role == "Direktur Utama":
    sub_choice = st.sidebar.selectbox("Tinjau Cakupan:", ["Semua Bidang (Keseluruhan)", "SPI", "Hukum", "Sekper", "Pengadaan"])
    if sub_choice == "Semua Bidang (Keseluruhan)":
        df_base = df_filtered_periode.copy()
        role_title = f"DIREKTORAT UTAMA - PERIODE {selected_periode}"
    else:
        df_base = df_filtered_periode[df_filtered_periode[col_bidang].str.contains(sub_choice, case=False, na=False)]
        role_title = f"DIREKTORAT UTAMA - {sub_choice.upper()} ({selected_periode})"

elif access_role == "Direktur Operasi & Komersial":
    ops_choices = ["Operasi", "Teknik", "Pemasaran"]
    df_base = df_filtered_periode[df_filtered_periode[col_bidang].str.contains('|'.join(ops_choices), case=False, na=False)]
    role_title = f"DIREKTORAT OPERASI & KOMERSIAL ({selected_periode})"

elif access_role == "Direktur Keuangan, SDM, HSSE, IT, PAP, Umum & RT":
    fin_choices = ["Keuangan", "SDM", "HSSE", "IT", "PAP", "Umum", "Rumah Tangga"]
    df_base = df_filtered_periode[df_filtered_periode[col_bidang].str.contains('|'.join(fin_choices), case=False, na=False)]
    role_title = f"DIREKTORAT KEUANGAN, SDM, HSSE, IT, PAP, UMUM & RT ({selected_periode})"

elif access_role == "Auditee":
    chosen_unit = st.sidebar.selectbox("Pilih Bidang:", current_available_bidang if current_available_bidang else ["Tidak ada data"])
    df_base = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(chosen_unit)]
    role_title = f"DEPARTEMEN {chosen_unit.upper()} ({selected_periode})"

else:  # Admin SPI
    if st.session_state.admin_logged_in:
        chosen_admin_filter = st.sidebar.selectbox("📂 Filter Bidang:", ["Semua Bidang"] + current_available_bidang)
        if chosen_admin_filter == "Semua Bidang":
            df_base = df_filtered_periode.copy()
        else:
            df_base = df_filtered_periode[df_filtered_periode[col_bidang].astype(str) == str(chosen_admin_filter)]
        role_title = f"ADMIN SPI - FULL ACCESS ({selected_periode})"
    else:
        df_base = df_filtered_periode.head(0)
        role_title = "SILAKAN LOGIN ADMIN"

# Header Banner
st.markdown(f"""<div class="header-banner"><div class="header-title">📊 {role_title}</div></div>""", unsafe_allow_html=True)

# KPI Interaktif
st.markdown("### 📈 Ringkasan Eksekutif KPI (Klik Kartu untuk Filter Status)")
if 'filter_status' not in st.session_state: 
    st.session_state.filter_status = "Semua"

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

df_filtered = df_base.copy()
if st.session_state.filter_status == "Selesai":
    df_filtered = df_base[df_base[col_status].str.contains("Selesai|SLS", case=False, na=False)]
elif st.session_state.filter_status == "Evaluasi":
    df_filtered = df_base[df_base[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)]
elif st.session_state.filter_status == "Overdue":
    df_filtered = df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)]

st.markdown(f"<p style='color: #3b82f6; font-size: 12px; margin-top: -10px;'>Status Filter Aktif: <b>{st.session_state.filter_status}</b></p>", unsafe_allow_html=True)
st.markdown("---")

color_map = {'Selesai': '#00BCD4', 'SLS': '#00BCD4', 'Evaluasi': '#FFCA28', 'EVAL': '#FFCA28', 'Overdue': '#FF7043', 'BD': '#FF7043', 'Belum TL': '#FF7043'}

col_chart_bar, col_chart_pie = st.columns([3, 1.5])
with col_chart_bar:
    if not df_filtered.empty:
        df_chart = df_filtered.groupby([col_bidang, col_status]).size().reset_index(name='Jumlah')
        fig_bar = px.bar(df_chart, x='Jumlah', y=col_bidang, color=col_status, orientation='h', barmode='stack', title="Progres Status per Bidang", color_discrete_map=color_map, template='plotly_dark')
        fig_bar.update_layout(height=300, margin=dict(l=0, r=10, t=30, b=0))
        st.plotly_chart(fig_bar, use_container_width=True)
with col_chart_pie:
    if not df_filtered.empty:
        df_pie = df_filtered.groupby(col_status).size().reset_index(name='Total')
        fig_pie = px.pie(df_pie, values='Total', names=col_status, hole=0.6, title="Proporsi Status", color=col_status, color_discrete_map=color_map, template='plotly_dark')
        fig_pie.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

# --- PENGATURAN KOLOM TABEL ---
columns_to_drop = [
    "No", "Poin", "Tahun Audit", "Nama Entitas", "Tingkat Risiko", 
    "Prioritas", "Tag Kata Kunci (#Preventif)", 
    "Ringkasan Kondisi & Akar Masalah (Root Cause)"
]
df_table_display = df_filtered.drop(columns=[col for col in columns_to_drop if col in df_filtered.columns])
df_table_display.insert(0, "No", range(1, len(df_table_display) + 1))

st.markdown("### 📋 Detail Data Temuan & Rekomendasi")
st.dataframe(df_table_display, use_container_width=True, hide_index=True)

# --- PANEL KHUSUS ADMIN SPI UNTUK INPUT VERIFIKASI ---
if access_role == "Admin SPI" and st.session_state.admin_logged_in:
    st.markdown("---")
    st.markdown("### ✍️ Panel Update Verifikasi Auditor (Approve / Reject / Sedang Diverifikasi)")
    st.info("💡 Pilih ID Temuan di bawah ini untuk memperbarui status verifikasi dan memberikan catatan kepada Auditee.")
    
    id_list = df_base["ID Temuan"].dropna().astype(str).unique().tolist() if "ID Temuan" in df_base.columns else []
    if id_list:
        selected_id = st.selectbox("Pilih ID Temuan:", id_list)
        row_idx = df_master[df_master["ID Temuan"].astype(str) == str(selected_id)].index
        if len(row_idx) > 0:
            current_verif = df_master.loc[row_idx[0], "Verifikasi_Auditor"]
            current_note = df_master.loc[row_idx[0], "Catatan_Auditor"]
            
            # Tentukan index default pilihan selectbox
            opt_list = [
                "Belum Diverifikasi", 
                "⏳ Sedang Diverifikasi Auditor", 
                "✅ Disetujui (Approve - Status Selesai)", 
                "❌ Ditolak (Reject - Status Overdue)"
            ]
            default_idx = 0
            if "Sedang" in str(current_verif):
                default_idx = 1
            elif "Disetujui" in str(current_verif):
                default_idx = 2
            elif "Ditolak" in str(current_verif):
                default_idx = 3

            with st.form(key="form_verifikasi"):
                col_v1, col_v2 = st.columns(2)
                with col_v1:
                    verdict = st.selectbox("Keputusan Auditor:", opt_list, index=default_idx)
                with col_v2:
                    auditor_note = st.text_area("Catatan / Tanggapan Auditor untuk Auditee:", value=str(current_note))
                
                submit_verif = st.form_submit_button("💾 Simpan & Tampilkan ke Auditee")
                
                if submit_verif:
                    df_master.loc[row_idx, "Catatan_Auditor"] = auditor_note
                    if "Sedang" in verdict:
                        df_master.loc[row_idx, "Verifikasi_Auditor"] = "⏳ Sedang Diverifikasi Auditor"
                        st.info(f"Temuan {selected_id} berstatus Sedang Diverifikasi Auditor.")
                    elif "Disetujui" in verdict:
                        df_master.loc[row_idx, "Verifikasi_Auditor"] = "Disetujui"
                        df_master.loc[row_idx, col_status] = "Selesai (SLS)"
                        st.success(f"Temuan {selected_id} disetujui. Status otomatis menjadi Selesai.")
                    elif "Ditolak" in verdict:
                        df_master.loc[row_idx, "Verifikasi_Auditor"] = "Ditolak"
                        df_master.loc[row_idx, col_status] = "Overdue (BD)"
                        st.warning(f"Temuan {selected_id} ditolak. Status otomatis menjadi Overdue.")
                    else:
                        df_master.loc[row_idx, "Verifikasi_Auditor"] = "Belum Diverifikasi"
                    
                    st.session_state.df_master = df_master
                    st.rerun()

# --- INTEGRASI GOOGLE FORM / GOOGLE DRIVE (KHUSUS AUDITEE & ADMIN) ---
if access_role in ["Auditee", "Admin SPI"]:
    st.markdown("---")
    st.markdown("### 📤 Pengunggahan Bukti Dukung (Evidence) Tindak Lanjut")
    st.info("💡 Klik tautan di bawah ini untuk mengunggah dokumen bukti penyelesaian temuan audit ke Google Drive SPI.")
    
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSczUxjVMZqcduSy704OVRGvIRga1LhQDAkJKoUkDUn6Aez82A/viewform"
    st.markdown(
        f"""
        <a href="{google_form_url}" target="_blank">
            <div style="display: inline-block; background-color: #3b82f6; color: white; padding: 12px 24px; border-radius: 8px; font-weight: bold; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                🚀 Buka Formulir Upload Bukti Dukung (Google Drive)
            </div>
        </a>
        """,
        unsafe_allow_html=True
    )
