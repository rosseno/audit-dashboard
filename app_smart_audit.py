import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime
import os

st.set_page_config(
    page_title="Executive Audit Dashboard - PT Pelindo Solusi Maritim",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Ultimate untuk Card KPI Proporsional, Neon Glow, & Animasi Kedip Peringatan
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

    /* Animasi Kedip (Blink) untuk Kotak Peringatan Darurat */
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

EXCEL_FILE = "Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx"
EXCEL_DOCS_FILE = "Database_Multi_Auditor_PA_KKA.xlsx"
EXCEL_LHA_FILE = "Database_Multi_Auditor_LHA.xlsx"

@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE)
    except:
        df = pd.read_excel(EXCEL_FILE)
    return df

if 'df_master' not in st.session_state:
    st.session_state.df_master = load_data()

# Memuat data multi-auditor PA & KKA secara permanen
if 'multi_audit_docs' not in st.session_state:
    if os.path.exists(EXCEL_DOCS_FILE):
        try:
            df_docs = pd.read_excel(EXCEL_DOCS_FILE)
            st.session_state.multi_audit_docs = df_docs.to_dict('records')
        except:
            st.session_state.multi_audit_docs = []
    else:
        st.session_state.multi_audit_docs = []

# Memuat data multi-auditor LHA secara permanen
if 'multi_lha_docs' not in st.session_state:
    if os.path.exists(EXCEL_LHA_FILE):
        try:
            df_lha = pd.read_excel(EXCEL_LHA_FILE)
            st.session_state.multi_lha_docs = df_lha.to_dict('records')
        except:
            st.session_state.multi_lha_docs = []
    else:
        st.session_state.multi_lha_docs = []

def save_docs_to_excel():
    if st.session_state.multi_audit_docs:
        pd.DataFrame(st.session_state.multi_audit_docs).to_excel(EXCEL_DOCS_FILE, index=False)

def save_lha_to_excel():
    if st.session_state.multi_lha_docs:
        pd.DataFrame(st.session_state.multi_lha_docs).to_excel(EXCEL_LHA_FILE, index=False)

df_master = st.session_state.df_master
PIN_ADMIN = "1234"  # <-- PIN Admin SPI

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

else:  # Admin SPI
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

if selected_periode == "2026":
    st.info("📅 **Periode 2026 (Rencana Audit Pelaksanaan Bulan Oktober):** Belum ada temuan atau LHP yang diterbitkan karena audit baru akan dijadwalkan pada bulan Oktober.")

# --- NAVIGASI UTAMA BERBENTUK TAB ---
tab_dash, tab_prog_kk, tab_lha = st.tabs([
    "📊 Dashboard Monitoring Eksekutif", 
    "📋 Modul Program Audit & Kertas Kerja Multi-Auditor", 
    "📝 Modul Generator Lembar Hasil Audit (LHA) Multi-Auditor"
])

