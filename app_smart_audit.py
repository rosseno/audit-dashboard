# --- RINGKASAN EKSEKUTIF KPI (Fungsional) ---
    st.markdown("### Ringkasan Eksekutif KPI")
    
    # Inisialisasi session state untuk filter jika belum ada
    if 'kpi_filter' not in st.session_state:
        st.session_state.kpi_filter = "SEMUA"

    # Fungsi untuk mengubah filter
    def set_filter(val):
        st.session_state.kpi_filter = val

    # Menggunakan columns untuk kartu KPI yang bisa diklik
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
