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

# Custom Styling UI
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    
    .header-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 22px 28px;
        border-radius: 12px;
        border-left: 6px solid #2563eb;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .header-title { font-size: 24px; font-weight: 700; color: #f8fafc; margin-bottom: 4px; }
    .header-subtitle { font-size: 13px; color: #94a3b8; }

    .metric-card {
        background: #1e293b; border-radius: 10px; padding: 16px 20px;
        border: 1px solid #334155; box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .metric-label { font-size: 12px; font-weight: 600; text-transform: uppercase; color: #94a3b8; }
    .metric-value { font-size: 26px; font-weight: 800; margin-top: 4px; margin-bottom: 2px; }
    .metric-sub { font-size: 12px; font-weight: 500; }

    .stButton>button { width: 100%; border-radius: 8px; font-weight: 600; height: 42px; }
</style>
""", unsafe_allow_html=True)

file_path = "Master_Database_Temuan_Audit_2024_2025_PSM_Ringkas.xlsx"
PIN_ADMIN = "1234"

@st.cache_data(ttl=5)
def load_data():
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal membaca database Excel: {e}")
        return pd.DataFrame()

df_master = load_data()

if not df_master.empty:
    # BANNER DENGAN JUDUL YANG DIMINTA
    st.markdown("""
    <div class="header-banner">
        <div class="header-title">📊 SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM</div>
        <div class="header-subtitle">Sistem Pemantauan Granular Hasil Audit Kepatuhan & Performansi — Internal Audit Unit</div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Filter Control
    st.sidebar.markdown("## 🎯 Filter Control Panel")
    st.sidebar.markdown("---")

    col_periode = "Tahun Audit" if "Tahun Audit" in df_master.columns else df_master.columns[3]
    periode_list = ["Semua Periode"] + sorted(list(df_master[col_periode].dropna().astype(str).unique()))
    selected_periode = st.sidebar.selectbox("📅 Periode Audit:", periode_list)

    col_bidang = "Bidang" if "Bidang" in df_master.columns else df_master.columns[5]
    bidang_list = ["Semua Bidang"] + sorted(list(df_master[col_bidang].dropna().astype(str).unique()))
    selected_bidang = st.sidebar.selectbox("🏢 Bidang Workgroup:", bidang_list)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔐 Akses Admin (Editor)")
    
    input_pin = st.sidebar.text_input("Masukkan PIN Admin untuk Edit Data:", type="password")
    
    if input_pin == PIN_ADMIN:
        st.sidebar.success("🔓 Akses Editor Aktif")
        mode_edit = st.sidebar.checkbox("✏️ Buka Mode Editor Status", value=True)
    elif input_pin != "":
        st.sidebar.error("❌ PIN Salah")
        mode_edit = False
    else:
        st.sidebar.info("🔒 Mode Read-Only (Hanya Lihat)")
        mode_edit = False

    # Filter Data
    df_filtered = df_master.copy()
    if selected_periode != "Semua Periode":
        df_filtered = df_filtered[df_filtered[col_periode].astype(str) == str(selected_periode)]
    if selected_bidang != "Semua Bidang":
        df_filtered = df_filtered[df_filtered[col_bidang].astype(str) == str(selected_bidang)]

    col_status = "Status" if "Status" in df_filtered.columns else "Status_TL"
    col_id = "ID Temuan" if "ID Temuan" in df_filtered.columns else df_filtered.columns[1]

    status_series = df_filtered[col_status].astype(str).str.upper()
    mask_sls = status_series.str.contains("SLS|SELESAI", na=False)
    mask_eval = status_series.str.contains("EVAL|EVALUASI", na=False)
    mask_bd = ~mask_sls & ~mask_eval

    total_temuan = df_filtered[col_id].nunique()
    total_rekomendasi = len(df_filtered)
    total_sls = int(mask_sls.sum())
    total_eval = int(mask_eval.sum())
    total_bd = int(mask_bd.sum())

    pct_sls = (total_sls / total_rekomendasi * 100) if total_rekomendasi > 0 else 0
    pct_eval = (total_eval / total_rekomendasi * 100) if total_rekomendasi > 0 else 0
    pct_bd = (total_bd / total_rekomendasi * 100) if total_rekomendasi > 0 else 0

    st.markdown("### 📈 Ringkasan Eksekutif KPI")
    m1, m2, m3, m4, m5 = st.columns(5)

    with m1:
        st.markdown(f'<div class="metric-card" style="border-top: 4px solid #3b82f6;"><div class="metric-label">Total Temuan</div><div class="metric-value" style="color: #f8fafc;">{total_temuan}</div><div class="metric-sub" style="color: #94a3b8;">Judul LHP Utama</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card" style="border-top: 4px solid #8b5cf6;"><div class="metric-label">Poin Rekomendasi</div><div class="metric-value" style="color: #f8fafc;">{total_rekomendasi}</div><div class="metric-sub" style="color: #94a3b8;">Butir Granular</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card" style="border-top: 4px solid #10b981;"><div class="metric-label">🟢 Selesai (SLS)</div><div class="metric-value" style="color: #34d399;">{total_sls}</div><div class="metric-sub" style="color: #10b981;">{pct_sls:.1f}% dari Total</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric-card" style="border-top: 4px solid #f59e0b;"><div class="metric-label">🟡 Evaluasi (EVAL)</div><div class="metric-value" style="color: #fbbf24;">{total_eval}</div><div class="metric-sub" style="color: #f59e0b;">{pct_eval:.1f}% Dalam Proses</div></div>', unsafe_allow_html=True)
    with m5:
        st.markdown(f'<div class="metric-card" style="border-top: 4px solid #ef4444;"><div class="metric-label">🔴 Overdue (BD)</div><div class="metric-value" style="color: #f87171;">{total_bd}</div><div class="metric-sub" style="color: #ef4444;">{pct_bd:.1f}% Belum TL</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("### 📊 Visualisasi Distribusi & Progres Tindak Lanjut")
    chart_col1, chart_col2 = st.columns([1.8, 1])

    summary_data = []
    for b in df_filtered[col_bidang].unique():
        sub = df_filtered[df_filtered[col_bidang] == b]
        s_series = sub[col_status].astype(str).str.upper()
        s_sls = s_series.str.contains("SLS|SELESAI", na=False).sum()
        s_eval = s_series.str.contains("EVAL|EVALUASI", na=False).sum()
        s_bd = len(sub) - s_sls - s_eval
        summary_data.append({'Bidang': b, 'Selesai (SLS)': s_sls, 'Evaluasi (EVAL)': s_eval, 'Belum TL (BD)': s_bd})
    df_chart = pd.DataFrame(summary_data)

    with chart_col1:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(y=df_chart['Bidang'], x=df_chart['Selesai (SLS)'], name='Selesai (SLS)', orientation='h', marker=dict(color='#10b981')))
        fig_bar.add_trace(go.Bar(y=df_chart['Bidang'], x=df_chart['Evaluasi (EVAL)'], name='Evaluasi (EVAL)', orientation='h', marker=dict(color='#f59e0b')))
        fig_bar.add_trace(go.Bar(y=df_chart['Bidang'], x=df_chart['Belum TL (BD)'], name='Belum TL (BD)', orientation='h', marker=dict(color='#ef4444')))
        fig_bar.update_layout(barmode='stack', title=dict(text="Progres Status per Bidang Workgroup", font=dict(size=14, color="#f8fafc")), height=260, margin=dict(l=10, r=10, t=35, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11, color="#94a3b8")), xaxis=dict(showgrid=True, gridcolor="#334155", tickfont=dict(color="#94a3b8")), yaxis=dict(autorange="reversed", tickfont=dict(color="#f8fafc", size=11)))
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        donut_data = pd.DataFrame({'Status': ['Selesai (SLS)', 'Evaluasi (EVAL)', 'Belum TL (BD)'], 'Jumlah': [total_sls, total_eval, total_bd]})
        fig_donut = px.pie(donut_data, values='Jumlah', names='Status', hole=0.6, color='Status', color_discrete_map={'Selesai (SLS)': '#10b981', 'Evaluasi (EVAL)': '#f59e0b', 'Belum TL (BD)': '#ef4444'})
        fig_donut.update_layout(title=dict(text="Proporsi Status Total", font=dict(size=14, color="#f8fafc")), height=260, margin=dict(l=10, r=10, t=35, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
        fig_donut.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_donut, use_container_width=True)

    st.write("---")

    if mode_edit:
        st.markdown("### ✏️ Interactive Editor Mode (Khusus Admin)")
        st.info("💡 Anda dapat mengubah status poin rekomendasi pada kolom **Status** di bawah ini, lalu klik tombol simpan.")
        edited_df = st.data_editor(
            df_filtered,
            column_config={"Status": st.column_config.SelectboxColumn("Status Tindak Lanjut", help="Pilih Status Rekomendasi", options=["SLS", "EVAL", "BD"], required=True)},
            disabled=["No", "ID Temuan", "Poin", "Tahun Audit", "Nama Entitas", "Bidang", "Judul Temuan Audit"],
            use_container_width=True, num_rows="fixed", height=400
        )
        if st.button("💾 SIMPAN PERUBAHAN STATUS KE EXCEL", type="primary"):
            df_master.update(edited_df)
            df_master.to_excel(file_path, sheet_name='Master Database Temuan', index=False)
            st.success("✅ Perubahan status berhasil diperbarui di database Excel!")
            st.rerun()
    else:
        st.markdown("### 🔍 Filter Detail Rincian Rekomendasi")
        b1, b2, b3, b4 = st.columns(4)
        show_sls = b1.button("🟢 REKOMENDASI SELESAI (SLS)")
        show_eval = b2.button("🟡 DALAM EVALUASI (EVAL)")
        show_bd = b3.button("🔴 OVERDUE / BELUM TL (BD)")
        show_all = b4.button("📋 TAMPILKAN SEMUA DATA")

        if show_sls:
            st.subheader("🟢 Rincian Poin Rekomendasi Status Selesai (SLS)")
            st.dataframe(df_filtered[mask_sls], use_container_width=True, height=400)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered[mask_sls].to_excel(writer, index=False, sheet_name='Data SLS')
            st.download_button("📥 Download Excel Data SLS (.xlsx)", output.getvalue(), "data_audit_selesai.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        elif show_eval:
            st.subheader("🟡 Rincian Poin Rekomendasi Status Dalam Evaluasi (EVAL)")
            st.dataframe(df_filtered[mask_eval], use_container_width=True, height=400)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered[mask_eval].to_excel(writer, index=False, sheet_name='Data Evaluasi')
            st.download_button("📥 Download Excel Data Evaluasi (.xlsx)", output.getvalue(), "data_audit_evaluasi.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        elif show_bd:
            st.subheader("🔴 Rincian Poin Rekomendasi Status Overdue / Belum Ditindaklanjuti (BD)")
            st.dataframe(df_filtered[mask_bd], use_container_width=True, height=400)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered[mask_bd].to_excel(writer, index=False, sheet_name='Data Overdue')
            st.download_button("📥 Download Excel Data Overdue (.xlsx)", output.getvalue(), "data_audit_overdue.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        else:
            st.subheader("📋 Tabel Master Rekapitulasi Data Granular")
            st.dataframe(df_filtered, use_container_width=True, height=400)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Master Data')
            st.download_button("📥 Download Seluruh Master Data Excel (.xlsx)", output.getvalue(), "master_data_audit.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

st.write("---")
st.caption("Internal Audit Unit (SPI) PT Pelindo Solusi Maritim © 2026")