# Header Banner dengan Logo di Pojok Kanan
col_banner_text, col_banner_logo = st.columns([4, 1])

with col_banner_text:
    st.markdown("""
    <div class="header-banner" style="margin-bottom: 0px;">
        <div class="header-title">SMART AUDIT MONITORING DASHBOARD - PT PELINDO SOLUSI MARITIM</div>
        <div class="header-subtitle">Sistem Pemantauan Granular Hasil Audit Kepatuhan & Performansi — Internal Audit Unit</div>
    </div>
    """, unsafe_allow_html=True)

with col_banner_logo:
    try:
        # Menampilkan gambar logo dari file lokal dengan lebar 180 pixel
        st.image("logo.png", width=180) 
    except:
        # Teks cadangan jika file gambar logo belum tersedia di folder
        st.markdown("<div style='text-align: right; color: #94a3b8; font-size: 12px; padding-top: 20px;'><b>LOGO PERusahaan</b></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
