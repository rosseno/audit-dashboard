# --- TABEL REKAPITULASI DENGAN BARIS JUMLAH BERWARNA ---
    if not df_base.empty:
        st.markdown("### Rekapitulasi Matriks Tindak Lanjut Hasil Audit")
        
        rekap_data = []
        unique_bidangs = sorted(df_base[col_bidang].dropna().astype(str).unique())
        
        tot_tem = 0
        tot_rek = 0
        tot_sls = 0
        tot_eval = 0
        tot_bd = 0
        tot_tptd = 0
        
        for idx, b in enumerate(unique_bidangs, 1):
            sub_df = df_base[df_base[col_bidang].astype(str) == str(b)]
            j_temuan = len(sub_df)
            j_selesai = len(sub_df[sub_df[col_status].str.contains("Selesai|SLS", case=False, na=False)])
            j_eval = len(sub_df[sub_df[col_status].str.contains("Evaluasi|EVAL", case=False, na=False)])
            j_bd = len(sub_df[sub_df[col_status].str.contains("Overdue|BD|Belum", case=False, na=False)])
            
            tot_tem += j_temuan
            tot_rek += j_temuan
            tot_sls += j_selesai
            tot_eval += j_eval
            tot_bd += j_bd
            
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
            
        # Baris Jumlah Total
        rekap_data.append({
            "No": "",
            "Objek Audit": "JUMLAH",
            "Jumlah Temuan": tot_tem,
            "Jumlah Rekomendasi": tot_rek,
            "Selesai (SLS)": tot_sls,
            "EVALUASI AUDITOR": tot_eval,
            "Belum Ditindaklanjuti (BD)": tot_bd,
            "TPTD": tot_tptd
        })
            
        df_rekap = pd.DataFrame(rekap_data)

        # Fungsi untuk mewarnai khusus baris terakhir (JUMLAH)
        def highlight_total_row(s):
            is_total = s['Objek Audit'] == 'JUMLAH'
            return ['background-color: rgba(30, 58, 138, 0.6); color: #60a5fa; font-weight: bold;' if is_total else '' for _ in s]

        styled_rekap = df_rekap.style.apply(highlight_total_row, axis=1)
        st.dataframe(styled_rekap, use_container_width=True, hide_index=True)
