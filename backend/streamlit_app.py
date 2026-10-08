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

# Initialize DB Tables & Page Config
Base.metadata.create_all(bind=engine)

st.set_page_config(
    page_title="CatalogCraft AI — Streamlit App",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #64748b;
        margin-bottom: 20px;
    }
    .metric-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 15px;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# Helper DB session manager
def get_db():
    return SessionLocal()

db = get_db()
brand_settings_db = SettingsRepository.get_settings(db)
brand_settings = SettingsRepository.to_schema(brand_settings_db)

# Sidebar Navigation
st.sidebar.title("✨ CatalogCraft AI")
st.sidebar.caption("Retail Product Description Platform")

menu = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "🎥 Demo Video Walkthrough", "🪄 Generate Description", "📦 Batch Generator", "🛍️ Product Catalogue", "⚙️ Brand Settings", "🛡️ Responsible AI"]
)

st.sidebar.divider()
st.sidebar.caption("Enterprise Edition v2.4 (Streamlit App)")

# -------------------------------------------------------------
# 1. DASHBOARD PAGE
# -------------------------------------------------------------
if menu == "📊 Dashboard":
    st.markdown('<div class="main-header">CatalogCraft AI Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Executive metrics and content generation overview</div>', unsafe_allow_html=True)

    products_count = db.query(Product).count()
    contents = db.query(GeneratedContent).all()
    generated_count = len(contents)
    approved_count = sum(1 for c in contents if c.status == "Approved")
    review_count = sum(1 for c in contents if c.status == "Needs Review")

    avg_quality = round(sum(c.quality_score for c in contents) / generated_count, 1) if generated_count > 0 else 0.0
    avg_seo = round(sum(c.seo_score for c in contents) / generated_count, 1) if generated_count > 0 else 0.0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Products", products_count)
    col2.metric("Descriptions Generated", generated_count)
    col3.metric("Approved Descriptions", approved_count, delta=f"{review_count} Pending Review")
    col4.metric("Avg Quality Score", f"{avg_quality} / 100", delta=f"SEO: {avg_seo}")

    st.divider()

    st.subheader("Category Distribution")
    query = db.query(Product.category).all()
    cats = [c[0] for c in query]
    if cats:
        df_cats = pd.Series(cats).value_counts().reset_index()
        df_cats.columns = ["Category", "Count"]
        st.bar_chart(df_cats.set_index("Category"))

# -------------------------------------------------------------
# DEMO VIDEO WALKTHROUGH PAGE
# -------------------------------------------------------------
elif menu == "🎥 Demo Video Walkthrough":
    st.markdown('<div class="main-header">🎥 Interactive Demo Video & Platform Walkthrough</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">See how CatalogCraft AI transforms retail product data into engaging SEO descriptions</div>', unsafe_allow_html=True)

    st.info("💡 **Retailer Walkthrough**: This interactive demonstration guides you through the 4 steps of automated e-commerce catalog generation.")

    col_v1, col_v2 = st.columns([7, 5])
    with col_v1:
        st.subheader("Interactive Video Simulator")
        step_choice = st.radio(
            "Select Walkthrough Step:",
            [
                "Step 1: Single Product & Bulk CSV Upload",
                "Step 2: Dual AI Engine Orchestration (Claude + Gemini)",
                "Step 3: 4D Quality Scoring (0-100)",
                "Step 4: Approval Workflow & CSV Export"
            ]
        )

        if "Step 1" in step_choice:
            st.success("📝 **Step 1: Input Product Attributes or Upload CSV**")
            st.markdown("""
            * **Single Product Studio**: Enter SKU, brand, category, price, key features, specifications, and primary keywords.
            * **Bulk CSV/JSON Upload**: Drag and drop catalogs with 100+ items (Electronics, Fashion, etc.).
            * **Validation**: Auto-checks required fields and normalizes attribute structures.
            """)
        elif "Step 2" in step_choice:
            st.success("🤖 **Step 2: Dual-AI Engine Orchestration**")
            st.markdown("""
            * **Concurrent Generation**: Requests copy candidates from Anthropic Claude 3.5 Sonnet & Google Gemini.
            * **Arbitration Logic**: Evaluates narrative appeal against technical precision to pick the winning description.
            * **Zero-Downtime Fallback**: Uses local Mock Generator when API key is offline.
            """)
        elif "Step 3" in step_choice:
            st.success("🎯 **Step 3: 4-Dimensional Quality Scoring**")
            st.markdown("""
            * **Completeness (25%)**: Checks presence of title, short desc, full desc, features, and specs.
            * **SEO Audit (25%)**: Validates keyword placement, meta title length (50-60 chars), and meta desc (120-160 chars).
            * **Readability (25%)**: Flesch-Kincaid readability optimization for conversion.
            * **Brand Compliance (25%)**: Enforces tone guidelines and flags prohibited words or missing USPs.
            """)
        else:
            st.success("🚀 **Step 4: Approval Workflow & CSV Export**")
            st.markdown("""
            * **Review Statuses**: Draft -> Needs Review -> Approved.
            * **Inline Editor**: Edit copy directly with instant quality score re-calculation.
            * **1-Click Export**: Export approved descriptions into formatted CSV/JSON for Shopify, Amazon, or ERP systems.
            """)

    with col_v2:
        st.subheader("Key Retailer Business Benefits")
        st.metric("Time-to-Market", "95% Faster", delta="2 mins vs 3 weeks")
        st.metric("Organic Search Traffic", "+40% SEO Lift", delta="Optimized Meta Tags")
        st.metric("Brand Tone Safety", "100% Guaranteed", delta="Enforced Guardrails")

        st.divider()
        st.download_button(
            label="📄 Download 105-Product Demo CSV",
            data=open("data/sample_products.csv", "rb").read(),
            file_name="catalogcraft_electronics_fashion_105.csv",
            mime="text/csv"
        )

