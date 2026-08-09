# --- FITUR NOTIFIKASI & DAFTAR RINCIAN OVERDUE BERDASARKAN RENCANA DEPARTEMEN ---
current_month_idx = datetime.now().month  # Agustus 2026

if not df_base.empty:
    overdue_df = df_base[
        (~df_base[col_status].str.contains("Selesai|SLS", case=False, na=False)) & 
        (df_base[col_status].str.contains("Overdue|BD|Belum|Evaluasi|EVAL", case=False, na=False))
    ]
    
    overdue_count = len(overdue_df)
    if overdue_count > 0:
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; padding: 15px 20px; border-radius: 8px; margin-bottom: 10px; display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 24px;">🚨</div>
            <div>
                <div style="color: #f87171; font-weight: 700; font-size: 15px;">PERINGATAN SISTEM: ADA {overdue_count} REKOMENDASI MELEWATI BATAS RENCANA TINDAK LANJUT</div>
                <div style="color: #cbd5e1; font-size: 12px; margin-top: 3px;">Terdeteksi temuan dengan status Belum Selesai (BD/EVAL) yang telah melewati jadwal target rencana departemen tahun 2026.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Tombol expander untuk melihat daftar rincian rekomendasi yang overdue
        with st.expander("📋 Klik di sini untuk melihat daftar rincian temuan yang melewati batas rencana"):
            cols_show = [col for col in ["ID Temuan", col_bidang, "Temuan", "Rekomendasi", col_status] if col in overdue_df.columns]
            st.dataframe(overdue_df[cols_show], use_container_width=True, hide_index=True)

# KPI Interaktif ala Card 3D Hidup dengan Proporsi Sempurna
st.markdown("### Ringkasan Eksekutif KPI")
