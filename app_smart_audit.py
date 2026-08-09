# --- TABEL REKAPITULASI MATRIKS AUDIT MENGGUNAKAN HTML KUSTOM (FONT BESAR) ---
st.markdown("### 📑 Rekapitulasi Matriks Tindak Lanjut Hasil Audit")
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
            "Belum Sesuai (BS)": j_eval,
            "Belum Ditindaklanjuti (BD)": j_bd,
            "TPTD": 0
        })
        
    p_sls = f"{(tot_sls/tot_r)*100:.2f}" if tot_r > 0 else "0.00"
    p_eval = f"{(tot_eval/tot_r)*100:.2f}" if tot_r > 0 else "0.00"
    p_bd = f"{(tot_bd/tot_r)*100:.2f}" if tot_r > 0 else "0.00"

    rows_html = ""
    for row in summary_rows:
        rows_html += f"""
        <tr style="border-bottom: 1px solid #30363d;">
            <td style="padding: 16px; text-align: left; font-size: 20px; border-right: 1px solid #30363d;">{row['Objek Audit']}</td>
            <td style="padding: 16px; text-align: center; font-size: 20px; border-right: 1px solid #30363d;">{row['Jumlah Temuan']}</td>
            <td style="padding: 16px; text-align: center; font-size: 20px; border-right: 1px solid #30363d;">{row['Jumlah Rekomendasi']}</td>
            <td style="padding: 16px; text-align: center; font-size: 20px; border-right: 1px solid #30363d;">{row['Selesai (SLS)']}</td>
            <td style="padding: 16px; text-align: center; font-size: 20px; border-right: 1px solid #30363d;">{row['Belum Sesuai (BS)']}</td>
            <td style="padding: 16px; text-align: center; font-size: 20px; border-right: 1px solid #30363d;">{row['Belum Ditindaklanjuti (BD)']}</td>
            <td style="padding: 16px; text-align: center; font-size: 20px;">{row['TPTD']}</td>
        </tr>
        """

    html_table = f"""
    <div style="width: 100%; overflow-x: auto; margin-bottom: 20px;">
        <table style="width: 100%; border-collapse: collapse; background-color: #161b22; color: #ffffff; font-family: sans-serif; border: 1px solid #30363d;">
            <thead>
                <tr style="background-color: #21262d; border-bottom: 2px solid #30363d;">
                    <th style="padding: 16px; text-align: left; font-size: 20px; font-weight: bold; border-right: 1px solid #30363d;">Objek Audit</th>
                    <th style="padding: 16px; text-align: center; font-size: 20px; font-weight: bold; border-right: 1px solid #30363d;">Jumlah Temuan</th>
                    <th style="padding: 16px; text-align: center; font-size: 20px; font-weight: bold; border-right: 1px solid #30363d;">Jumlah Rekomendasi</th>
                    <th style="padding: 16px; text-align: center; font-size: 20px; font-weight: bold; border-right: 1px solid #30363d;">Selesai (SLS)</th>
                    <th style="padding: 16px; text-align: center; font-size: 20px; font-weight: bold; border-right: 1px solid #30363d;">Belum Sesuai (BS)</th>
                    <th style="padding: 16px; text-align: center; font-size: 20px; font-weight: bold; border-right: 1px solid #30363d;">Belum Ditindaklanjuti (BD)</th>
                    <th style="padding: 16px; text-align: font-size: 20px; font-weight: bold;">TPTD</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
                <tr style="background-color: #1e3a8a; border-bottom: 1px solid #30363d; font-weight: bold;">
                    <td style="padding: 18px; text-align: left; font-size: 22px; border-right: 1px solid #30363d;">JUMLAH</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">{tot_t}</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">{tot_r}</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">{tot_sls}</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">{tot_eval}</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">{tot_bd}</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px;">0</td>
                </tr>
                <tr style="background-color: #0f766e; font-weight: bold;">
                    <td style="padding: 18px; text-align: left; font-size: 22px; border-right: 1px solid #30363d;">PROGRES (%)</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">-</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">-</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">{p_sls}</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">{p_eval}</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px; border-right: 1px solid #30363d;">{p_bd}</td>
                    <td style="padding: 18px; text-align: center; font-size: 22px;">0</td>
                </tr>
            </tbody>
        </table>
    </div>
    """
    
    st.markdown(html_table, unsafe_allow_html=True)
else:
    st.info("Tidak ada data untuk ditampilkan dalam matriks rekapitulasi.")
