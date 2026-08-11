# --- TABEL REKAPITULASI BERWARNA & ELEGAN ---
    if not df_base.empty:
        st.markdown("### Rekapitulasi Matriks Tindak Lanjut Hasil Audit")
        
        rekap_data = []
        unique_bidangs = sorted(df_base[col_bidang].dropna().astype(str).unique())
        
        for idx, b in enumerate(unique_bidangs, 1):
            sub_df = df_base[df_base[col_bidang].astype(str) == str(b)]
            j_temuan = len(sub_df)
            j_selesai = len(sub_df[sub_df[col_status].str.contains("Selesai|SLS", case=False, na=False)])
            j_eval = len(sub_df[sub_df[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)])
            j_bd = len(sub_df[sub_df[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)])
            
            rekap_data.append({
                "No": chr(64 + idx),
                "Objek Audit": f"Bidang {b}",
                "Jumlah Temuan": j_temuan,
                "Jumlah Rekomendasi": j_temuan,
                "Selesai (SLS)": j_selesai,
                "EVALUASI AUDITOR": j_eval,
                "Belum Ditindaklanjuti (BD)": j_bd,
                "TPTD": 0
            })
            
        df_rekap = pd.DataFrame(rekap_data)

        # Fungsi Pewarnaan Otomatis (Styling)
        def color_coding(val, col_name):
            if col_name == "Selesai (SLS)" and val > 0:
                return 'background-color: rgba(16, 185, 129, 0.25); color: #34d399; font-weight: bold;'
            elif col_name == "EVALUASI AUDITOR" and val > 0:
                return 'background-color: rgba(245, 158, 11, 0.25); color: #fbbf24; font-weight: bold;'
            elif col_name == "Belum Ditindaklanjuti (BD)" and val > 0:
                return 'background-color: rgba(239, 68, 68, 0.25); color: #f87171; font-weight: bold;'
            return ''

        # Terapkan styling ke tabel
        styled_rekap = df_rekap.style.apply(lambda col: [color_coding(v, col.name) for v in col], subset=["Selesai (SLS)", "EVALUASI AUDITOR", "Belum Ditindaklanjuti (BD)"])
        
        st.dataframe(styled_rekap, use_container_width=True, hide_index=True)