# -------------------------------------------------------------
# 2. GENERATE DESCRIPTION PAGE
# -------------------------------------------------------------
elif menu == "🪄 Generate Description":
    st.markdown('<div class="main-header">Single Product Description Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Enter product details to generate AI copy and quality score</div>', unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([1, 4])
    if col_btn1.button("⚡ Load Electronics Preset"):
        st.session_state["p_name"] = "AuraSound Pro Wireless Headphones"
        st.session_state["p_brand"] = "AuraSound"
        st.session_state["p_cat"] = "Electronics"
        st.session_state["p_price"] = 199.99
        st.session_state["p_features"] = "Active Noise Cancellation, 40-hour Battery Life, Spatial Audio"
        st.session_state["p_kw"] = "wireless noise cancelling headphones"

    if col_btn2.button("👗 Load Fashion Preset"):
        st.session_state["p_name"] = "UrbanShield Waterproof Jacket"
        st.session_state["p_brand"] = "UrbanShield"
        st.session_state["p_cat"] = "Fashion"
        st.session_state["p_price"] = 129.99
        st.session_state["p_features"] = "3-Layer Breathable Membrane, Seam-Sealed Zippers, Adjustable Hood"
        st.session_state["p_kw"] = "waterproof rain jacket"

    with st.form("gen_form"):
        col1, col2 = st.columns(2)
        p_name = col1.text_input("Product Name *", value=st.session_state.get("p_name", ""))
        p_brand = col2.text_input("Brand", value=st.session_state.get("p_brand", ""))

        col3, col4 = st.columns(2)
        p_cat = col3.selectbox("Category *", ["Electronics", "Fashion", "Home and Kitchen", "Beauty and Personal Care", "Sports and Fitness", "Grocery", "Furniture", "Travel Accessories"], index=0)
        p_price = col4.number_input("Price ($)", value=st.session_state.get("p_price", 99.99))

        p_features_str = st.text_area("Key Features (comma-separated)", value=st.session_state.get("p_features", ""))
        p_kw_str = st.text_input("Primary SEO Keywords (comma-separated)", value=st.session_state.get("p_kw", ""))

        col_opt1, col_opt2 = st.columns(2)
        tone = col_opt1.selectbox("Tone", ["Professional", "Premium / Luxury", "Friendly", "Minimal", "Technical", "Playful", "Eco-conscious"])
        word_count = col_opt2.selectbox("Word Count", ["Short", "Medium", "Long"], index=1)

        submit = st.form_submit_button("✨ Generate Copy", type="primary")

    if submit and p_name:
        prod_create = ProductCreate(
            name=p_name,
            brand=p_brand,
            category=p_cat,
            price=p_price,
            features=[f.strip() for f in p_features_str.split(",") if f.strip()],
            primary_keywords=[k.strip() for k in p_kw_str.split(",") if k.strip()]
        )

        content_dict, source, decision_meta = AIService.generate_description(
            product=prod_create,
            brand_settings=brand_settings,
            tone=tone,
            language="English",
            word_count_preference=word_count
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

        model_name = decision_meta.get("chosen_model", source)
        st.success(f"Generated via **{model_name.upper()}** Engine! Overall Quality Score: **{scores['quality_score']}/100**")
        if decision_meta.get("decision_rationale"):
            st.info(f"💡 **AI Selection Rationale**: {decision_meta['decision_rationale']}")

        st.subheader(content_dict["title"])
        st.caption(f"Short Description: {content_dict['short_description']}")
        st.write(content_dict["full_description"])

        st.markdown("**Highlights:**")
        for h in content_dict["highlights"]:
            st.markdown(f"- {h}")

        st.info(f"**Meta Title:** {content_dict['meta_title']} | **Meta Description:** {content_dict['meta_description']}")

        if scores["recommendations"]:
            st.warning("Recommendations:\n" + "\n".join([f"- {r}" for r in scores["recommendations"]]))

# -------------------------------------------------------------
# 3. BATCH GENERATOR PAGE
# -------------------------------------------------------------
elif menu == "📦 Batch Generator":
    st.markdown('<div class="main-header">Batch Description Generator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Upload CSV or JSON files to generate multiple descriptions</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV or JSON Catalog", type=["csv", "json"])

    if uploaded_file:
        file_bytes = uploaded_file.read()
        file_ext = uploaded_file.name.split(".")[-1].lower()

        valid_rows, invalid_rows = BatchProcessor.parse_file(file_bytes, file_ext)

        st.write(f"Parsed **{len(valid_rows)} valid products** and **{len(invalid_rows)} invalid rows**.")

        if valid_rows:
            df_preview = pd.DataFrame(valid_rows)
            st.dataframe(df_preview[["name", "category", "brand", "price"]].head())

            if st.button("🚀 Process Batch Generation"):
                job = BatchRepository.create_job(db, uploaded_file.name, file_ext, len(valid_rows))
                
                for row in valid_rows:
                    row.pop("row_number", None)
                    prod_create = ProductCreate(**row)
                    db_product = ProductRepository.create(db, prod_create)
                    BatchRepository.add_item(db, batch_job_id=job.id, row_number=1, product_id=db_product.id)

                BatchProcessor.process_batch(db, job, brand_settings)
                st.success("Batch processing completed!")

# -------------------------------------------------------------
# 4. PRODUCT CATALOGUE PAGE
# -------------------------------------------------------------
elif menu == "🛍️ Product Catalogue":
    st.markdown('<div class="main-header">Product Catalogue & Review</div>', unsafe_allow_html=True)

    items, total = ProductRepository.get_all(db, page_size=20)
    st.write(f"Showing {len(items)} products (Total: {total}):")

    data = []
    for item in items:
        p = item["product"]
        c = item["generated_content"]
        data.append({
            "ID": p["id"],
            "Name": p["name"],
            "Category": p["category"],
            "Price": f"${p['price']}" if p['price'] else "N/A",
            "Quality Score": f"{c['quality_score']}/100" if c else "N/A",
            "Status": c["status"] if c else "Not Generated"
        })

    st.table(pd.DataFrame(data))

# -------------------------------------------------------------
# 5. BRAND SETTINGS PAGE
# -------------------------------------------------------------
elif menu == "⚙️ Brand Settings":
    st.markdown('<div class="main-header">Brand Voice Rules Configuration</div>', unsafe_allow_html=True)

    with st.form("settings_form"):
        b_name = st.text_input("Brand Name", value=brand_settings.brand_name)
        b_voice = st.text_area("Brand Voice Description", value=brand_settings.brand_voice)
        pref_words = st.text_input("Preferred Words (comma-separated)", value=", ".join(brand_settings.preferred_words))
        proh_words = st.text_input("Prohibited Words (comma-separated)", value=", ".join(brand_settings.prohibited_words))
        disclaimer = st.text_input("Mandatory Disclaimer", value=brand_settings.mandatory_disclaimer or "")

        saved = st.form_submit_button("Save Brand Rules")
        if saved:
            SettingsRepository.update_settings(db, {
                "brand_name": b_name,
                "brand_voice": b_voice,
                "preferred_words": [w.strip() for w in pref_words.split(",") if w.strip()],
                "prohibited_words": [w.strip() for w in proh_words.split(",") if w.strip()],
                "mandatory_disclaimer": disclaimer
            })
            st.success("Brand settings updated!")

# -------------------------------------------------------------
# 6. RESPONSIBLE AI PAGE
# -------------------------------------------------------------
elif menu == "🛡️ Responsible AI":
    st.markdown('<div class="main-header">Responsible AI Governance</div>', unsafe_allow_html=True)
    st.info("1. Human-in-the-Loop review is required before publishing generated copy.")
    st.info("2. AI relies strictly on provided product specs and does not invent facts.")
    st.info("3. Zero PII collection policy.")
