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

# Custom CSS Ultimate
st.markdown("""
<style>
    .main { background-color: #0e1117; }
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

    .stTextArea textarea {
        min-height: 100px !important;
    }

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

    .kpi-row {
        display: flex;
        gap: 14px;
        width: 100%;
        margin-bottom: 20px;
    }

    .kpi-card {
        flex: 1;
        background: linear-gradient(145deg, #161b22 0%, #0d1117 100%);
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        transition: transform 0.2s ease;
    }
    
    .kpi-card:hover { transform: translateY(-3px); }

    .card-blue { border: 2px solid #3b82f6; box-shadow: 0 0 12px rgba(59, 130, 246, 0.35); }
    .card-purple { border: 2px solid #8b5cf6; box-shadow: 0 0 12px rgba(139, 92, 246, 0.35); }
    .card-green { border: 2px solid #10b981; box-shadow: 0 0 12px rgba(16, 185, 129, 0.35); }
    .card-yellow { border: 2px solid #f59e0b; box-shadow: 0 0 12px rgba(245, 158, 11, 0.35); }
    .card-red { border: 2px solid #ef4444; box-shadow: 0 0 12px rgba(239, 68, 68, 0.35); }

    .kpi-title { color: #94a3b8; font-size: 10.5px; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase; margin-bottom: 4px; }
    .kpi-value { color: #ffffff; font-size: 28px; font-weight: 800; margin-bottom: 2px; line-height: 1.1; }
    .kpi-desc { color: #cbd5e1; font-size: 11.5px; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

EXCEL_FILE = "Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx"
EXCEL_KKA_FILE = "Database_Vault_KKA_AP.xlsx"
EXCEL_LHA_FILE = "Database_Vault_LHA_Word.xlsx"
VAULT_DIR = "audit_file_vault"

if not os.path.exists(VAULT_DIR):
    os.makedirs(VAULT_DIR)

@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE)
    except:
        df = pd.read_excel(EXCEL_FILE)
    return df

if 'df_master' not in st.session_state:
    st.session_state.df_master = load_data()

# Memuat data vault KKA & AP
if 'vault_kka' not in st.session_state:
    if os.path.exists(EXCEL_KKA_FILE):
        try:
            df_kka = pd.read_excel(EXCEL_KKA_FILE)
            if 'stored_filename' not in df_kka.columns:
                df_kka['stored_filename'] = "-"
            st.session_state.vault_kka = df_kka.to_dict('records')
        except:
            st.session_state.vault_kka = []
    else:
        st.session_state.vault_kka = []

# Memuat data vault LHA Word
if 'vault_lha' not in st.session_state:
    if os.path.exists(EXCEL_LHA_FILE):
        try:
            df_lha = pd.read_excel(EXCEL_LHA_FILE)
            if 'stored_filename' not in df_lha.columns:
                df_lha['stored_filename'] = "-"
            st.session_state.vault_lha = df_lha.to_dict('records')
        except:
            st.session_state.vault_lha = []
    else:
        st.session_state.vault_lha = []

def save_vault_kka_to_excel():
    if st.session_state.vault_kka:
        pd.DataFrame(st.session_state.vault_kka).to_excel(EXCEL_KKA_FILE, index=False)
    else:
        pd.DataFrame(columns=["vault_id", "target_temuan", "judul_kka", "auditor_name", "stored_filename", "catatan"]).to_excel(EXCEL_KKA_FILE, index=False)

def save_vault_lha_to_excel():
    if st.session_state.vault_lha:
        pd.DataFrame(st.session_state.vault_lha).to_excel(EXCEL_LHA_FILE, index=False)
    else:
        pd.DataFrame(columns=["vault_id", "target_temuan", "judul_lha", "auditor_name", "stored_filename", "catatan"]).to_excel(EXCEL_LHA_FILE, index=False)

df_master = st.session_state.df_master
PIN_ADMIN = "1234"

col_bidang = "Bidang" if "Bidang" in df_master.columns else df_master.columns[5]
col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]
col_status = "Status" if "Status" in df_master.columns else "Status_TL"

if "Catatan_Auditor" not in df_master.columns:
    df_master["Catatan_Auditor"] = "-"

# --- SIDEBAR: PENGATURAN HAK AKSES & PERIODE ---
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

# --- HEADER BANNER UTAMA ---
st.markdown("""
<div class="header-banner">
    <div class="header-title">SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM</div>
    <div class="header-subtitle">Sistem Pemantauan Granular Hasil Audit Kepatuhan & Performansi — Internal Audit Unit</div>
</div>
""", unsafe_allow_html=True)

# --- NAVIGASI UTAMA BERBENTUK TAB ---
tab_dash, tab_vault_kka, tab_vault_lha = st.tabs([
    "📊 Dashboard Monitoring Eksekutif", 
    "📋 Vault KKA & AP (Penyimpanan File)", 
    "📁 Vault LHA Word (Penyimpanan File)"
])

# ================= TAB 1: DASHBOARD MONITORING =================
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
    selesai = len(df_base[df_base[col_status].str.contains("Selesai|SLS", case=False, na=False)])
    evaluasi = len(df_base[df_base[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)])
    overdue = len(df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)])

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card card-blue"><div class="kpi-title">TOTAL TEMUAN</div><div class="kpi-value">{total_temuan}</div></div>
        <div class="kpi-card card-green"><div class="kpi-title">SELESAI (SLS)</div><div class="kpi-value">{selesai}</div></div>
        <div class="kpi-card card-yellow"><div class="kpi-title">EVALUASI (EVAL)</div><div class="kpi-value">{evaluasi}</div></div>
        <div class="kpi-card card-red"><div class="kpi-title">OVERDUE (BD)</div><div class="kpi-value">{overdue}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Detail Data Temuan & Rekomendasi")
    st.dataframe(df_base, use_container_width=True, hide_index=True)


# ================= TAB 2: VAULT KKA & AP =================
with tab_vault_kka:
    st.markdown("### Vault Penyimpanan File KKA & Program Audit (AP)")
    st.info("💡 **Penyimpanan Aman:** Unggah file asli KKA atau Program Audit (.xlsx, .docx, .pdf) dari auditor induk di sini. File tersimpan aman di sistem dan dapat diunduh kembali kapan saja.")
    
    if access_role == "Admin SPI":
        id_kka_list = df_master["ID Temuan"].dropna().astype(str).unique().tolist() if "ID Temuan" in df_master.columns else []
        if id_kka_list:
            selected_kka_id = st.selectbox("Pilih ID Temuan / Penugasan:", id_kka_list, key="vault_kka_select")
            
            if st.button("➕ Upload KKA / AP Baru"):
                new_v_id = f"VAULT-KKA-{len(st.session_state.vault_kka) + 1}"
                st.session_state.vault_kka.append({
                    "vault_id": new_v_id,
                    "target_temuan": selected_kka_id,
                    "judul_kka": "KKA & Program Audit",
                    "auditor_name": "Auditor Induk",
                    "stored_filename": "-",
                    "catatan": "File KKA asli tersimpan di sistem."
                })
                save_vault_kka_to_excel()
                st.rerun()
            
            st.markdown("---")
            
            filtered_vault_kkas = [r for r in st.session_state.vault_kka if str(r.get("target_temuan")) == str(selected_kka_id)]
            
            if not filtered_vault_kkas:
                st.info("Belum ada file KKA yang diunggah untuk temuan ini. Klik tombol ➕ di atas.")
            else:
                for idx, reg in enumerate(filtered_vault_kkas):
                    reg_key = reg['vault_id']
                    with st.container():
                        st.markdown(f"📋 **[{reg['vault_id']}] Temuan ID: {reg['target_temuan']}**")
                        
                        with st.form(key=f"form_vault_kka_{reg_key}_{idx}"):
                            judul_input = st.text_input("Judul / Keterangan Dokumen:", value=reg["judul_kka"])
                            auditor_input = st.text_input("Sumber / Penyusun:", value=reg["auditor_name"])
                            
                            uploaded_file = st.file_uploader("Upload / Ganti File KKA (.xlsx, .docx, .pdf):", type=["xlsx", "xls", "docx", "doc", "pdf"], key=f"up_f_kka_{reg_key}_{idx}")
                            
                            catatan_input = st.text_area("Catatan:", value=reg["catatan"], height=70)
                            
                            col_v1, col_v2 = st.columns(2)
                            with col_v1:
                                save_btn = st.form_submit_button("Simpan & Unggah File")
                            with col_v2:
                                del_btn = st.form_submit_button("🗑️ Hapus Dokumen Ini")
                                
                            if save_btn:
                                reg["judul_kka"] = judul_input
                                reg["auditor_name"] = auditor_input
                                reg["catatan"] = catatan_input
                                
                                if uploaded_file is not None:
                                    safe_name = f"{reg_key}_{uploaded_file.name}"
                                    file_path = os.path.join(VAULT_DIR, safe_name)
                                    with open(file_path, "wb") as f:
                                        f.write(uploaded_file.read())
                                    reg["stored_filename"] = safe_name
                                    st.toast("File berhasil diunggah dan disimpan!")
                                    
                                save_vault_kka_to_excel()
                                st.success("Data KKA berhasil diperbarui!")
                                st.rerun()
                                
                            if del_btn:
                                st.session_state.vault_kka.remove(reg)
                                save_vault_kka_to_excel()
                                st.success("Dokumen berhasil dihapus!")
                                st.rerun()

                        # Tombol Download File jika sudah ada
                        current_file = reg.get("stored_filename", "-")
                        if current_file != "-" and os.path.exists(os.path.join(VAULT_DIR, current_file)):
                            with open(os.path.join(VAULT_DIR, current_file), "rb") as file_to_down:
                                st.download_button(
                                    label=f"📥 Download File Tersimpan: {current_file}",
                                    data=file_to_down,
                                    file_name=current_file,
                                    mime="application/octet-stream",
                                    key=f"dl_kka_{reg_key}_{idx}"
                                )
                        else:
                            st.warning("⚠️ Belum ada file fisik yang diunggah.")
                        st.markdown("---")
    else:
        st.warning("⚠️ Menu penyimpanan file dikhususkan untuk peran Admin SPI.")


# ================= TAB 3: VAULT LHA WORD =================
with tab_vault_lha:
    st.markdown("### Vault Penyimpanan File LHA (.docx / .pdf)")
    st.info("💡 **Pusat Arsip LHA:** Unggah file laporan hasil audit resmi dari auditor induk di sini. File aman tersimpan di aplikasi dan siap diunduh kapan saja.")
    
    if access_role == "Admin SPI":
        id_lha_list = df_master["ID Temuan"].dropna().astype(str).unique().tolist() if "ID Temuan" in df_master.columns else []
        if id_lha_list:
            selected_lha_id = st.selectbox("Pilih ID Temuan / Penugasan:", id_lha_list, key="vault_lha_select")
            
            if st.button("➕ Upload LHA Baru"):
                new_v_lha_id = f"VAULT-LHA-{len(st.session_state.vault_lha) + 1}"
                st.session_state.vault_lha.append({
                    "vault_id": new_v_lha_id,
                    "target_temuan": selected_lha_id,
                    "judul_lha": "Laporan Hasil Audit (LHA)",
                    "auditor_name": "Auditor Induk",
                    "stored_filename": "-",
                    "catatan": "File LHA tersimpan di sistem."
                })
                save_vault_lha_to_excel()
                st.rerun()
            
            st.markdown("---")
            
            filtered_vault_lhas = [r for r in st.session_state.vault_lha if str(r.get("target_temuan")) == str(selected_lha_id)]
            
            if not filtered_vault_lhas:
                st.info("Belum ada file LHA yang diunggah untuk temuan ini. Klik tombol ➕ di atas.")
            else:
                for idx, reg in enumerate(filtered_vault_lhas):
                    reg_key = reg['vault_id']
                    with st.container():
                        st.markdown(f"📁 **[{reg['vault_id']}] Temuan ID: {reg['target_temuan']}**")
                        
                        with st.form(key=f"form_vault_lha_{reg_key}_{idx}"):
                            judul_input = st.text_input("Judul / Keterangan LHA:", value=reg["judul_lha"])
                            auditor_input = st.text_input("Sumber / Penyusun:", value=reg["auditor_name"])
                            
                            uploaded_lha_file = st.file_uploader("Upload / Ganti File LHA (.docx, .pdf):", type=["docx", "doc", "pdf"], key=f"up_f_lha_{reg_key}_{idx}")
                            
                            catatan_input = st.text_area("Catatan LHA:", value=reg["catatan"], height=70)
                            
                            col_l1, col_l2 = st.columns(2)
                            with col_l1:
                                save_lha_btn = st.form_submit_button("Simpan & Unggah LHA")
                            with col_l2:
                                del_lha_btn = st.form_submit_button("🗑️ Hapus LHA Ini")
                                
                            if save_lha_btn:
                                reg["judul_lha"] = judul_input
                                reg["auditor_name"] = auditor_input
                                reg["catatan"] = catatan_input
                                
                                if uploaded_lha_file is not None:
                                    safe_lha_name = f"{reg_key}_{uploaded_lha_file.name}"
                                    file_path = os.path.join(VAULT_DIR, safe_lha_name)
                                    with open(file_path, "wb") as f:
                                        f.write(uploaded_lha_file.read())
                                    reg["stored_filename"] = safe_lha_name
                                    st.toast("File LHA berhasil diunggah!")
                                    
                                save_vault_lha_to_excel()
                                st.success("Data LHA berhasil diperbarui!")
                                st.rerun()
                                
                            if del_lha_btn:
                                st.session_state.vault_lha.remove(reg)
                                save_vault_lha_to_excel()
                                st.success("LHA berhasil dihapus!")
                                st.rerun()

                        # Tombol Download LHA jika sudah ada
                        current_lha_file = reg.get("stored_filename", "-")
                        if current_lha_file != "-" and os.path.exists(os.path.join(VAULT_DIR, current_lha_file)):
                            with open(os.path.join(VAULT_DIR, current_lha_file), "rb") as file_to_down_lha:
                                st.download_button(
                                    label=f"📥 Download File LHA Tersimpan: {current_lha_file}",
                                    data=file_to_down_lha,
                                    file_name=current_lha_file,
                                    mime="application/octet-stream",
                                    key=f"dl_lha_{reg_key}_{idx}"
                                )
                        else:
                            st.warning("⚠️ Belum ada file LHA fisik yang diunggah.")
                        st.markdown("---")
    else:
        st.warning("⚠️ Menu penyimpanan LHA dikhususkan untuk peran Admin SPI.")
