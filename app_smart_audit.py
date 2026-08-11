# --- DAFTAR ARSIP FILE UNGGAHAN AUDITEE DENGAN FITUR HAPUS ---
    if st.session_state.notification_list:
        st.markdown("### 📂 Arsip Unggahan Bukti Tindak Lanjut")
        
        # Iterasi menggunakan index untuk mempermudah penghapusan
        for i, note in enumerate(st.session_state.notification_list):
            file_path = os.path.join(VAULT_DIR, note['filename'])
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"📄 **{note['filename']}** | Diunggah: *{note['bidang']}* pada {note['waktu']}")
            
            with col2:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button("📥 Unduh", f, file_name=note['filename'], key=f"btn_dl_{i}")
            
            with col3:
                # Tombol hapus
                if st.button("🗑️ Hapus", key=f"btn_del_{i}"):
                    # 1. Hapus file fisik dari folder server
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    
                    # 2. Hapus dari daftar notifikasi di session_state
                    st.session_state.notification_list.pop(i)
                    
                    # 3. Rerun untuk memperbarui tampilan
                    st.rerun()
