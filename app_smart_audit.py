# --- PUSAT NOTIFIKASI LIVE UNTUK ADMIN/DIREKSI ---
if st.session_state.notification_list and access_role in ["Direktur Utama", "Admin SPI", "Direktur Operasi & Komersial"]:
    st.markdown("### 🔔 Pusat Notifikasi Unggah Dokumen Tindak Lanjut")
    for note in st.session_state.notification_list:
        file_path = os.path.join(VAULT_DIR, note['filename'])
        
        # Membuat wadah tampilan notifikasi
        st.markdown(f"""
        <div class="notification-box">
            📥 <b>{note['waktu']}</b> — Unit/Auditee <b>{note['bidang']}</b> telah mengunggah file bukti tindak lanjut: <b>{note['filename']}</b>
        </div>
        """, unsafe_allow_html=True)
        
        # Tombol unduh langsung di bawah notifikasi agar bisa di-klik
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.download_button(
                    label=f"📥 Klik untuk Unduh/Buka: {note['filename']}",
                    data=f,
                    file_name=note['filename'],
                    key=f"dl_note_{note['filename']}_{note['waktu']}"
                )
