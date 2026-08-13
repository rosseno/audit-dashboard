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

# Custom CSS dengan Latar Belakang Krem Lembut & Kartu Timbul (Soft Cream Theme)
st.markdown("""
<style>
    /* Latar belakang utama aplikasi menjadi krem lembut agar chart lebih hidup */
    .stApp { background-color: #fcfbfa; }
    
    /* Sidebar kiri dengan warna yang kontras dan elegan */
    [data-testid="stSidebar"] {
        background-color: #f1f5f9;
        color: #1e293b;
        padding-top: 20px;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: #1e293b !important;
    }

    /* Kartu Header Utama */
    .header-banner {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        padding: 20px 25px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.06);
    }
    .header-title { color: #ffffff; font-size: 22px; font-weight: 700; }
    .header-subtitle { color: #e2e8f0; font-size: 13px; margin-top: 5px; }

    /* Kotak Peringatan Overdue */
    .alert-blink {
        background: #fef2f2;
        border: 1px solid #f87171;
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 2px 4px rgba(239, 68, 68, 0.05);
    }

    /* Tombol KPI / Kartu Metrik Timbul */
    div.stButton > button {
        min-height: 90px;
        border-radius: 12px;
        font-weight: 600;
        background-color: #ffffff;
        color: #1e293b;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }
    div.stButton > button:hover {
        background-color: #f8fafc;
        border-color: #cbd5e1;
        box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.08);
    }
</style>
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

if 'notification_list' not in st.session_state:
    st.session_state.notification_list = []

df_master = st.session_state.df_master
col_bidang = "Bidang" if "Bidang" in df_master.columns else df_master.columns[5]
col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]
col_status = "Status" if "Status" in df_master.columns else "Status_TL"

PIN_ADMIN = "1234"

# --- SIDEBAR NAVIGASI ---
with st.sidebar:
    st.markdown("### 🛡️ AUDIT DASHBOARD")
    st.markdown("<p style='font-size: 12px; color: #64748b;'>Decision Support System</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    selected_menu = st.radio(
        "Navigasi Utama",
        [
            "📊 Executive Overview",
            "📋 KPI Performance",
            "📁 Vault KKA & AP",
            "📂 Vault LHA Word"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("## Filter Control Panel")
    existing_periods = sorted(list(df_master[col_periode].dropna().astype(str).unique()))
    if "2026" not in existing_periods:
        existing_periods.append("2026")

    periode_options = ["Semua Periode"] + existing_periods
    selected_periode = st.selectbox("Periode Audit:", periode_options)

    if selected_periode == "2026":
        df_filtered_periode = df_master.head(0).copy()
    else:
        df_filtered_periode = df_master[df_master[col_periode].astype(str) == str(selected_periode)] if selected_periode != "Semua Periode" else df_master.copy()

    current_available_bidang = sorted(list(df_filtered_periode[col_bidang].dropna().astype(str).unique())) if not df_filtered_periode.empty else sorted(list(df_master[col_bidang].dropna().astype(str).unique()))

    st.markdown("---")
    st.markdown("## Hak Akses & Portofolio")

    access_role = st.selectbox(
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
            entered_pin = st.text_input("Masukkan PIN Admin:", type="password")
            if entered_pin == PIN_ADMIN:
                st.session_state.admin_logged_in = True
                st.success("Login Admin Berhasil!")
                st.rerun()
            elif entered_pin:
                st.error("PIN Salah!")
        else:
            st.success("Status: Admin Aktif")
            if st.button("Logout Admin"):
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

# --- KONTEN UTAMA ---

# 1. PERINGATAN OVERDUE
if not df_base.empty:
    overdue_df = df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)]
    overdue_count = len(overdue_df)
    if overdue_count > 0:
        st.markdown(f"""
        <div class="alert-blink">
            <div style="font-size: 20px;">🚨</div>
            <div>
                <div style="color: #dc2626; font-weight: 700; font-size: 14px;">PERINGATAN: ADA {overdue_count} REKOMENDASI OVERDUE (BELUM DITINDAKLANJUTI)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 2. HEADER UTAMA
st.markdown("""
<div class="header-banner">
    <div class="header-title">EXECUTIVE OVERVIEW - PT PELINDO SOLUSI MARITIM</div>
    <div class="header-subtitle">KPI Performance Summary — Seluruh Departemen & Unit Kerja</div>
</div>
""", unsafe_allow_html=True)

if selected_menu == "📊 Executive Overview":
    st.markdown("### Ringkasan Eksekutif KPI")
    total_temuan = len(df_base)
    selesai = len(df_base[df_base[col_status].str.contains("Selesai|SLS", case=False, na=False)]) if not df_base.empty else 0
    evaluasi = len(df_base[df_base[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)]) if not df_base.empty else 0
    overdue = len(df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)]) if not df_base.empty else 0

    if 'kpi_filter' not in st.session_state:
        st.session_state.kpi_filter = "SEMUA"

    def set_filter(val):
        st.session_state.kpi_filter = val

    k_col1, k_col2, k_col3, k_col4 = st.columns(4)
    with k_col1:
        if st.button(f"📊 TOTAL\n\n{total_temuan}", key="btn_total", use_container_width=True):
            set_filter("SEMUA")
            st.rerun()
    with k_col2:
        if st.button(f"✅ SELESAI\n\n{selesai}", key="btn_sls", use_container_width=True):
            set_filter("SLS")
            st.rerun()
    with k_col3:
        if st.button(f"⚠️ EVALUASI\n\n{evaluasi}", key="btn_eval", use_container_width=True):
            set_filter("EVAL")
            st.rerun()
    with k_col4:
        if st.button(f"🚨 OVERDUE\n\n{overdue}", key="btn_bd", use_container_width=True):
            set_filter("BD")
            st.rerun()

    # --- VISUALISASI GRAFIK DENGAN LATAR KARTU PUTIH BERSIH AGAR TIMBUL ---
    st.markdown("---")
    st.markdown("### 📊 Visualisasi Distribusi & Progres Tindak Lanjut")
    
    color_map = {
        'Selesai (SLS)': '#10b981',
        'Evaluasi (EVAL)': '#f59e0b',
        'Overdue (BD)': '#ef4444',
        'Belum TL': '#ef4444'
    }

    if not df_base.empty and col_status in df_base.columns:
        col_chart_bar, col_chart_pie = st.columns([2.5, 1.5])

        with col_chart_bar:
            st.markdown('<div style="background: #ffffff; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
            df_chart = df_base.groupby([col_bidang, col_status]).size().reset_index(name='Jumlah')
            fig_bar = px.bar(
                df_chart, 
                x='Jumlah', 
                y=col_bidang, 
                color=col_status, 
                orientation='h',
                barmode='stack',
                title="Progres Status per Bidang Workgroup",
                color_discrete_map=color_map,
                template='plotly_white'
            )
            fig_bar.update_layout(
                height=260,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=10, t=35, b=0),
                title_font=dict(size=14, color='#1e293b', family='sans-serif'),
                font=dict(color='#334155', size=11),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title="")
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart_pie:
            st.markdown('<div style="background: #ffffff; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
            df_pie = df_base.groupby(col_status).size().reset_index(name='Total')
            fig_pie = px.pie(
                df_pie, 
                values='Total', 
                names=col_status, 
                hole=0.6,
                title="Proporsi Status Total",
                color=col_status,
                color_discrete_map=color_map,
                template='plotly_white'
            )
            fig_pie.update_layout(
                height=260,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=35, b=10),
                title_font=dict(size=14, color='#1e293b', family='sans-serif'),
                font=dict(color='#334155', size=11),
                showlegend=False
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Data grafik belum tersedia untuk filter yang dipilih.")

    st.markdown("---")
    st.markdown("### Detail Data Temuan & Rekomendasi")
    if st.session_state.kpi_filter == "SEMUA":
        df_table_final = df_base
    else:
        df_table_final = df_base[df_base[col_status].str.contains(st.session_state.kpi_filter, case=False, na=False)]

    target_columns = ["No", "ID Temuan", "Bidang", "Judul Temuan Audit", "Rekomendasi Utama / Tindak Lanjut", "Status", "PIC Temuan Audit"]
    df_table_display = df_table_final[[c for c in target_columns if c in df_table_final.columns]].copy()
    df_table_display["No"] = range(1, len(df_table_display) + 1)
    st.dataframe(df_table_display, use_container_width=True, hide_index=True)

elif selected_menu == "📋 KPI Performance":
    st.markdown("### 📋 Halaman Kinerja KPI & Detail Rekapitulasi")
    if not df_base.empty:
        rekap_data = []
        unique_bidangs = sorted(df_base[col_bidang].dropna().astype(str).unique())
        tot_tem = 0; tot_sls = 0; tot_eval = 0; tot_bd = 0
        
        for idx, b in enumerate(unique_bidangs, 1):
            sub_df = df_base[df_base[col_bidang].astype(str) == str(b)]
            j_temuan = len(sub_df)
            j_selesai = len(sub_df[sub_df[col_status].str.contains("Selesai|SLS", case=False, na=False)])
            j_eval = len(sub_df[sub_df[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)])
            j_bd = len(sub_df[sub_df[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)])
            
            tot_tem += j_temuan; tot_sls += j_selesai; tot_eval += j_eval; tot_bd += j_bd
            rekap_data.append({
                "No": chr(64 + idx), "Objek Audit": f"Bidang {b}", "Jumlah Temuan": j_temuan,
                "Selesai (SLS)": j_selesai, "EVALUASI AUDITOR": j_eval, "Belum Ditindaklanjuti (BD)": j_bd
            })
            
        rekap_data.append({"No": "", "Objek Audit": "JUMLAH", "Jumlah Temuan": tot_tem, "Selesai (SLS)": tot_sls, "EVALUASI AUDITOR": tot_eval, "Belum Ditindaklanjuti (BD)": tot_bd})
        df_rekap = pd.DataFrame(rekap_data)
        st.dataframe(df_rekap, use_container_width=True, hide_index=True)

elif selected_menu == "📁 Vault KKA & AP":
    st.markdown("### 📋 Vault Penyimpanan File KKA & Program Audit (AP)")
    uploaded_kka = st.file_uploader("Unggah File KKA / AP (.xlsx, .docx, .pdf)", type=["xlsx", "docx", "pdf"], key="uploader_kka")
    if uploaded_kka is not None:
        file_path = os.path.join(VAULT_DIR, uploaded_kka.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_kka.getbuffer())
        st.session_state.vault_kka.append({
            "Nama File": uploaded_kka.name,
            "Tanggal Upload": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Tipe": "KKA / AP"
        })
        pd.DataFrame(st.session_state.vault_kka).to_excel(EXCEL_KKA_FILE, index=False)
        st.success(f"File KKA '{uploaded_kka.name}' berhasil disimpan ke Vault!")

    if st.session_state.vault_kka:
        st.markdown("#### Daftar File KKA & AP Tersimpan:")
        for i, item in enumerate(st.session_state.vault_kka):
            f_path = os.path.join(VAULT_DIR, item["Nama File"])
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"📄 **{item['Nama File']}** ({item['Tipe']}) - {item['Tanggal Upload']}")
            with col2:
                if os.path.exists(f_path):
                    with open(f_path, "rb") as f:
                        st.download_button("📥 Unduh", f, file_name=item['Nama File'], key=f"dl_kka_{i}")
            with col3:
                if st.button("🗑️ Hapus", key=f"del_kka_{i}"):
                    if os.path.exists(f_path):
                        os.remove(f_path)
                    st.session_state.vault_kka.pop(i)
                    pd.DataFrame(st.session_state.vault_kka).to_excel(EXCEL_KKA_FILE, index=False)
                    st.rerun()

