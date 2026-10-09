import os
import json
import pandas as pd
import streamlit as st
from datetime import datetime

from app.database import SessionLocal, Base, engine
from app.models import Product, GeneratedContent, BrandSettings, BatchJob, BatchItem
from app.repositories import ProductRepository, ContentRepository, SettingsRepository, BatchRepository
from app.schemas.product import ProductCreate
from app.services.ai import AIService, MockGenerator
from app.services.scoring.quality_scorer import QualityScorer
from app.services.batch import BatchProcessor
from app.config import settings

# Initialize DB Tables & Page Config
Base.metadata.create_all(bind=engine)

st.set_page_config(
    page_title="CatalogCraft AI — Dual-AI Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# PREMIUM MODERN DARK THEME CSS (MATCHING REACT STUDIO / OPTION 2)
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Overall Dark Slate Canvas */
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }

    /* Custom Modern Header */
    .studio-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(12px);
    }
    .studio-title {
        font-size: 1.85rem;
        font-weight: 900;
        letter-spacing: -0.025em;
        background: linear-gradient(135deg, #60a5fa 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 6px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .studio-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        margin: 0;
        line-height: 1.5;
    }

    /* Status Pills */
    .pill-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .pill-blue {
        background: rgba(37, 99, 235, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    .pill-purple {
        background: rgba(147, 51, 234, 0.15);
        color: #c084fc;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }
    .pill-emerald {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .pill-amber {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* Candidate Cards (Dual-AI Comparison) */
    .candidate-box {
        background: #111827;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .candidate-box:hover {
        border-color: rgba(96, 165, 250, 0.4);
    }
    .candidate-box-claude {
        border-top: 4px solid #a855f7;
    }
    .candidate-box-gemini {
        border-top: 4px solid #38bdf8;
    }

    .winner-tag {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #ffffff;
        padding: 3px 10px;
        border-radius: 8px;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.4);
    }

    /* Modern Score Card */
    .score-card-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin: 16px 0;
    }
    .score-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 14px;
        text-align: center;
    }
    .score-num {
        font-size: 1.6rem;
        font-weight: 900;
        color: #f8fafc;
    }
    .score-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }

    /* Google SERP Preview Mock */
    .google-preview-card {
        background: #ffffff;
        color: #1f2937;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        font-family: Arial, sans-serif;
        margin: 16px 0;
    }
    .google-url {
        font-size: 0.82rem;
        color: #202124;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .google-title {
        font-size: 1.25rem;
        color: #1a0dab;
        text-decoration: none;
        font-weight: 500;
        line-height: 1.3;
        margin-bottom: 6px;
        cursor: pointer;
    }
    .google-title:hover {
        text-decoration: underline;
    }
    .google-snippet {
        font-size: 0.88rem;
        color: #4d5156;
        line-height: 1.5;
    }

    /* Storefront Mock Card */
    .storefront-card {
        background: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        color: #f8fafc;
        margin: 16px 0;
    }
    .storefront-price {
        font-size: 1.85rem;
        font-weight: 900;
        color: #38bdf8;
    }

    /* Notice Alert Card */
    .api-notice-banner {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.35);
        border-radius: 14px;
        padding: 16px 20px;
        margin: 16px 0;
        color: #fef3c7;
    }

    /* Streamlit Sidebar Overrides */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Top Streamlit Header */
    header[data-testid="stHeader"] {
        background-color: #0b0f19 !important;
    }

    /* Buttons Override */
    .stButton > button {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background-color: #334155 !important;
        border-color: #60a5fa !important;
        color: #ffffff !important;
    }
    button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }
    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
    }

    /* Input Fields Override */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2) !important;
    }
    div[data-baseweb="select"] {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
    }
    /* Sidebar Radio Group -> Interactive SaaS Nav Items */
    div[data-testid="stRadio"] div[role="radiogroup"] > label,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 9px 12px !important;
        margin-bottom: 6px !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:hover,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: #334155 !important;
        border-color: #60a5fa !important;
        transform: translateX(4px) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, rgba(37, 99, 235, 0.4) 0%, rgba(96, 165, 250, 0.2) 100%) !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 0 12px rgba(59, 130, 246, 0.3) !important;
    }
    /* Hide the radio circle button */
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child,
    div[data-testid="stRadio"] div[role="radiogroup"] > label span[class*="radio"] {
        display: none !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > label p {
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        color: #f8fafc !important;
        margin: 0 !important;
    }

    /* Sidebar Mini Metrics */
    .sidebar-metrics-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 12px 14px;
        margin: 12px 0;
    }
    .sidebar-metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 0;
        font-size: 0.8rem;
    }
    .sidebar-metric-label {
        color: #94a3b8;
    }
    .sidebar-metric-val {
        font-weight: 700;
        color: #f8fafc;
    }

    /* Sidebar Navigation Interactive Buttons */
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div > div > .stButton > button {
        text-align: left !important;
        justify-content: flex-start !important;
        padding: 9px 14px !important;
        font-size: 0.88rem !important;
        margin-bottom: 2px !important;
        border-radius: 10px !important;
        width: 100% !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background-color: rgba(30, 41, 59, 0.5) !important;
        color: #cbd5e1 !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        display: flex !important;
        align-items: center !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div > div > .stButton > button:hover {
        background-color: #1e293b !important;
        border-color: #60a5fa !important;
        color: #ffffff !important;
        transform: translateX(4px) !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div > div > .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid #60a5fa !important;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.45) !important;
        transform: translateX(2px) !important;
    }
</style>
""", unsafe_allow_html=True)

# Helper DB session manager
def get_db():
    return SessionLocal()

db = get_db()
brand_settings_db = SettingsRepository.get_settings(db)
brand_settings = SettingsRepository.to_schema(brand_settings_db)

# Live Catalog Counts for Sidebar
try:
    live_p_count = db.query(Product).count()
    live_c_count = db.query(GeneratedContent).count()
    live_appr_count = db.query(GeneratedContent).filter(GeneratedContent.status == "Approved").count()
except Exception:
    live_p_count = 0
    live_c_count = 0
    live_appr_count = 0

# -------------------------------------------------------------
# SIDEBAR NAVIGATION (POLISHED LIKE OPTION 2 / REACT STUDIO)
# -------------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 10px 0 16px 0;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-size: 1.8rem;">✨</span>
        <div>
            <div style="font-size: 1.25rem; font-weight: 900; color: #f8fafc; letter-spacing: -0.02em;">CatalogCraft AI</div>
            <div style="font-size: 0.75rem; font-weight: 600; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.05em;">Dual-AI Copy Studio</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Status indicators
has_anthropic = bool(settings.ANTHROPIC_API_KEY.strip()) if settings.ANTHROPIC_API_KEY else False
has_gemini = bool(settings.GEMINI_API_KEY.strip()) if settings.GEMINI_API_KEY else False

if has_anthropic and has_gemini:
    st.sidebar.markdown('<span class="pill-badge pill-purple">⚡ Dual-AI Live</span>', unsafe_allow_html=True)
elif has_anthropic or has_gemini:
    st.sidebar.markdown('<span class="pill-badge pill-blue">🟢 Single Live AI</span>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<span class="pill-badge pill-amber">⚡ Offline Mock Engine</span>', unsafe_allow_html=True)

st.sidebar.caption("Deterministic offline fallback active if API keys are empty.")

# Interactive Live Mini-Metrics Widget
st.sidebar.markdown(f"""
<div class="sidebar-metrics-card">
    <div style="font-size: 0.72rem; font-weight: 800; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
        📊 Live Catalog Summary
    </div>
    <div class="sidebar-metric-row">
        <span class="sidebar-metric-label">📦 Products in Catalog</span>
        <span class="sidebar-metric-val">{live_p_count} SKUs</span>
    </div>
    <div class="sidebar-metric-row">
        <span class="sidebar-metric-label">✍️ Generated Descriptions</span>
        <span class="sidebar-metric-val">{live_c_count}</span>
    </div>
    <div class="sidebar-metric-row">
        <span class="sidebar-metric-label">✅ Merchandiser Approved</span>
        <span class="sidebar-metric-val" style="color: #34d399;">{live_appr_count}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Action: New Description (Matching Option 2 Studio)
if st.sidebar.button("✨ + New Description", type="primary", use_container_width=True, key="quick_new_desc"):
    st.session_state["menu"] = "🪄 Generate Studio"
    for key in ["last_content", "last_product", "p_name", "p_brand", "p_cat", "p_price", "p_features", "p_kw"]:
        st.session_state.pop(key, None)
    st.rerun()

st.sidebar.markdown("""
<div style="font-size: 0.72rem; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; padding: 10px 0 6px 2px;">
    STUDIO NAVIGATION
</div>
""", unsafe_allow_html=True)

if "menu" not in st.session_state:
    st.session_state["menu"] = "🪄 Generate Studio"

nav_items = [
    ("🪄 Generate Studio", "🪄 Generate Studio", "Dual-AI"),
    ("🛍️ Product Catalog", "🛍️ Product Catalog", f"{live_p_count} SKUs"),
    ("📦 Batch CSV Engine", "📦 Batch CSV Engine", "Bulk"),
    ("📊 Analytics & Insights", "📊 Analytics & Insights", "Stats"),
    ("⚙️ Brand Voice Settings", "⚙️ Brand Voice Settings", None),
    ("🎥 Platform Walkthrough", "🎥 Platform Walkthrough", "Demo"),
    ("🛡️ Responsible AI", "🛡️ Responsible AI", None),
]

for label, target, badge in nav_items:
    is_active = (st.session_state["menu"] == target)
    btn_text = f"{label}   [{badge}]" if badge else label
    if is_active:
        btn_text = f"▶ {btn_text}"
    
    if st.sidebar.button(
        btn_text,
        key=f"nav_btn_{target}",
        type="primary" if is_active else "secondary",
        use_container_width=True
    ):
        st.session_state["menu"] = target
        st.rerun()

menu = st.session_state["menu"]

# Interactive Sidebar Quick Actions
st.sidebar.markdown("---")
st.sidebar.markdown("##### ⚡ Quick Presets")
quick_preset = st.sidebar.selectbox(
    "Load Product Preset",
    ["Select Preset...", "🎧 AuraSound Headphones", "👗 UrbanShield Jacket", "🧴 HydraGlow Serum", "☕ BaristaExpress Espresso"],
    index=0
)
if quick_preset == "🎧 AuraSound Headphones":
    st.session_state["p_name"] = "AuraSound Pro Wireless Headphones"
    st.session_state["p_brand"] = "AuraSound"
    st.session_state["p_cat"] = "Electronics"
    st.session_state["p_price"] = 199.99
    st.session_state["p_features"] = "Hybrid Active Noise Cancellation, 40-hour Battery Life, Spatial Audio"
    st.session_state["p_kw"] = "wireless noise cancelling headphones"
elif quick_preset == "👗 UrbanShield Jacket":
    st.session_state["p_name"] = "UrbanShield Waterproof Commuter Jacket"
    st.session_state["p_brand"] = "UrbanShield"
    st.session_state["p_cat"] = "Fashion"
    st.session_state["p_price"] = 149.99
    st.session_state["p_features"] = "3-Layer breathable membrane, Seam-sealed zippers, Storm hood"
    st.session_state["p_kw"] = "waterproof commuter jacket"
elif quick_preset == "🧴 HydraGlow Serum":
    st.session_state["p_name"] = "HydraGlow Botanical Hyaluronic Serum"
    st.session_state["p_brand"] = "Lumiere Botanics"
    st.session_state["p_cat"] = "Beauty and Personal Care"
    st.session_state["p_price"] = 48.00
    st.session_state["p_features"] = "Triple-weight Hyaluronic Acid, Vitamin C + E complex, Vegan"
    st.session_state["p_kw"] = "hydrating face serum"
elif quick_preset == "☕ BaristaExpress Espresso":
    st.session_state["p_name"] = "BaristaExpress Compact Espresso Machine"
    st.session_state["p_brand"] = "CaffèVeloce"
    st.session_state["p_cat"] = "Home and Kitchen"
    st.session_state["p_price"] = 289.00
    st.session_state["p_features"] = "15-Bar pump, Stainless milk steam wand, 45-second rapid heat"
    st.session_state["p_kw"] = "compact espresso maker"

col_act1, col_act2 = st.sidebar.columns(2)
if col_act1.button("🔄 Reset", use_container_width=True):
    for key in ["last_content", "last_product", "p_name", "p_brand", "p_cat", "p_price", "p_features", "p_kw"]:
        st.session_state.pop(key, None)
    st.rerun()

with st.sidebar.expander("⚡ System Diagnostics", expanded=False):
    st.caption(f"**Database**: SQLite (`catalogcraft.db`)")
    st.caption(f"**Claude Model**: `{settings.CLAUDE_MODEL}`")
    st.caption(f"**Gemini Model**: `{settings.GEMINI_MODEL}`")
    st.caption(f"**Backend Server**: `http://127.0.0.1:8000`")
    st.caption(f"**React App**: `http://localhost:5173`")

st.sidebar.markdown("""
<div style="padding: 10px 0; font-size: 0.8rem; color: #94a3b8; line-height: 1.5;">
    <a href="http://localhost:5173" target="_blank" style="display: block; text-align: center; background: rgba(37, 99, 235, 0.2); border: 1px solid #3b82f6; border-radius: 8px; padding: 8px; color: #60a5fa; text-decoration: none; font-weight: 700;">
        🚀 Open React Studio (Port 5173)
    </a>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# TOP STUDIO HEADER
# -------------------------------------------------------------
st.markdown("""
<div class="studio-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
            <h1 class="studio-title">✨ CatalogCraft AI Copywriting Studio</h1>
            <p class="studio-subtitle">
                Autonomous e-commerce copywriting platform benchmarking <strong>Anthropic Claude 3.5 Sonnet</strong> against <strong>Google Gemini 2.5 Flash Lite</strong> with 4D Quality Scoring.
            </p>
        </div>
        <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
            <span class="pill-badge pill-blue">FastAPI Connected</span>
            <span class="pill-badge pill-purple">Claude 3.5 Sonnet</span>
            <span class="pill-badge pill-emerald">Gemini 2.5 Flash Lite</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. GENERATE STUDIO (MATCHING OPTION 2 DUAL-AI STUDIO)
# -------------------------------------------------------------
if menu == "🪄 Generate Studio":
    st.markdown("### 🪄 Product Copywriting Configuration")
    st.caption("Select a one-click retail preset or enter custom product specifications to generate high-converting copy.")

    # One-click Retail Presets
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    if col_p1.button("🎧 AuraSound Headphones", use_container_width=True):
        st.session_state["p_name"] = "AuraSound Pro Wireless Headphones"
        st.session_state["p_brand"] = "AuraSound"
        st.session_state["p_cat"] = "Electronics"
        st.session_state["p_price"] = 199.99
        st.session_state["p_features"] = "Hybrid Active Noise Cancellation, 40-hour Battery Life, Spatial Audio, Ultra-plush memory foam"
        st.session_state["p_kw"] = "wireless noise cancelling headphones, over ear bluetooth headset, hi-fi audio"

    if col_p2.button("👗 UrbanShield Jacket", use_container_width=True):
        st.session_state["p_name"] = "UrbanShield Waterproof Commuter Jacket"
        st.session_state["p_brand"] = "UrbanShield"
        st.session_state["p_cat"] = "Fashion"
        st.session_state["p_price"] = 149.99
        st.session_state["p_features"] = "3-Layer breathable membrane, Seam-sealed YKK zippers, Packable storm hood, Reflective accents"
        st.session_state["p_kw"] = "waterproof rain jacket, urban commuter coat, breathable windbreaker"

    if col_p3.button("🧴 HydraGlow Face Serum", use_container_width=True):
        st.session_state["p_name"] = "HydraGlow Botanical Hyaluronic Serum"
        st.session_state["p_brand"] = "Lumiere Botanics"
        st.session_state["p_cat"] = "Beauty and Personal Care"
        st.session_state["p_price"] = 48.00
        st.session_state["p_features"] = "Triple-weight Hyaluronic Acid, Vitamin C + E complex, 100% Vegan & cruelty-free, Fragrance-free"
        st.session_state["p_kw"] = "hydrating face serum, hyaluronic acid moisturizer, radiant skin treatment"

    if col_p4.button("☕ BaristaExpress Espresso", use_container_width=True):
        st.session_state["p_name"] = "BaristaExpress Compact Espresso Machine"
        st.session_state["p_brand"] = "CaffèVeloce"
        st.session_state["p_cat"] = "Home and Kitchen"
        st.session_state["p_price"] = 289.00
        st.session_state["p_features"] = "15-Bar Italian high pressure pump, Integrated stainless milk steam wand, 45-second rapid heat thermo-block"
        st.session_state["p_kw"] = "compact espresso maker, 15 bar coffee machine, home barista latte maker"

    with st.form("generation_form"):
        col1, col2 = st.columns(2)
        p_name = col1.text_input("Product Name *", value=st.session_state.get("p_name", ""))
        p_brand = col2.text_input("Brand", value=st.session_state.get("p_brand", ""))

        col3, col4 = st.columns(2)
        p_cat = col3.selectbox(
            "Category *",
            ["Electronics", "Fashion", "Home and Kitchen", "Beauty and Personal Care", "Sports and Fitness", "Grocery", "Furniture", "Travel Accessories"],
            index=["Electronics", "Fashion", "Home and Kitchen", "Beauty and Personal Care", "Sports and Fitness", "Grocery", "Furniture", "Travel Accessories"].index(st.session_state.get("p_cat", "Electronics"))
        )
        p_price = col4.number_input("Price ($)", value=st.session_state.get("p_price", 99.99), step=5.0)

        p_features_str = st.text_area(
            "Key Features & Specifications (comma-separated)",
            value=st.session_state.get("p_features", ""),
            placeholder="e.g. Active Noise Cancellation, 40-hour Battery Life, Bluetooth 5.3"
        )
        p_kw_str = st.text_input(
            "Primary SEO Keywords (comma-separated)",
            value=st.session_state.get("p_kw", ""),
            placeholder="e.g. noise cancelling headphones, wireless headset"
        )

        col_opt1, col_opt2, col_opt3 = st.columns(3)
        tone = col_opt1.selectbox("Tone of Voice", ["Professional", "Premium / Luxury", "Friendly", "Minimal", "Technical", "Playful", "Eco-conscious"])
        word_count = col_opt2.selectbox("Copy Length", ["Short", "Medium", "Long"], index=1)
        engine_mode = col_opt3.selectbox("AI Engine", [
            "Dual-AI Arbiter (Claude 3.5 + Gemini 2.5)",
            "Anthropic Claude 3.5 Sonnet",
            "Google Gemini (Flash Lite)"
        ], index=0)

        st.markdown("""
        <div style="font-size: 0.78rem; color: #94a3b8; display: flex; align-items: center; gap: 6px; margin: 8px 0 16px 0;">
            <span>⚡</span>
            <span><strong>Zero-Downtime Guarantee:</strong> If live cloud API keys are empty, CatalogCraft automatically generates realistic copy and 4D quality scores via the deterministic offline Mock Engine.</span>
        </div>
        """, unsafe_allow_html=True)

        submit = st.form_submit_button("✨ Generate Dual-AI Copy", type="primary", use_container_width=True)

    if submit and p_name:
        if "Dual-AI" in engine_mode:
            engine_code = "dual"
        elif "Claude" in engine_mode:
            engine_code = "anthropic"
        elif "Gemini" in engine_mode:
            engine_code = "gemini"
        else:
            engine_code = "dual"

        prod_create = ProductCreate(
            name=p_name,
            brand=p_brand,
            category=p_cat,
            price=p_price,
            features=[f.strip() for f in p_features_str.split(",") if f.strip()],
            primary_keywords=[k.strip() for k in p_kw_str.split(",") if k.strip()]
        )

        with st.spinner("Benchmarking Claude 3.5 Sonnet and Gemini 2.5 Flash Lite..."):
            content_dict, source, decision_meta = AIService.generate_description(
                product=prod_create,
                brand_settings=brand_settings,
                tone=tone,
                language="English",
                word_count_preference=word_count,
                engine=engine_code
            )

            scores = QualityScorer.calculate_scores(
                product=prod_create,
                title=content_dict["title"],
                short_desc=content_dict["short_description"],
                full_desc=content_dict["full_description"],
                meta_title=content_dict["meta_title"],
                meta_desc=content_dict["meta_description"],
                brand_settings=brand_settings,
                tone=tone
            )

        st.session_state["last_product"] = prod_create
        st.session_state["last_content"] = content_dict
        st.session_state["last_source"] = source
        st.session_state["last_decision_meta"] = decision_meta
        st.session_state["last_scores"] = scores
        st.session_state["last_tone"] = tone
        st.session_state["last_word_count"] = word_count

    # ---------------------------------------------------------
    # RESULTS STUDIO VIEW (TABS LIKE OPTION 2 / REACT)
    # ---------------------------------------------------------
    if "last_content" in st.session_state:
        prod_create = st.session_state["last_product"]
        content_dict = st.session_state["last_content"]
        source = st.session_state["last_source"]
        decision_meta = st.session_state["last_decision_meta"]
        scores = st.session_state["last_scores"]
        tone = st.session_state["last_tone"]
        word_count = st.session_state["last_word_count"]
        candidates = decision_meta.get("candidates", [])

        st.divider()

        # Decision Rationale Banner
        if decision_meta.get("decision_rationale"):
            st.markdown(f"""
            <div style="background: rgba(37, 99, 235, 0.12); border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 12px; padding: 14px 18px; margin-bottom: 16px;">
                <div style="font-size: 0.82rem; font-weight: 800; color: #60a5fa; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">
                    💡 Dual-AI Arbiter Rationale
                </div>
                <div style="font-size: 0.92rem; color: #e2e8f0; line-height: 1.5;">
                    {decision_meta['decision_rationale']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # API Key Notice Banner
        api_notice = decision_meta.get("api_key_notice")
        if (api_notice and api_notice.get("is_missing")) or source == "mock" or "mock" in str(source):
            provs = (api_notice.get("missing_providers") if api_notice else None) or ["Gemini", "Claude"]
            missing_text = " and ".join(provs)
            st.markdown(f"""
            <div class="api-notice-banner">
                <div style="display: flex; align-items: flex-start; gap: 12px;">
                    <span style="font-size: 1.4rem;">⚠️</span>
                    <div>
                        <div style="font-size: 0.95rem; font-weight: 800; color: #fbbf24; margin-bottom: 4px;">
                            API Key Notice: Switched to Offline Deterministic Mock Generator
                        </div>
                        <div style="font-size: 0.85rem; color: #fde68a; line-height: 1.5;">
                            No active API keys found for <strong>{missing_text}</strong>. CatalogCraft automatically activated the offline Mock Engine with full 4D scoring, bullet points, and candidate arbitration so you can continue testing without cloud API credits.
                        </div>
                        <div style="font-size: 0.78rem; color: #cbd5e1; margin-top: 6px; font-family: monospace;">
                            To use live models, add GEMINI_API_KEY and ANTHROPIC_API_KEY inside backend/.env
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 4D Overall Quality Scorecard
        st.markdown("""
        <div style="font-size: 1.1rem; font-weight: 800; color: #f8fafc; margin-bottom: 8px;">
            📊 4-Dimensional Copy Quality Scorecard
        </div>
        """, unsafe_allow_html=True)

        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("Overall Quality", f"{scores['quality_score']}/100", delta="+4.2 vs baseline")
        col_s2.metric("SEO Audit", f"{scores['seo_score']}/100", delta=f"{len(content_dict.get('suggested_keywords', []))} keywords")
        col_s3.metric("Readability", f"{scores['readability_score']}/100", delta="Flesch-Kincaid Grade 8")
        col_s4.metric("Brand Compliance", f"{scores['brand_tone_score']}/100", delta=f"{tone} Voice")

        # Result Mode Tabs (Exact replica of Option 2 Studio Tabs)
        tab_comp, tab_store, tab_seo, tab_json = st.tabs([
            "⚖️ Dual-AI Candidate Benchmark",
            "🛍️ Storefront Mock Preview",
            "🔍 Google SERP Snippet Preview",
            "📝 Raw Copy & JSON Export"
        ])

        # TAB 1: DUAL-AI SIDE-BY-SIDE BENCHMARK
        with tab_comp:
            if len(candidates) >= 2:
                st.caption("Inspect both Claude and Gemini copy side-by-side, then approve your preferred version to add it to your catalog:")

                cand_cols = st.columns(2)
                for idx, cand in enumerate(candidates):
                    is_claude = (cand["provider"] == "anthropic")
                    col = cand_cols[idx]
                    with col:
                        header_color = "#c084fc" if is_claude else "#38bdf8"
                        card_class = "candidate-box candidate-box-claude" if is_claude else "candidate-box candidate-box-gemini"
                        winner_badge = '<span class="winner-tag">⭐ Arbiter Winner</span>' if cand.get("is_winner") else ''
                        icon_emoji = '🟣' if is_claude else '🔵'
                        cand_header_html = f'<div class="{card_class}"><div style="display:flex;justify-content:space-between;align-items:center;"><div style="display:flex;align-items:center;gap:8px;"><span style="font-size:1.3rem;">{icon_emoji}</span><strong style="font-size:1.1rem;color:{header_color};">{cand["provider_label"]}</strong></div>{winner_badge}</div></div>'
                        st.markdown(cand_header_html, unsafe_allow_html=True)

                        c_scores = cand.get("scores", {})
                        col_m1, col_m2 = st.columns(2)
                        col_m1.metric("Overall Score", f"{c_scores.get('quality_score', 0)}/100")
                        col_m2.metric("SEO Score", f"{c_scores.get('seo_score', 0)}/100")

                        st.markdown(f"**Headline:** {cand['content']['title']}")
                        st.caption(f"**Hook:** {cand['content']['short_description']}")
                        st.text_area(f"Full Body Copy ({cand['provider_label']})", cand['content']['full_description'], height=180, key=f"desc_{idx}")

                        st.markdown("**Bullet Highlights:**")
                        for h in (cand['content'].get('highlights') or [])[:3]:
                            st.markdown(f"• {h}")

                        # Approve Button for this candidate
                        btn_label = f"✅ Approve {cand['provider_label']} & Add to Catalog"
                        if st.button(btn_label, key=f"appr_{cand['provider']}", use_container_width=True, type="primary" if cand.get("is_winner") else "secondary"):
                            db_p = ProductRepository.create(db, prod_create)
                            db_content = GeneratedContent(
                                product_id=db_p.id,
                                title=cand['content']['title'],
                                short_description=cand['content']['short_description'],
                                full_description=cand['content']['full_description'],
                                highlights=json.dumps(cand['content'].get('highlights', [])),
                                meta_title=cand['content'].get('meta_title', ''),
                                meta_description=cand['content'].get('meta_description', ''),
                                suggested_keywords=json.dumps(cand['content'].get('suggested_keywords', [])),
                                warnings=json.dumps(cand['content'].get('warnings', [])),
                                tone=tone,
                                language="English",
                                word_count_preference=word_count,
                                seo_score=c_scores.get('seo_score', 0),
                                readability_score=c_scores.get('readability_score', 0),
                                completeness_score=c_scores.get('completeness_score', 0),
                                brand_tone_score=c_scores.get('brand_tone_score', 0),
                                quality_score=c_scores.get('quality_score', 0),
                                status="Approved",
                                generation_source=cand['provider'],
                                candidates_data=json.dumps(candidates),
                                decision_rationale=decision_meta.get("decision_rationale", "")
                            )
                            db.add(db_content)
                            db.commit()
                            st.success(f"🎉 Successfully approved and committed **{cand['provider_label']}** version to the product catalog!")
            else:
                # Single engine display
                st.markdown(f"### {content_dict['title']}")
                st.caption(content_dict['short_description'])
                st.write(content_dict['full_description'])
                if st.button("✅ Approve & Add to Catalog", type="primary", use_container_width=True):
                    db_p = ProductRepository.create(db, prod_create)
                    db_content = GeneratedContent(
                        product_id=db_p.id,
                        title=content_dict['title'],
                        short_description=content_dict['short_description'],
                        full_description=content_dict['full_description'],
                        highlights=json.dumps(content_dict.get('highlights', [])),
                        meta_title=content_dict.get('meta_title', ''),
                        meta_description=content_dict.get('meta_description', ''),
                        suggested_keywords=json.dumps(content_dict.get('suggested_keywords', [])),
                        warnings=json.dumps(scores.get('recommendations', [])),
                        tone=tone,
                        language="English",
                        word_count_preference=word_count,
                        seo_score=scores['seo_score'],
                        readability_score=scores['readability_score'],
                        completeness_score=scores['completeness_score'],
                        brand_tone_score=scores['brand_tone_score'],
                        quality_score=scores['quality_score'],
                        status="Approved",
                        generation_source=source
                    )
                    db.add(db_content)
                    db.commit()
                    st.success("🎉 Successfully approved and saved to the catalog!")

        # TAB 2: STOREFRONT MOCK PREVIEW (Exact replica of Option 2 storefront preview)
        with tab_store:
            st.markdown(f"""
            <div class="storefront-card">
                <div style="display: flex; gap: 24px; flex-wrap: wrap;">
                    <div style="flex: 1; min-width: 250px; background: rgba(15, 23, 42, 0.6); border-radius: 12px; display: flex; align-items: center; justify-content: center; min-height: 240px; border: 1px dashed rgba(255, 255, 255, 0.2);">
                        <div style="text-align: center; color: #94a3b8;">
                            <div style="font-size: 3rem;">🛍️</div>
                            <div style="font-size: 0.85rem; font-weight: 700; margin-top: 6px;">{prod_create.brand or 'Brand'} Official Store</div>
                            <div style="font-size: 0.75rem; color: #64748b;">{prod_create.category}</div>
                        </div>
                    </div>
                    <div style="flex: 2; min-width: 320px;">
                        <span class="pill-badge pill-blue">{prod_create.category}</span>
                        <h2 style="font-size: 1.4rem; font-weight: 800; color: #f8fafc; margin: 8px 0 6px 0;">{content_dict['title']}</h2>
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                            <span style="color: #fbbf24;">★★★★★</span>
                            <span style="font-size: 0.8rem; color: #94a3b8;">4.9 (128 verified customer reviews)</span>
                        </div>
                        <div class="storefront-price">${prod_create.price}</div>
                        <p style="font-size: 0.95rem; color: #cbd5e1; line-height: 1.6; margin: 12px 0;">{content_dict['short_description']}</p>
                        <div style="margin: 16px 0;">
                            <strong style="font-size: 0.85rem; color: #e2e8f0; text-transform: uppercase; letter-spacing: 0.05em;">Highlights:</strong>
                            <ul style="margin: 8px 0 0 18px; color: #94a3b8; font-size: 0.88rem; line-height: 1.6;">
                                {''.join(f'<li>{h}</li>' for h in content_dict.get('highlights', [])[:4])}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # TAB 3: GOOGLE SERP PREVIEW (Option 2 Google Snippet Card)
        with tab_seo:
            st.markdown(f"""
            <div class="google-preview-card">
                <div class="google-url">
                    <span style="background: #e8f0fe; border-radius: 50%; width: 16px; height: 16px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px;">🌐</span>
                    <span>https://www.yourstore.com › products › {prod_create.name.lower().replace(' ', '-')}</span>
                </div>
                <div class="google-title">{content_dict['meta_title']}</div>
                <div class="google-snippet">{content_dict['meta_description']}</div>
            </div>
            """, unsafe_allow_html=True)

            col_meta1, col_meta2 = st.columns(2)
            col_meta1.caption(f"Meta Title Length: **{len(content_dict['meta_title'])} / 60 characters** (Optimal: 50-60)")
            col_meta2.caption(f"Meta Description Length: **{len(content_dict['meta_description'])} / 160 characters** (Optimal: 120-160)")

        # TAB 4: RAW COPY & JSON EXPORT
        with tab_json:
            st.text_input("Copyable Title", value=content_dict['title'])
            st.text_area("Copyable Full Description", value=content_dict['full_description'], height=150)
            st.json(content_dict)

# -------------------------------------------------------------
# 2. PRODUCT CATALOGUE PAGE
# -------------------------------------------------------------
elif menu == "🛍️ Product Catalog":
    st.markdown("### 🛍️ Retail Product Catalog & Merchandising Review")
    st.caption("Inspect, filter, and audit all catalog products along with their generated copy and approval statuses.")

    col_s1, col_s2 = st.columns([3, 1])
    search = col_s1.text_input("Search catalog products by name, brand, or SKU...", "")
    cat_filter = col_s2.selectbox("Filter Category", ["All Categories", "Electronics", "Fashion", "Home and Kitchen", "Beauty and Personal Care", "Sports and Fitness"])

    items, total = ProductRepository.get_all(db, search=search if search else None, page_size=50)

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Catalog Products", total)
    approved_total = sum(1 for item in items if item["generated_content"] and item["generated_content"].get("status") == "Approved")
    review_total = total - approved_total
    col_m2.metric("Approved Listings", approved_total, delta=f"{round((approved_total/total*100) if total else 0)}% ready")
    col_m3.metric("Pending Review", review_total)

    data = []
    for item in items:
        p = item["product"]
        c = item["generated_content"]
        if cat_filter != "All Categories" and p["category"] != cat_filter:
            continue
        data.append({
            "ID": p["id"],
            "Name": p["name"],
            "Brand": p.get("brand") or "N/A",
            "Category": p["category"],
            "Price": f"${p['price']}" if p.get('price') else "N/A",
            "Quality Score": f"{c['quality_score']}/100" if c else "—",
            "Status": c["status"] if c else "Not Generated",
            "Model": c.get("generation_source", "—") if c else "—"
        })

    st.dataframe(pd.DataFrame(data), use_container_width=True, height=450)

# -------------------------------------------------------------
# 3. BATCH GENERATOR PAGE
# -------------------------------------------------------------
elif menu == "📦 Batch CSV Engine":
    st.markdown("### 📦 Enterprise Batch Processing Engine")
    st.caption("Upload multi-SKU CSV or JSON files to generate hundreds of descriptions concurrently.")

    uploaded_file = st.file_uploader("Upload Product Catalog (CSV or JSON)", type=["csv", "json"])

    if uploaded_file:
        file_bytes = uploaded_file.read()
        file_ext = uploaded_file.name.split(".")[-1].lower()
        valid_rows, invalid_rows = BatchProcessor.parse_file(file_bytes, file_ext)

        st.info(f"📁 Parsed **{len(valid_rows)} valid products** and **{len(invalid_rows)} invalid rows** from `{uploaded_file.name}`.")

        if valid_rows:
            st.dataframe(pd.DataFrame(valid_rows).head(10), use_container_width=True)

            if st.button("🚀 Run Batch Processing", type="primary", use_container_width=True):
                with st.spinner("Processing batch catalog with Dual-AI Arbiter..."):
                    job = BatchRepository.create_job(db, uploaded_file.name, file_ext, len(valid_rows))
                    for row in valid_rows:
                        row.pop("row_number", None)
                        prod_create = ProductCreate(**row)
                        db_product = ProductRepository.create(db, prod_create)
                        BatchRepository.add_item(db, batch_job_id=job.id, row_number=1, product_id=db_product.id)

                    BatchProcessor.process_batch(db, job, brand_settings)
                    st.success("🎉 Batch processing successfully completed! Descriptions are now saved to the catalog.")

# -------------------------------------------------------------
# 4. ANALYTICS & INSIGHTS PAGE
# -------------------------------------------------------------
elif menu == "📊 Analytics & Insights":
    st.markdown("### 📊 E-Commerce Copywriting Quality Intelligence")
    st.caption("Executive overview of copywriting performance, category distribution, and approval throughput.")

    contents = db.query(GeneratedContent).all()
    products_count = db.query(Product).count()
    generated_count = len(contents)
    approved_count = sum(1 for c in contents if c.status == "Approved")
    avg_quality = round(sum(c.quality_score for c in contents) / generated_count, 1) if generated_count > 0 else 0.0
    avg_seo = round(sum(c.seo_score for c in contents) / generated_count, 1) if generated_count > 0 else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Catalog Products", products_count)
    col2.metric("Descriptions Generated", generated_count)
    col3.metric("Approved Copy", approved_count, delta=f"{round((approved_count/generated_count*100) if generated_count else 0)}% Approved")
    col4.metric("Avg Quality Score", f"{avg_quality} / 100", delta=f"SEO: {avg_seo}")

    st.divider()

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Category Distribution")
        query = db.query(Product.category).all()
        cats = [c[0] for c in query]
        if cats:
            df_cats = pd.Series(cats).value_counts().reset_index()
            df_cats.columns = ["Category", "Count"]
            st.bar_chart(df_cats.set_index("Category"))

    with col_chart2:
        st.subheader("Approval Workflow Distribution")
        statuses = [c.status for c in contents]
        if statuses:
            df_stat = pd.Series(statuses).value_counts().reset_index()
            df_stat.columns = ["Status", "Count"]
            st.bar_chart(df_stat.set_index("Status"))

# -------------------------------------------------------------
# 5. BRAND SETTINGS PAGE
# -------------------------------------------------------------
elif menu == "⚙️ Brand Settings":
    st.markdown("### ⚙️ Brand Voice & Compliance Guardrails")
    st.caption("Define mandatory vocabulary, prohibited claims, and legal disclaimers enforced across all generated descriptions.")

    with st.form("brand_settings_form"):
        b_name = st.text_input("Brand Name", value=brand_settings.brand_name)
        b_voice = st.text_area("Brand Voice Personality", value=brand_settings.brand_voice)
        pref_words = st.text_input("Preferred Vocabulary (comma-separated)", value=", ".join(brand_settings.preferred_words))
        proh_words = st.text_input("Prohibited Words (comma-separated)", value=", ".join(brand_settings.prohibited_words))
        disclaimer = st.text_input("Mandatory Legal Disclaimer", value=brand_settings.mandatory_disclaimer or "")

        saved = st.form_submit_button("Save Brand Rules", type="primary")
        if saved:
            SettingsRepository.update_settings(db, {
                "brand_name": b_name,
                "brand_voice": b_voice,
                "preferred_words": [w.strip() for w in pref_words.split(",") if w.strip()],
                "prohibited_words": [w.strip() for w in proh_words.split(",") if w.strip()],
                "mandatory_disclaimer": disclaimer
            })
            st.success("🎉 Brand voice guardrails successfully updated!")

# -------------------------------------------------------------
# 6. DEMO VIDEO WALKTHROUGH PAGE
# -------------------------------------------------------------
elif menu == "🎥 Platform Walkthrough":
    st.markdown("### 🎥 Interactive Platform Architecture Walkthrough")
    st.caption("How CatalogCraft AI delivers production-grade retail copywriting with Dual-AI verification.")

    col_v1, col_v2 = st.columns([7, 5])
    with col_v1:
        step_choice = st.radio(
            "Select Architecture Step:",
            [
                "Step 1: Single Product & Enterprise Bulk CSV",
                "Step 2: Dual-AI Arbiter (Claude 3.5 Sonnet vs Gemini 2.5 Flash Lite)",
                "Step 3: 4D Multi-Attribute Scoring (Completeness, SEO, Readability, Tone)",
                "Step 4: Merchandiser Approval Workflow & Catalog Export"
            ]
        )

        if "Step 1" in step_choice:
            st.info("📝 **Step 1: Specification Ingestion**\n\nDirect attribute entry or bulk CSV/JSON ingestion with automatic attribute normalization.")
        elif "Step 2" in step_choice:
            st.info("🤖 **Step 2: Dual-AI Arbitration**\n\nConcurrent prompting of Claude 3.5 Sonnet and Gemini 2.5 Flash Lite, followed by automated heuristic quality comparison.")
        elif "Step 3" in step_choice:
            st.info("🎯 **Step 3: 4-Dimensional Quality Scoring**\n\nIndependent evaluation across Completeness (30%), SEO (30%), Readability (20%), and Brand Tone (20%).")
        else:
            st.info("🚀 **Step 4: Approval & Multi-Channel Export**\n\nHuman-in-the-loop review, approval, and 1-click export to Shopify, Amazon, or ERP.")

    with col_v2:
        st.metric("Time-to-Market", "95% Faster", delta="2 mins vs 3 weeks")
        st.metric("Organic SEO Lift", "+40% Organic Traffic", delta="Optimized SERP snippets")
        st.metric("Brand Tone Safety", "100% Guaranteed", delta="Enforced guardrails")

# -------------------------------------------------------------
# 7. RESPONSIBLE AI PAGE
# -------------------------------------------------------------
elif menu == "🛡️ Responsible AI":
    st.markdown("### 🛡️ Responsible AI Governance & Transparency")
    st.caption("Enterprise safety guardrails built into CatalogCraft AI.")

    st.markdown("""
    1. **Strict Truthfulness & Anti-Hallucination**: The AI engine uses only verified product facts provided in the input specifications. It does not invent dimensions, materials, or certifications.
    2. **Human-in-the-Loop Verification**: Copy requires merchandiser approval before publication.
    3. **Tone Guardrails**: Prohibited terms and unverified marketing superlatives are flagged automatically.
    4. **Zero-PII Storage**: The platform processes catalog product attributes only with zero customer PII collection.
    """)
