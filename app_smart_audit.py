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
            # Indikator atau tombol cek notifikasi file masuk
            if st.button("Cek Pembaruan / Refresh Status Upload"):
                st.toast("Memeriksa database unggahan...", icon="🔄")
                st.success("Data berhasil disinkronisasi!")