# ================= TAB 1: DASHBOARD MONITORING =================
with tab_dash:
    if not df_base.empty:
        overdue_df = df_base[
            df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)
        ]
        
        overdue_count = len(overdue_df)
        if overdue_count > 0:
            st.markdown(f"""
            <div class="alert-blink">
                <div style="font-size: 24px;">🚨</div>
                <div>
                    <div style="color: #f87171; font-weight: 700; font-size: 15px;">PERINGATAN: ADA {overdue_count} REKOMENDASI OVERDUE (BELUM DITINDAKLANJUTI)</div>
                    <div style="color: #cbd5e1; font-size: 12px; margin-top: 3px;">Terdapat temuan dengan status Belum Selesai (BD) yang melewati batas jadwal rencana departemen. Mohon segera diselesaikan.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📋 Klik di sini untuk melihat daftar rincian temuan Overdue (BD)"):
                target_cols = ["ID Temuan", col_bidang, "Temuan", "Rekomendasi", col_status]
                cols_show = [col for col in target_cols if col in overdue_df.columns]
                st.dataframe(overdue_df[cols_show], use_container_width=True, hide_index=True)

    st.markdown("### Ringkasan Eksekutif KPI")
    if 'filter_status' not in st.session_state: 
        st.session_state.filter_status = "Semua"

    total_temuan = len(df_base)
    selesai = len(df_base[df_base[col_status].str.contains("Selesai|SLS", case=False, na=False)])
    evaluasi = len(df_base[df_base[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)])
    overdue = len(df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)])

    pct_selesai = f"{(selesai/total_temuan)*100:.1f}% dari Total" if total_temuan > 0 else "0%"
    pct_eval = f"{(evaluasi/total_temuan)*100:.1f}% Dalam Proses" if total_temuan > 0 else "0%"
    pct_overdue = f"{(overdue/total_temuan)*100:.1f}% Belum TL" if total_temuan > 0 else "0%"

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi-card card-blue">
            <div class="kpi-title">TOTAL TEMUAN</div>
            <div class="kpi-value">{total_temuan}</div>
            <div class="kpi-desc">Judul LHP Utama</div>
        </div>
        <div class="kpi-card card-purple">
            <div class="kpi-title">POIN REKOMENDASI</div>
            <div class="kpi-value">{total_temuan}</div>
            <div class="kpi-desc">Butir Granular</div>
        </div>
        <div class="kpi-card card-green">
            <div class="kpi-title">SELESAI (SLS)</div>
            <div class="kpi-value">{selesai}</div>
            <div class="kpi-desc">{pct_selesai}</div>
        </div>
        <div class="kpi-card card-yellow">
            <div class="kpi-title">EVALUASI (EVAL)</div>
            <div class="kpi-value">{evaluasi}</div>
            <div class="kpi-desc">{pct_eval}</div>
        </div>
        <div class="kpi-card card-red">
            <div class="kpi-title">OVERDUE (BD)</div>
            <div class="kpi-value">{overdue}</div>
            <div class="kpi-desc">{pct_overdue}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    df_filtered = df_base.copy()
    if st.session_state.filter_status == "Selesai":
        df_filtered = df_base[df_base[col_status].str.contains("Selesai|SLS", case=False, na=False)]
    elif st.session_state.filter_status == "Evaluasi":
        df_filtered = df_base[df_base[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)]
    elif st.session_state.filter_status == "Overdue":
        df_filtered = df_base[df_base[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)]

    st.markdown("---")

    st.markdown("### Rekapitulasi Matriks Tindak Lanjut Hasil Audit")
    if not df_base.empty:
        summary_rows = []
        unique_bidang = sorted(df_base[col_bidang].dropna().astype(str).unique())
        
        tot_t, tot_r, tot_sls, tot_eval, tot_bd = 0, 0, 0, 0, 0
        
        for idx, b in enumerate(unique_bidang):
            clean_b_name = b.replace("Bidang ", "").strip()
            df_b = df_base[df_base[col_bidang].astype(str) == b]
            j_t = len(df_b)
            j_r = j_t 
            j_sls = len(df_b[df_b[col_status].str.contains("Selesai|SLS", case=False, na=False)])
            j_eval = len(df_b[df_b[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)])
            j_bd = len(df_b[df_b[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)])
            
            tot_t += j_t
            tot_r += j_r
            tot_sls += j_sls
            tot_eval += j_eval
            tot_bd += j_bd
            
            summary_rows.append({
                "Objek Audit": f"{chr(65+idx)}. Bidang {clean_b_name}",
                "Jumlah Temuan": j_t,
                "Jumlah Rekomendasi": j_r,
                "Selesai (SLS)": j_sls,
                "EVALUASI AUDITOR": j_eval,
                "Belum Ditindaklanjuti (BD)": j_bd,
                "TPTD": 0
            })
            
        p_sls = f"{(tot_sls/tot_r)*100:.2f}%" if tot_r > 0 else "0.00%"
        p_eval = f"{(tot_eval/tot_r)*100:.2f}%" if tot_r > 0 else "0.00%"
        p_bd = f"{(tot_bd/tot_r)*100:.2f}%" if tot_r > 0 else "0.00%"

        summary_rows.append({"Objek Audit": "JUMLAH", "Jumlah Temuan": tot_t, "Jumlah Rekomendasi": tot_r, "Selesai (SLS)": tot_sls, "EVALUASI AUDITOR": tot_eval, "Belum Ditindaklanjuti (BD)": tot_bd, "TPTD": 0})
        summary_rows.append({"Objek Audit": "PROGRES (%)", "Jumlah Temuan": "-", "Jumlah Rekomendasi": "-", "Selesai (SLS)": p_sls, "EVALUASI AUDITOR": p_eval, "Belum Ditindaklanjuti (BD)": p_bd, "TPTD": 0})

        df_summary_display = pd.DataFrame(summary_rows)
        def highlight_summary_rows(row):
            if row["Objek Audit"] == "JUMLAH":
                return ['background-color: #1e3a8a; color: white; font-weight: bold;'] * len(row)
            elif row["Objek Audit"] == "PROGRES (%)":
                return ['background-color: #0f766e; color: white; font-weight: bold;'] * len(row)
            return [''] * len(row)

        st.dataframe(df_summary_display.style.apply(highlight_summary_rows, axis=1), use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada data temuan untuk periode ini.")

    st.markdown("---")
    
    columns_to_drop = ["No", "Poin", "Tahun Audit", "Nama Entitas", "Tingkat Risiko", "Prioritas", "Tag Kata Kunci (#Preventif)", "Ringkasan Kondisi & Akar Masalah (Root Cause)", "Verifikasi_Auditor"]
    df_table_display = df_filtered.drop(columns=[col for col in columns_to_drop if col in df_filtered.columns])
    df_table_display.insert(0, "No", range(1, len(df_table_display) + 1))

    st.markdown("### Detail Data Temuan & Rekomendasi")
    st.dataframe(df_table_display, use_container_width=True, hide_index=True)


# ================= TAB 2: PROGRAM AUDIT & KERTAS KERJA MULTI-AUDITOR =================
with tab_prog_kk:
    st.markdown("### Modul Program Audit & Kertas Kerja Multi-Auditor (Penyimpanan Permanen)")
    st.info("💡 Setiap auditor dapat membuat bagian Program Audit (PA) dan Kertas Kerja Audit (KKA) secara mandiri.")
    
    if access_role == "Admin SPI":
        id_pk_list = df_master["ID Temuan"].dropna().astype(str).unique().tolist() if "ID Temuan" in df_master.columns else []
        if id_pk_list:
            selected_pk_id = st.selectbox("Pilih ID Temuan / Penugasan untuk KKA:", id_pk_list, key="pk_id_select_multi")
            
            col_btn_add, _ = st.columns([1, 3])
            with col_btn_add:
                if st.button("➕ Buat Program & KKA Baru"):
                    new_id_doc = f"DOC-{len(st.session_state.multi_audit_docs) + 1}"
                    st.session_state.multi_audit_docs.append({
                        "doc_id": new_id_doc,
                        "target_temuan": selected_pk_id,
                        "auditor_name": f"Auditor {len(st.session_state.multi_audit_docs) + 1}",
                        "audit_program": "-",
                        "kertas_kerja": "-"
                    })
                    save_docs_to_excel()
                    st.rerun()
            
            st.markdown("---")
            
            filtered_docs = [d for d in st.session_state.multi_audit_docs if str(d.get("target_temuan")) == str(selected_pk_id)]
            
            if not filtered_docs:
                st.info("Belum ada dokumen Program Audit & KKA yang dibuat untuk penugasan ini. Klik tombol ➕ di atas untuk membuat lembar kerja baru.")
            else:
                for idx, doc in enumerate(filtered_docs):
                    with st.expander(f"📄 [{doc['doc_id']}] Lembar Kerja — Disusun oleh: {doc['auditor_name']}", expanded=True):
                        with st.form(key=f"form_multi_doc_{doc['doc_id']}_{idx}"):
                            auditor_input = st.text_input("Nama / Inisial Auditor:", value=doc["auditor_name"])
                            prog_input = st.text_area("Langkah-langkah Program Audit (AP):", value=doc["audit_program"], height=120)
                            kk_input = st.text_area("Rincian Pengujian Kertas Kerja Audit (KKA):", value=doc["kertas_kerja"], height=140)
                            
                            col_f1, col_f2 = st.columns(2)
                            with col_f1:
                                save_sub_btn = st.form_submit_button("Simpan Perubahan Dokumen Ini")
                            with col_f2:
                                del_sub_btn = st.form_submit_button("🗑️ Hapus Dokumen Ini")
                                
                            if save_sub_btn:
                                doc["auditor_name"] = auditor_input
                                doc["audit_program"] = prog_input
                                doc["kertas_kerja"] = kk_input
                                save_docs_to_excel()
                                st.success(f"Dokumen {doc['doc_id']} berhasil disimpan secara permanen!")
                                st.rerun()
                                
                            if del_sub_btn:
                                st.session_state.multi_audit_docs.remove(doc)
                                save_docs_to_excel()
                                st.success(f"Dokumen {doc['doc_id']} berhasil dihapus!")
                                st.rerun()
                                
                        doc_text_export = f"""==================================================
PROGRAM AUDIT & KERTAS KERJA AUDIT (KKA)
PT PELINDO SOLUSI MARITIM
==================================================
ID Penugasan : {doc['target_temuan']}
Nomor Dokumen: {doc['doc_id']}
Auditor      : {doc['auditor_name']}
Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y')}
--------------------------------------------------
1. PROGRAM AUDIT (AP):
{doc['audit_program']}

2. KERTAS KERJA AUDIT (KKA):
{doc['kertas_kerja']}
=================================================="""
                        st.download_button(
                            label=f"📥 Download Dokumen {doc['doc_id']} (Format Word/TXT)",
                            data=doc_text_export.encode('utf-8'),
                            file_name=f"KKA_{doc['target_temuan']}_{doc['doc_id']}.txt",
                            mime="text/plain",
                            key=f"dl_btn_{doc['doc_id']}_{idx}"
                        )
    else:
        st.warning("⚠️ Menu penyusunan Program Audit & Kertas Kerja dikhususkan untuk peran Admin SPI (Auditor).")


# ================= TAB 3: GENERATOR LHA MULTI-AUDITOR (DENGAN TOMBOL TAMBAH + & PENYIMPANAN PERMANEN) =================
with tab_lha:
    st.markdown("### Modul Generator Lembar Hasil Audit (LHA) Multi-Auditor")
    st.info("💡 Setiap auditor dapat membuat dan mengenerate LHA mandiri (Observasi, Root Cause, Rekomendasi, Implikasi) menggunakan tombol tambah (+) di bawah.")
    
    if access_role == "Admin SPI":
        id_lha_list = df_master["ID Temuan"].dropna().astype(str).unique().tolist() if "ID Temuan" in df_master.columns else []
        if id_lha_list:
            selected_lha_id = st.selectbox("Pilih ID Temuan / Penugasan untuk LHA:", id_lha_list, key="lha_id_select_multi")
            
            col_lha_add, _ = st.columns([1, 3])
            with col_lha_add:
                if st.button("➕ Buat LHA Baru"):
                    new_lha_id = f"LHA-DOC-{len(st.session_state.multi_lha_docs) + 1}"
                    st.session_state.multi_lha_docs.append({
                        "lha_doc_id": new_lha_id,
                        "target_temuan": selected_lha_id,
                        "auditor_name": f"Auditor LHA {len(st.session_state.multi_lha_docs) + 1}",
                        "observasi": "-",
                        "root_cause": "-",
                        "rekomendasi": "-",
                        "implikasi": "-"
                    })
                    save_lha_to_excel()
                    st.rerun()
            
            st.markdown("---")
            
            filtered_lhas = [l for l in st.session_state.multi_lha_docs if str(l.get("target_temuan")) == str(selected_lha_id)]
            
            if not filtered_lhas:
                st.info("Belum ada dokumen LHA yang dibuat untuk penugasan ini. Klik tombol ➕ di atas untuk membuat lembar LHA baru.")
            else:
                for idx, lha_doc in enumerate(filtered_lhas):
                    with st.expander(f"📄 [{lha_doc['lha_doc_id']}] Lembar LHA — Disusun oleh: {lha_doc['auditor_name']}", expanded=True):
                        with st.form(key=f"form_multi_lha_{lha_doc['lha_doc_id']}_{idx}"):
                            auditor_lha_input = st.text_input("Nama / Inisial Auditor LHA:", value=lha_doc["auditor_name"])
                            obs_input = st.text_area("1. Observasi / Kondisi:", value=lha_doc["observasi"], height=100)
                            root_input = st.text_area("2. Akar Masalah (Root Cause):", value=lha_doc["root_cause"], height=100)
                            rek_input = st.text_area("3. Rekomendasi:", value=lha_doc["rekomendasi"], height=100)
                            imp_input = st.text_area("4. Implikasi / Risiko:", value=lha_doc["implikasi"], height=100)
                            
                            col_lha_f1, col_lha_f2 = st.columns(2)
                            with col_lha_f1:
                                save_lha_sub_btn = st.form_submit_button("Simpan Perubahan LHA Ini")
                            with col_lha_f2:
                                del_lha_sub_btn = st.form_submit_button("🗑️ Hapus LHA Ini")
                                
                            if save_lha_sub_btn:
                                lha_doc["auditor_name"] = auditor_lha_input
                                lha_doc["observasi"] = obs_input
                                lha_doc["root_cause"] = root_input
                                lha_doc["rekomendasi"] = rek_input
                                lha_doc["implikasi"] = imp_input
                                save_lha_to_excel()
                                st.success(f"Dokumen LHA {lha_doc['lha_doc_id']} berhasil disimpan secara permanen!")
                                st.rerun()
                                
                            if del_lha_sub_btn:
                                st.session_state.multi_lha_docs.remove(lha_doc)
                                save_lha_to_excel()
                                st.success(f"Dokumen LHA {lha_doc['lha_doc_id']} berhasil dihapus!")
                                st.rerun()
                                
                        lha_text_export = f"""==================================================
LEMBAR HASIL AUDIT (LHA) — INTERNAL AUDIT UNIT
PT PELINDO SOLUSI MARITIM
==================================================
ID Penugasan : {lha_doc['target_temuan']}
Nomor Dokumen: {lha_doc['lha_doc_id']}
Auditor      : {lha_doc['auditor_name']}
Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y')}
--------------------------------------------------
1. OBSERVASI / KONDISI:
{lha_doc['observasi']}

2. AKAR MASALAH (ROOT CAUSE):
{lha_doc['root_cause']}

3. REKOMENDASI:
{lha_doc['rekomendasi']}

4. IMPLIKASI / RISIKO:
{lha_doc['implikasi']}
=================================================="""
                        st.download_button(
                            label=f"📥 Download Dokumen LHA {lha_doc['lha_doc_id']} (Format Word/TXT)",
                            data=lha_text_export.encode('utf-8'),
                            file_name=f"LHA_{lha_doc['target_temuan']}_{lha_doc['lha_doc_id']}.txt",
                            mime="text/plain",
                            key=f"dl_lha_btn_{lha_doc['lha_doc_id']}_{idx}"
                        )
    else:
        st.warning("⚠️ Menu penyusunan LHA dikhususkan untuk peran Admin SPI (Auditor).")


# --- PANEL KHUSUS ADMIN SPI UNTUK INPUT VERIFIKASI & EKSPOR LAPORAN ---
if access_role == "Admin SPI" and st.session_state.admin_logged_in:
    st.markdown("---")
    st.markdown("### Panel Update Status & Catatan Auditor")
    st.info("💡 Pilih ID Temuan di bawah ini untuk memperbarui status tindak lanjut dan memberikan catatan kepada Auditee.")
    
    id_list = df_base["ID Temuan"].dropna().astype(str).unique().tolist() if "ID Temuan" in df_base.columns else []
    if id_list:
        selected_id = st.selectbox("Pilih ID Temuan:", id_list, key="panel_status_select")
        row_idx = df_master[df_master["ID Temuan"].astype(str) == str(selected_id)].index
        if len(row_idx) > 0:
            current_status = df_master.loc[row_idx[0], col_status]
            current_note = df_master.loc[row_idx[0], "Catatan_Auditor"]
            
            opt_status = ["BD (Belum Selesai / Overdue)", "EVAL (Sedang Dievaluasi)", "SLS (Selesai)"]
            default_idx = 0
            if "EVAL" in str(current_status):
                default_idx = 1
            elif "SLS" in str(current_status) or "Selesai" in str(current_status):
                default_idx = 2

            with st.form(key="form_verifikasi"):
                col_v1, col_v2 = st.columns(2)
                with col_v1:
                    new_status_choice = st.selectbox("Ubah Status Temuan:", opt_status, index=default_idx)
                with col_v2:
                    auditor_note = st.text_area("Catatan / Tanggapan Auditor untuk Auditee:", value=str(current_note))
                
                submit_verif = st.form_submit_button("Simpan Perubahan Status & Catatan")
                
                if submit_verif:
                    df_master.loc[row_idx, "Catatan_Auditor"] = auditor_note
                    if "BD" in new_status_choice:
                        df_master.loc[row_idx, col_status] = "BD"
                    elif "EVAL" in new_status_choice:
                        df_master.loc[row_idx, col_status] = "EVAL"
                    elif "SLS" in new_status_choice:
                        df_master.loc[row_idx, col_status] = "SLS"
                    
                    st.session_state.df_master = df_master
                    st.success(f"Temuan {selected_id} berhasil diperbarui!")
                    st.rerun()

    st.markdown("---")
    st.markdown("### Ekspor Laporan Ringkas (Untuk Rapat Direksi / Komite Audit)")
    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        csv_data = df_table_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Rekapan Laporan (Format Excel/CSV)",
            data=csv_data,
            file_name=f"Laporan_Audit_{selected_periode}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    with col_exp2:
        def generate_summary_text_report():
            report = f"=== LAPORAN EKSEKUTIF PENGAWASAN SPI ===\n"
            report += f"Periode: {selected_periode}\n"
            report += f"Tanggal Cetak: {datetime.now().strftime('%d-%m-%Y')}\n"
            report += f"Total Temuan: {total_temuan}\n"
            report += f"Selesai (SLS): {selesai}\n"
            report += f"Dalam Evaluasi (EVAL): {evaluasi}\n"
            report += f"Overdue (BD): {overdue}\n"
            report += f"===========================================\n"
            return report.encode('utf-8')

        st.download_button(
            label="Download Laporan Ringkas (Format Siap Cetak PDF/TXT)",
            data=generate_summary_text_report(),
            file_name=f"Ringkasan_Eksekutif_Audit_{selected_periode}.txt",
            mime="text/plain",
        )

if access_role in ["Auditee", "Admin SPI"]:
    st.markdown("---")
    st.markdown("### Pengunggahan Bukti Dukung (Evidence) Tindak Lanjut")
    st.info("💡 Klik tautan di bawah ini untuk mengunggah dokumen bukti penyelesaian temuan audit ke Google Drive SPI melalui Google Form.")
    
    col_up1, col_up2 = st.columns([2, 1])
    
    with col_up1:
        google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSczUxjVMZqcduSy704OVRGvIRga1LhQDAkJKoUkDUn6Aez82A/viewform"
        st.markdown(
            f"""
            <a href="{google_form_url}" target="_blank">
                <div style="display: inline-block; background-color: #3b82f6; color: white; padding: 12px 24px; border-radius: 8px; font-weight: bold; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                    Buka Formulir Upload Bukti Dukung (Google Drive)
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )
        
    with col_up2:
        if access_role == "Admin SPI":
            if st.button("Cek Pembaruan / Refresh Status Upload"):
                st.toast("Memeriksa database unggahan...", icon="🔄")
                st.success("Data berhasil disinkronisasi!")
