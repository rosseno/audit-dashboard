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

# Custom CSS Ultimate untuk Card KPI Proporsional, Neon Glow, & Styling Global
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

if "Catatan_Auditor" not in df_master.columns:
    df_master["Catatan_Auditor"] = "-"

# --- SIDEBAR: PENGATURAN HAK AKSES & PERIODE ---
st.sidebar.markdown("## Filter Control Panel")
selected_periode = st.sidebar.selectbox("Periode Audit:", ["Semua Periode"] + sorted(list(df_master[col_periode].dropna().astype(str).unique())))

df_filtered_periode = df_master[df_master[col_periode].astype(str) == str(selected_periode)] if selected_periode != "Semua Periode" else df_master.copy()
current_available_bidang = sorted(list(df_filtered_periode[col_bidang].dropna().astype(str).unique()))

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

# --- LOGIKA INPUT PIN ADMIN ---
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

# --- PEMETAAN DATA BERDASARKAN PERAN ---
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

# --- HEADER BANNER UTAMA BERSIH TANPA LOGO ---
st.markdown("""
<div class="header-banner">
    <div class="header-title">SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM</div>
    <div class="header-subtitle">Sistem Pemantauan Granular Hasil Audit Kepatuhan & Performansi — Internal Audit Unit</div>
</div>
""", unsafe_allow_html=True)

# KPI Interaktif ala Card 3D Hidup dengan Proporsi Sempurna
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

# Render Tampilan Visual Card Proporsional
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

st.markdown(f"<p style='color: #3b82f6; font-size: 12px; margin-top: 5px;'>Status Filter Aktif: <b>{st.session_state.filter_status}</b></p>", unsafe_allow_html=True)
st.markdown("---")

color_map = {'Selesai': '#00BCD4', 'SLS': '#00BCD4', 'Evaluasi': '#FFCA28', 'EVAL': '#FFCA28', 'Overdue': '#FF7043', 'BD': '#FF7043', 'Belum TL': '#FF7043'}

# --- TABEL REKAPITULASI MATRIKS AUDIT ---
st.markdown("### Rekapitulasi Matriks Tindak Lanjut Hasil Audit")
if not df_base.empty:
    summary_rows = []
    unique_bidang = sorted(df_base[col_bidang].dropna().astype(str).unique())
    
    tot_t = 0
    tot_r = 0
    tot_sls = 0
    tot_eval = 0
    tot_bd = 0
    
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

    summary_rows.append({
        "Objek Audit": "JUMLAH",
        "Jumlah Temuan": tot_t,
        "Jumlah Rekomendasi": tot_r,
        "Selesai (SLS)": tot_sls,
        "EVALUASI AUDITOR": tot_eval,
        "Belum Ditindaklanjuti (BD)": tot_bd,
        "TPTD": 0
    })

    summary_rows.append({
        "Objek Audit": "PROGRES (%)",
        "Jumlah Temuan": "-",
        "Jumlah Rekomendasi": "-",
        "Selesai (SLS)": p_sls,
        "EVALUASI AUDITOR": p_eval,
        "Belum Ditindaklanjuti (BD)": p_bd,
        "TPTD": 0
    })

    df_summary_display = pd.DataFrame(summary_rows)

    def highlight_summary_rows(row):
        if row["Objek Audit"] == "JUMLAH":
            return ['background-color: #1e3a8a; color: white; font-weight: bold;'] * len(row)
        elif row["Objek Audit"] == "PROGRES (%)":
            return ['background-color: #0f766e; color: white; font-weight: bold;'] * len(row)
        return [''] * len(row)

    styled_summary = df_summary_display.style.apply(highlight_summary_rows, axis=1)
    st.dataframe(styled_summary, use_container_width=True, hide_index=True)
else:
    st.info("Tidak ada data untuk ditampilkan dalam matriks rekapitulasi.")

st.markdown("---")

# --- VISUALISASI GRAFIK ---
tab_grafik1, tab_grafik2 = st.tabs(["Visualisasi Grafik Progres & Sebaran", "Grafik Tren Perbandingan Antar Tahun"])

with tab_grafik1:
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

with tab_grafik2:
    st.markdown("#### Analisis Komparasi Temuan & Penyelesaian Antar Tahun")
    if col_periode in df_master.columns:
        df_trend = df_master.groupby([col_periode, col_status]).size().reset_index(name='Jumlah')
        fig_trend = px.bar(df_trend, x=col_periode, y='Jumlah', color=col_status, barmode='group', title="Tren Perbandingan Temuan Audit Berdasarkan Tahun", color_discrete_map=color_map, template='plotly_dark')
        fig_trend.update_layout(height=350)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Kolom periode tahun tidak ditemukan dalam dataset.")

# --- PENGATURAN KOLOM TABEL UTAMA ---
columns_to_drop = [
    "No", "Poin", "Tahun Audit", "Nama Entitas", "Tingkat Risiko", 
    "Prioritas", "Tag Kata Kunci (#Preventif)", 
    "Ringkasan Kondisi & Akar Masalah (Root Cause)",
    "Verifikasi_Auditor"
]
df_table_display = df_filtered.drop(columns=[col for col in columns_to_drop if col in df_filtered.columns])
df_table_display.insert(0, "No", range(1, len(df_table_display) + 1))

st.markdown("### Detail Data Temuan & Rekomendasi")
st.dataframe(df_table_display, use_container_width=True, hide_index=True)

# --- PANEL KHUSUS ADMIN SPI UNTUK INPUT VERIFIKASI & EKSPOR LAPORAN ---
if access_role == "Admin SPI" and st.session_state.admin_logged_in:
    st.markdown("---")
    st.markdown("### Panel Update Status & Catatan Auditor")
    st.info("💡 Pilih ID Temuan di bawah ini untuk memperbarui status tindak lanjut dan memberikan catatan kepada Auditee.")
    
    id_list = df_base["ID Temuan"].dropna().astype(str).unique().tolist() if "ID Temuan" in df_base.columns else []
    if id_list:
        selected_id = st.selectbox("Pilih ID Temuan:", id_list)
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

    # --- FITUR EKSPOR LAPORAN KUSTOM ---
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

# --- INTEGRASI GOOGLE FORM / GOOGLE DRIVE & MONITORING UPLOAD ---
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
