# --- FITUR UPLOAD OLEH AUDITEE + ARSIP FILE ---
    st.markdown("### 📤 Unggah Bukti Tindak Lanjut (Auditee)")
    uploaded_file = st.file_uploader("Pilih file bukti tindak lanjut (.pdf, .docx, .xlsx)", type=["pdf", "docx", "xlsx"], key="uploader_tl")
    
    if uploaded_file is not None:
        file_path = os.path.join(VAULT_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        current_unit = chosen_unit if access_role == "Auditee" else access_role
        waktu_sekarang = datetime.now().strftime("%d-%m-%Y %H:%M")
        
        new_note = {
            "waktu": waktu_sekarang,
            "bidang": current_unit,
            "filename": uploaded_file.name
        }
        if not st.session_state.notification_list or st.session_state.notification_list[-1]["filename"] != uploaded_file.name:
            st.session_state.notification_list.append(new_note)
            
        st.success(f"File {uploaded_file.name} berhasil diunggah!")

    # --- DAFTAR ARSIP FILE UNGGAHAN AUDITEE ---
    if st.session_state.notification_list:
        st.markdown("### 📂 Arsip Unggahan Bukti Tindak Lanjut")
        for note in st.session_state.notification_list:
            file_path = os.path.join(VAULT_DIR, note['filename'])
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📄 **{note['filename']}** | Diunggah oleh: *{note['bidang']}* pada {note['waktu']}")
            with col2:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button("📥 Unduh", f, file_name=note['filename'], key=f"btn_{note['filename']}_{note['waktu']}")