elif selected_menu == "📂 Vault LHA Word":
    st.markdown("### 📁 Vault Penyimpanan File LHA (.docx / .pdf)")
    uploaded_lha = st.file_uploader("Unggah File LHA (.docx, .pdf)", type=["docx", "pdf"], key="uploader_lha")
    if uploaded_lha is not None:
        file_path = os.path.join(VAULT_DIR, uploaded_lha.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_lha.getbuffer())
        st.session_state.vault_lha.append({
            "Nama File": uploaded_lha.name,
            "Tanggal Upload": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Tipe": "LHA"
        })
        pd.DataFrame(st.session_state.vault_lha).to_excel(EXCEL_LHA_FILE, index=False)
        st.success(f"File LHA '{uploaded_lha.name}' berhasil disimpan ke Vault!")

    if st.session_state.vault_lha:
        st.markdown("#### Daftar File LHA Tersimpan:")
        for i, item in enumerate(st.session_state.vault_lha):
            f_path = os.path.join(VAULT_DIR, item["Nama File"])
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"📄 **{item['Nama File']}** ({item['Tipe']}) - {item['Tanggal Upload']}")
            with col2:
                if os.path.exists(f_path):
                    with open(f_path, "rb") as f:
                        st.download_button("📥 Unduh", f, file_name=item['Nama File'], key=f"dl_lha_{i}")
            with col3:
                if st.button("🗑️ Hapus", key=f"del_lha_{i}"):
                    if os.path.exists(f_path):
                        os.remove(f_path)
                    st.session_state.vault_lha.pop(i)
                    pd.DataFrame(st.session_state.vault_lha).to_excel(EXCEL_LHA_FILE, index=False)
                    st.rerun()
