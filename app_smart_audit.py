import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from datetime import datetime
import os

st.set_page_config(
    page_title="Executive Audit Dashboard | PT Pelindo Solusi Maritim",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Ultimate + Banner Kemerdekaan yang Jelas & Elegan
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    
    /* Banner Kemerdekaan Diperbaiki */
    .merdeka-banner {
        background: linear-gradient(135deg, #991b1b 0%, #dc2626 50%, #b91c1c 100%);
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        color: #ffffff !important;
        font-weight: 800;
        font-size: 18px;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.4);
        border: 2px solid #fca5a5;
    }
    
    .header-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 20px 25px;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .header-title { color: #ffffff; font-size: 22px; font-weight: 700; }
    .header-subtitle { color: #94a3b8; font-size: 13px; margin-top: 5px; }

    .stTextArea textarea { min-height: 100px !important; }

    @keyframes blink-animation {
        0% { opacity: 1; border-color: #ef4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.6); }
        50% { opacity: 0.4; border-color: #7f1d1d; box-shadow: 0 0 2px rgba(239, 68, 68, 0.1); }
        100% { opacity: 1; border-color: #ef4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.6); }
    }

    .alert-blink {
        background: rgba(239, 68, 68, 0.15);
        border: 2px solid #ef4444;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 15px;
        animation: blink-animation 1.5s infinite ease-in-out;
    }

    .kpi-row { display: flex; gap: 14px; width: 100%; margin-bottom: 20px; }
    .kpi-card {
        flex: 1;
        background: linear-gradient(145deg, #161b22 0%, #0d1117 100%);
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 8px 20px -4px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.15);
        transition: transform 0.2s ease;
    }
    .kpi-card:hover { transform: translateY(-3px); }
    .card-blue { border: 2px solid #3b82f6; }
    .card-green { border: 2px solid #10b981; }
    .card-yellow { border: 2px solid #f59e0b; }
    .card-red { border: 2px solid #ef4444; }
    .kpi-title { color: #94a3b8; font-size: 10.5px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
    .kpi-value { color: #ffffff; font-size: 28px; font-weight: 800; line-height: 1.1; }
</style>
""", unsafe_allow_html=True)

# --- UCAPAN KEMERDEKAAN ---
st.markdown("""
<div class="merdeka-banner">
    🇮🇩 DIRGAHAYU REPUBLIK INDONESIA KE-81 — NUSANTARA BARU, INDONESIA MAJU (MERDEKA!) 🇮🇩
</div>
""", unsafe_allow_html=True)

# Lanjutkan sisa kode program Anda di bawah ini seperti biasa...
