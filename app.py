import pandas as pd
import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Audit Control - Integrasi Bukti Tindak Lanjut", layout="wide"
)

# ------------------------------------------------------------------
# 1. SIMULASI DATABASE REKOMENDASI TEMUAN PER BIDANG
# (Ganti/hubungkan bagian ini dengan database atau dataframe Anda)
# ------------------------------------------------------------------
data_temuan_per_bidang = {
    "Bidang Pemasaran": [
        "Database Realisasi Pekerjaan dan Harga Bahan dan Upah docking.",
        "Evaluasi Perjanjian Kerjasama Mitra Pemasaran dan Agen",
        "Laporan Monitoring Target Penjualan dan Realisasi Semester Lalu",
    ],
    "Bidang Keuangan": [
        "Rekonsiliasi Bank Bulanan dan Daftar Outstanding Cek",
        "Dokumen Pertanggungjawaban Kas Kecil dan SPJ",
    ],
    "Bidang SDM": [
        "Dokumen Evaluasi Key Performance Indicator (KPI) Pegawai",
        "Rekapitulasi Kehadiran, Cuti, dan Lembur Pegawai",
    ],
    "Bidang Operasional": [
        "Berita Acara Opname Fisik Persediaan Gudang",
        "Laporan Pemeliharaan dan Perawatan Mesin/Alat Produksi",
    ],
}

# ------------------------------------------------------------------
# 2. SIDEBAR NAVIGASI & FILTER
# ------------------------------------------------------------------
st.sidebar.markdown("### **AUDIT CONTROL**")
st.sidebar.markdown("---")

pilihan_peran = st.sidebar.selectbox("Pilih Peran / Jabatan:", ["Auditee", "Auditor", "Admin"])
periode_tahun = st.sidebar.selectbox("Periode Tahun Audit:", ["2026", "2025", "2024"])

# Pilihan Unit (Kunci filter bidang)
daftar_unit = list(data_temuan_per_bidang.keys())
pilih_unit = st.sidebar.selectbox("Pilih Unit:", daftar_unit)

pilih_menu = st.sidebar.selectbox("Pilih Menu Utama:", ["Upload Dokumen", "Dashboard", "Monitoring TL"])

# ------------------------------------------------------------------
# 3. KONTROL UTAMA HALAMAN (UPLOAD DOKUMEN)
# ------------------------------------------------------------------
st.markdown("## 🔗 Integrasi Bukti Tindak Lanjut ke Google Drive")
st.write(
    f"Auditee dari **{pilih_unit}** dapat melampirkan tautan Google Drive berisi dokumen bukti tindak lanjut temuan audit."
)

# Filter judul rekomendasi temuan berdasarkan unit yang dipilih di sidebar
list_rekomendasi_tersedia = data_temuan_per_bidang.get(pilih_unit, [])

# Formulir Input
with st.form("form_upload_tl"):
    if list_rekomendasi_tersedia:
        selected_rekomendasi = st.selectbox(
            "Pilih Rekomendasi Temuan:", list_rekomendasi_tersedia
        )
    else:
        st.warning(f"Tidak ada rekomendasi temuan yang tersedia untuk {pilih_unit}.")
        selected_rekomendasi = None

    google_drive_link = st.text_input(
        "Masukkan Link Google Drive (Folder/File Bukti Tindak Lanjut):",
        placeholder="https://drive.google.com/drive/folders/...",
    )

    submit_button = st.form_submit_button("Simpan Tautan Google Drive")

    if submit_button:
        if not selected_rekomendasi:
            st.error("Silakan pilih rekomendasi temuan terlebih dahulu.")
        elif not google_drive_link:
            st.error("Mohon masukkan tautan Google Drive terlebih dahulu.")
        else:
            # Di sini Anda bisa menambahkan logika untuk menyimpan ke database/file CSV/Excel
            st.success(
                f"Berhasil menyimpan tautan untuk temuan: **'{selected_rekomendasi}'** pada **{pilih_unit}**!"
            )
            st.info(f"Link yang disimpan: {google_drive_link}")
