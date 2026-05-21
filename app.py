"""
DTAA Advisor - Main Streamlit Application
AI-Powered Double Tax Treaty Advisory Suite for Chartered Accountants
Built under Income Tax Act, 2025 | Income Tax Rules, 2026
Kapoor Kumar and Associates | AICA Level 2 Capstone 2026
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="DTAA Advisor — Kapoor Kumar & Associates",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Main theme */
    .main-header {
        background: linear-gradient(135deg, #1F3864, #2E5090);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { color: #C9A22A; margin: 0; font-size: 2rem; }
    .main-header p { color: #CCCCCC; margin: 0.3rem 0 0; font-size: 0.9rem; }

    /* Risk badges */
    .risk-low { background: #C6EFCE; color: #375623; padding: 6px 14px;
                border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .risk-med { background: #FFF2CC; color: #7D6608; padding: 6px 14px;
                border-radius: 20px; font-weight: 600; font-size: 0.85rem; }
    .risk-high { background: #FCE4D6; color: #9C0006; padding: 6px 14px;
                 border-radius: 20px; font-weight: 600; font-size: 0.85rem; }

    /* Info boxes */
    .ita-box { background: #E6F1FB; border-left: 4px solid #1F3864;
               padding: 0.8rem 1rem; border-radius: 0 8px 8px 0;
               margin: 0.8rem 0; font-size: 0.85rem; color: #0C447C; }
    .warning-box { background: #FCE4D6; border-left: 4px solid #C0392B;
                   padding: 0.8rem 1rem; border-radius: 0 8px 8px 0;
                   margin: 0.8rem 0; font-size: 0.85rem; color: #7B0000; }
    .success-box { background: #E2EFDA; border-left: 4px solid #375623;
                   padding: 0.8rem 1rem; border-radius: 0 8px 8px 0;
                   margin: 0.8rem 0; font-size: 0.85rem; color: #375623; }

    /* Cards */
    .metric-card { background: white; border: 1px solid #E0E0E0;
                   border-radius: 10px; padding: 1rem; text-align: center; }
    .metric-card h3 { color: #C9A22A; font-size: 1.8rem; margin: 0; }
    .metric-card p { color: #666; font-size: 0.8rem; margin: 0.3rem 0 0; }

    /* Sidebar */
    .css-1d391kg { background: #1F3864; }

    /* Output area */
    .output-box { background: #F8F9FA; border: 1px solid #DEE2E6;
                  border-radius: 8px; padding: 1.2rem;
                  font-family: 'Segoe UI', sans-serif; line-height: 1.7; }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ── IMPORTS (lazy to handle missing packages gracefully) ──────────────────
def import_modules():
    try:
        from treaty_reader import (get_available_treaties, get_all_treaty_names,
                                   detect_country_from_filename, TREATIES_FOLDER)
        from advisor import (generate_advisory, generate_notice_reply,
                             generate_rate_comparison, classify_form_145,
                             get_claude_client)
        return True, get_available_treaties, get_all_treaty_names, \
               detect_country_from_filename, TREATIES_FOLDER, \
               generate_advisory, generate_notice_reply, \
               generate_rate_comparison, classify_form_145, get_claude_client
    except ImportError as e:
        return False, str(e), None, None, None, None, None, None, None, None


result = import_modules()
MODULES_OK = result[0]


# ── HEADER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>⚖️ DTAA Advisor</h1>
    <p>AI-Powered Double Tax Treaty Advisory Suite &nbsp;|&nbsp;
       Kapoor Kumar & Associates &nbsp;|&nbsp;
       Built under Income Tax Act, 2025 &nbsp;|&nbsp;
       Income Tax Rules, 2026</p>
</div>
""", unsafe_allow_html=True)

# ITA 2025 banner
st.markdown("""
<div class="ita-box">
<b>ITA 2025 Active:</b> Form 145 (replaces 15CA) &nbsp;|&nbsp;
Form 146 (replaces 15CB) &nbsp;|&nbsp;
Form 41 mandatory (replaces Form 10F) &nbsp;|&nbsp;
Section 393 (replaces Section 195) &nbsp;|&nbsp;
Rule 220(3) exempt list — 33 categories
</div>
""", unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚖️ DTAA Advisor")
    st.markdown("**Kapoor Kumar & Associates**")
    st.markdown("---")

    # API Key input
    st.markdown("#### 🔑 API Configuration")
    api_key_input = st.text_input(
        "Anthropic API Key",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        type="password",
        placeholder="sk-ant-...",
        help="Get from console.anthropic.com"
    )
    if api_key_input:
        os.environ["ANTHROPIC_API_KEY"] = api_key_input

    st.markdown("---")

    # Treaties status
    st.markdown("#### 📂 Treaty Library")
    treaties_path = Path(__file__).parent / "treaties"
    if treaties_path.exists():
        pdfs = list(treaties_path.glob("*.pdf"))
        st.success(f"✅ {len(pdfs)} treaty PDFs loaded")
        with st.expander("View loaded treaties"):
            for pdf in sorted(pdfs):
                if "afghanistan" not in pdf.name.lower():
                    st.caption(f"📄 {pdf.name[:50]}")
    else:
        st.error("❌ Treaties folder not found")
        st.caption("Expected: treaties/ folder in project root")
        st.info("Create treaties/ folder in your repo and add treaty PDFs")

    st.markdown("---")
    st.markdown("#### ℹ️ About")
    st.caption("AICA Level 2 Capstone Project")
    st.caption("May 2026")
    st.caption("90+ Indian DTAAs covered")


# ── STATS ROW ─────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><h3>90+</h3><p>Indian DTAAs</p></div>',
                unsafe_allow_html=True)
with col2:
    treaties_path = Path(__file__).parent / "treaties"
    count = len(list(treaties_path.glob("*.pdf"))) if treaties_path.exists() else 0
    st.markdown(f'<div class="metric-card"><h3>{count}</h3><p>PDFs Loaded</p></div>',
                unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><h3>4</h3><p>Core Modules</p></div>',
                unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><h3>&lt;10m</h3><p>Per Advisory</p></div>',
                unsafe_allow_html=True)

st.markdown("---")


# ── TABS ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 DTAA Rate Lookup",
    "📋 AI Advisory",
    "📄 Form 145 Classifier",
    "📨 Notice Reply Drafter",
    "📚 Treaty Search"
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — DTAA RATE LOOKUP
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### 🔍 DTAA Rate Comparator")
    st.caption("Compare DTAA rates vs domestic Section 393 rates. "
               "Green = DTAA beneficial. ⚠️ = Use domestic rate.")

    # Rate database
    rate_data = {
        "Country": ["USA", "UK", "UAE", "Singapore", "Mauritius", "Germany",
                    "Japan", "Canada", "Australia", "Netherlands", "France",
                    "Switzerland", "Hong Kong", "Malaysia", "China",
                    "New Zealand", "South Africa", "Sri Lanka", "Thailand", "Italy"],
        "Dividend DTAA%": [15, 15, 10, 15, "Nil", 10, 10, 15, 15, 10,
                            10, 10, 5, 10, 10, 15, 10, 15, 15, 15],
        "Interest DTAA%": [15, 15, 12.5, 15, "Nil", 10, 10, 15, 15, 10,
                            10, 10, 10, 10, 10, 10, 10, 10, 15, 15],
        "Royalty DTAA%": [15, 15, 10, 10, 15, 10, 10, 15, 10, 10,
                           10, 10, 10, 10, 10, 10, 10, 10, 15, 20],
        "FTS DTAA%": [15, 15, "N/A", 10, "N/A", 10, 10, 15, 10, 10,
                       10, 10, 10, 10, 10, "N/A", 10, 10, 15, 20],
        "MLI": ["No", "Yes", "Yes", "Yes", "Yes", "Yes", "No", "Yes", "Yes",
                 "Yes", "Yes", "Yes", "No", "Yes", "Partial", "Yes",
                 "No", "No", "No", "Yes"],
        "GAAR Risk": ["HIGH", "MEDIUM", "MEDIUM", "MEDIUM", "HIGH", "MEDIUM",
                       "LOW", "MEDIUM", "MEDIUM", "HIGH", "MEDIUM", "MEDIUM",
                       "LOW", "MEDIUM", "MEDIUM", "LOW", "LOW", "LOW",
                       "LOW", "MEDIUM"],
    }

    df = pd.DataFrame(rate_data)

    col_a, col_b = st.columns([1, 2])
    with col_a:
        selected_country = st.selectbox(
            "Select Country",
            options=["All Countries"] + df["Country"].tolist()
        )
        income_filter = st.selectbox(
            "Income Type",
            ["All", "Dividend", "Interest", "Royalty", "FTS"]
        )

    with col_b:
        # Domestic rates reference
        st.markdown("""
        <div class="ita-box">
        <b>Domestic Rates (Section 393 ITA 2025):</b><br>
        Dividend: 20% + SC + Cess &nbsp;|&nbsp;
        Interest: 20% + SC + Cess &nbsp;|&nbsp;
        Royalty: 10% + SC + Cess &nbsp;|&nbsp;
        FTS: 10% + SC + Cess
        </div>
        """, unsafe_allow_html=True)

        if selected_country == "Italy":
            st.markdown("""
            <div class="warning-box">
            ⚠️ <b>Italy Royalty Trap:</b> DTAA rate is 20% vs domestic 10%.
            Always use domestic rate for India-Italy royalty payments.
            </div>
            """, unsafe_allow_html=True)

    # Display table
    if selected_country != "All Countries":
        display_df = df[df["Country"] == selected_country]
    else:
        display_df = df

    # Color code GAAR risk
    def color_gaar(val):
        colors = {"HIGH": "background-color: #FCE4D6; color: #9C0006",
                  "MEDIUM": "background-color: #FFF2CC; color: #7D6608",
                  "LOW": "background-color: #E2EFDA; color: #375623"}
        return colors.get(val, "")

    styled_df = display_df.style.map(color_gaar, subset=["GAAR Risk"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    if selected_country != "All Countries":
        row = df[df["Country"] == selected_country].iloc[0]
        st.markdown("#### Key Notes")
        c1, c2, c3 = st.columns(3)
        with c1:
            risk = row["GAAR Risk"]
            icon = "🔴" if risk == "HIGH" else "🟡" if risk == "MEDIUM" else "🟢"
            st.metric("GAAR Risk", f"{icon} {risk}")
        with c2:
            st.metric("MLI Applies", "✅ Yes" if row["MLI"] == "Yes" else "❌ No")
        with c3:
            st.metric("Form 41", "✅ Mandatory")

        # AI Rate Analysis button
        if st.button(f"🤖 Get AI Rate Analysis for {selected_country}", type="primary"):
            if not os.getenv("ANTHROPIC_API_KEY") or \
               os.getenv("ANTHROPIC_API_KEY") == "sk-ant-your-key-here":
                st.error("Please enter your Anthropic API key in the sidebar first.")
            else:
                with st.spinner(f"Analysing India-{selected_country} DTAA rates..."):
                    try:
                        from advisor import generate_rate_comparison
                        result = generate_rate_comparison(selected_country)
                        st.markdown("#### AI Rate Analysis")
                        st.markdown(
                            f'<div class="output-box">{result}</div>',
                            unsafe_allow_html=True
                        )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — AI ADVISORY
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📋 AI-Powered DTAA Advisory")
    st.caption("Describe your cross-border transaction. "
               "The AI reads the actual treaty PDF and generates a structured advisory.")

    col1, col2 = st.columns(2)
    with col1:
        adv_country = st.selectbox(
            "Country of Payee/Recipient",
            ["USA", "UK", "UAE", "Singapore", "Mauritius", "Germany",
             "Japan", "Canada", "Australia", "Netherlands", "France",
             "Switzerland", "Hong Kong", "Malaysia", "China",
             "New Zealand", "South Africa", "Sri Lanka", "Thailand", "Italy"],
            key="adv_country"
        )
        adv_income = st.selectbox(
            "Nature of Income",
            ["Royalty / Software Licence", "Fees for Technical Services (FTS)",
             "Dividend", "Interest", "Capital Gains", "Salary / Employment Income",
             "Business Profits / PE income", "Other Income"],
            key="adv_income"
        )

    with col2:
        adv_amount = st.number_input(
            "Transaction Amount (Rs. Lakhs)",
            min_value=0.0, value=25.0, step=1.0
        )
        adv_trc = st.selectbox(
            "TRC Available?",
            ["Yes — TRC obtained", "No — TRC not yet obtained",
             "In process of obtaining"]
        )

    adv_details = st.text_area(
        "Transaction Details",
        placeholder="Describe the transaction: e.g. Indian company paying annual software licence "
                    "fee of Rs. 25 lakhs to a US-based company. Services involve use of proprietary "
                    "software under EULA. No copyright rights transferred.",
        height=100
    )

    use_treaty_pdf = st.checkbox(
        "📄 Use actual treaty PDF for analysis (recommended)",
        value=True
    )

    # Demo scenarios
    with st.expander("📌 Load Demo Scenario"):
        demo = st.radio("Select scenario:", [
            "Scenario 1: Software Licence Fee — India to USA",
            "Scenario 2: Dividend to NRI in UAE",
            "Scenario 3: FTS Payment — India to Singapore"
        ])
        if st.button("Load Scenario"):
            scenarios = {
                "Scenario 1: Software Licence Fee — India to USA": {
                    "country": "USA", "income": "Royalty / Software Licence",
                    "details": "Indian IT company paying annual software licence fee of Rs. 25 lakhs "
                               "to US-based software company. Standard EULA — no copyright rights transferred. "
                               "US company has no PE in India."
                },
                "Scenario 2: Dividend to NRI in UAE": {
                    "country": "UAE", "income": "Dividend",
                    "details": "Indian listed company paying dividend of Rs. 3 lakhs to UAE resident NRI "
                               "holding 5% shares. TRC available from UAE Federal Tax Authority."
                },
                "Scenario 3: FTS Payment — India to Singapore": {
                    "country": "Singapore", "income": "Fees for Technical Services (FTS)",
                    "details": "Indian company paid management consultancy fees of Rs. 25 lakhs to "
                               "Singapore entity. Services involved general business advisory — "
                               "no technical knowledge transferred to Indian company."
                }
            }
            st.session_state["demo_loaded"] = scenarios[demo]
            st.success(f"Scenario loaded! Scroll down and click Generate Advisory.")

    if st.button("🤖 Generate DTAA Advisory", type="primary", key="gen_advisory"):
        if not adv_details.strip():
            st.warning("Please describe the transaction details.")
        elif not os.getenv("ANTHROPIC_API_KEY") or \
             os.getenv("ANTHROPIC_API_KEY") == "sk-ant-your-key-here":
            st.error("Please enter your Anthropic API key in the sidebar first.")
        else:
            income_map = {
                "Royalty / Software Licence": "royalty",
                "Fees for Technical Services (FTS)": "fts",
                "Dividend": "dividend",
                "Interest": "interest",
                "Capital Gains": "capital gains",
                "Salary / Employment Income": "salary",
                "Business Profits / PE income": "business profits",
                "Other Income": "other"
            }
            income_type = income_map.get(adv_income, adv_income.lower())
            full_details = (f"{adv_details}\n\nAmount: Rs. {adv_amount} lakhs. "
                           f"TRC status: {adv_trc}.")

            with st.spinner("Reading treaty PDF and generating advisory... (20-30 seconds)"):
                try:
                    from advisor import generate_advisory
                    result = generate_advisory(
                        adv_country, income_type,
                        full_details, use_treaty_pdf
                    )
                    st.markdown("#### Advisory Output")
                    st.markdown(
                        f'<div class="output-box">{result}</div>',
                        unsafe_allow_html=True
                    )
                    st.download_button(
                        "📥 Download Advisory as Text",
                        data=result,
                        file_name=f"DTAA_Advisory_{adv_country}_{income_type}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error generating advisory: {str(e)}")
                    st.info("Check your API key in the sidebar.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — FORM 145 CLASSIFIER
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 📄 Form 145 / Form 146 Classifier")
    st.markdown("""
    <div class="ita-box">
    <b>ITA 2025 Update (w.e.f. 1 April 2026):</b>
    Form 15CA → <b>Form 145</b> &nbsp;|&nbsp;
    Form 15CB → <b>Form 146</b> &nbsp;|&nbsp;
    Rule 37BB → <b>Rule 220(3)</b> (33 exempt categories) &nbsp;|&nbsp;
    Form 10F → <b>Form 41</b> (mandatory)
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        f_payment = st.selectbox(
            "Nature of Payment",
            ["Royalty / Software Licence", "Fees for Technical Services",
             "Dividend to NRI", "Interest to NR Lender",
             "Capital Gains (NR seller)", "Salary to NR Employee",
             "Import of Goods", "Professional Services",
             "Rent of Foreign Property", "Partnership Profit",
             "RBI Exempt List Payment"]
        )
    with col2:
        f_amount = st.number_input("Amount (Rs. Lakhs)", min_value=0.0, value=10.0)
    with col3:
        f_taxable = st.selectbox(
            "Taxable in India?",
            ["Yes — chargeable to tax", "No — not chargeable", "Exempt under Rule 220(3)"]
        )

    f_dtaa = st.selectbox(
        "DTAA Benefit Claimed?",
        ["Yes — DTAA rate applied", "No — domestic rate applied",
         "Nil TDS — Article 7 (Business Profits, no PE)"]
    )

    # Instant classification logic
    st.markdown("#### Instant Classification")

    if f_payment == "Import of Goods" or "Exempt" in f_taxable:
        part = "PART D"
        part_color = "#DDEBF7"
        part_text_color = "#185FA5"
        form146 = "❌ Not Required"
        form41 = "❌ Not Required"
        note = "RBI exempt list under Rule 220(3) — No Form 145 required at all."
    elif "not chargeable" in f_taxable and f_amount <= 5:
        part = "PART A"
        part_color = "#E2EFDA"
        part_text_color = "#375623"
        form146 = "❌ Not Required"
        form41 = "✅ Required if DTAA claimed"
        note = "Non-taxable, ≤ Rs. 5 lakh. Remitter files on portal. No CA required."
    elif "not chargeable" in f_taxable and f_amount > 5:
        part = "PART B"
        part_color = "#FFF2CC"
        part_text_color = "#7D6608"
        form146 = "✅ REQUIRED"
        form41 = "✅ Mandatory"
        note = "Non-taxable but > Rs. 5 lakh. AO certificate OR Form 146 needed."
    else:
        part = "PART C"
        part_color = "#FCE4D6"
        part_text_color = "#9C0006"
        form146 = "✅ REQUIRED — Upload BEFORE Form 145 Part C"
        form41 = "✅ MANDATORY under Rule 75 / Section 159(8) ITA 2025"
        note = "Chargeable remittance. Form 146 (CA Certificate) mandatory."

    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    with col_r1:
        st.markdown(
            f'<div style="background:{part_color};color:{part_text_color};'
            f'padding:1rem;border-radius:8px;text-align:center;">'
            f'<b style="font-size:1.4rem">{part}</b><br>'
            f'<small>Form 145</small></div>',
            unsafe_allow_html=True
        )
    with col_r2:
        st.markdown(
            f'<div style="background:#F0F0F0;padding:1rem;border-radius:8px;">'
            f'<b>Form 146</b><br>{form146}</div>',
            unsafe_allow_html=True
        )
    with col_r3:
        st.markdown(
            f'<div style="background:#F0F0F0;padding:1rem;border-radius:8px;">'
            f'<b>Form 41 (ITA 2025)</b><br>{form41}</div>',
            unsafe_allow_html=True
        )
    with col_r4:
        st.markdown(
            f'<div style="background:#F0F0F0;padding:1rem;border-radius:8px;">'
            f'<b>TRC Required</b><br>{"✅ Yes" if "Not Required" not in form41 else "❌ No"}</div>',
            unsafe_allow_html=True
        )

    st.info(f"📌 {note}")

    if st.button("🤖 Get Detailed AI Classification", key="classify_btn"):
        if not os.getenv("ANTHROPIC_API_KEY") or \
           os.getenv("ANTHROPIC_API_KEY") == "sk-ant-your-key-here":
            st.error("Please enter your Anthropic API key in the sidebar.")
        else:
            with st.spinner("Generating detailed classification..."):
                try:
                    from advisor import classify_form_145
                    result = classify_form_145(f_payment, f_amount, f_taxable, f_dtaa)
                    st.markdown(
                        f'<div class="output-box">{result}</div>',
                        unsafe_allow_html=True
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — NOTICE REPLY DRAFTER
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 📨 IT Department Notice Reply Drafter")
    st.caption("Generate submission-ready formal replies citing treaty articles, "
               "Supreme Court judgments, and CBDT circulars.")

    col1, col2 = st.columns(2)
    with col1:
        n_country = st.selectbox(
            "Country of Foreign Entity",
            ["USA", "UK", "UAE", "Singapore", "Mauritius", "Germany",
             "Japan", "Canada", "Australia", "Netherlands", "France",
             "Switzerland", "Hong Kong", "Malaysia", "China"],
            key="n_country"
        )
        n_type = st.selectbox(
            "Notice Type",
            ["FTS / Royalty characterisation dispute",
             "PE allegation — Business Profits",
             "GAAR / Treaty Shopping challenge",
             "Short deduction / Non-deduction of TDS",
             "MFN clause dispute",
             "Beneficial ownership challenge",
             "Transfer Pricing adjustment"]
        )
    with col2:
        n_article = st.text_input(
            "Treaty Article in dispute",
            placeholder="e.g. Article 12 (FTS) vs Article 7 (Business Profits)"
        )
        n_section = st.text_input(
            "ITA 2025 Section",
            placeholder="e.g. Section 393"
        )

    n_facts = st.text_area(
        "Facts of the Case",
        placeholder="Describe: what payment was made, to whom, what TDS was deducted, "
                    "what is the department's objection, what documents were obtained...",
        height=120
    )

    if st.button("📝 Draft Notice Reply", type="primary", key="draft_notice"):
        if not n_facts.strip():
            st.warning("Please describe the facts of the case.")
        elif not os.getenv("ANTHROPIC_API_KEY") or \
             os.getenv("ANTHROPIC_API_KEY") == "sk-ant-your-key-here":
            st.error("Please enter your Anthropic API key in the sidebar.")
        else:
            with st.spinner("Drafting formal reply (30-40 seconds)..."):
                try:
                    from advisor import generate_notice_reply
                    result = generate_notice_reply(n_type, n_country, n_facts, n_article)
                    st.markdown("#### Draft Notice Reply")
                    st.markdown(
                        f'<div class="output-box">{result}</div>',
                        unsafe_allow_html=True
                    )
                    st.download_button(
                        "📥 Download Reply as Text",
                        data=result,
                        file_name=f"Notice_Reply_{n_country}_{n_type[:20]}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {str(e)}")


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — TREATY SEARCH
# ════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("### 📚 Treaty Text Search")
    st.caption("Search and view actual CBDT treaty text from the treaty library.")

    treaties_path = Path(__file__).parent / "treaties"

    if not treaties_path.exists():
        st.error("❌ Treaties folder not found")
        st.info("Add a 'treaties/' folder to your GitHub repository and commit your treaty PDFs into it.")
    else:
        pdfs = sorted([p for p in treaties_path.glob("*.pdf")
                       if "afghanistan" not in p.name.lower()])

        if not pdfs:
            st.warning("No PDF files found in the treaties/ folder in your repository.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                selected_pdf = st.selectbox(
                    "Select Treaty PDF",
                    options=[p.name for p in pdfs]
                )
            with col2:
                search_topic = st.text_input(
                    "Search Topic",
                    placeholder="e.g. royalties, dividends, permanent establishment, FTS"
                )

            if st.button("🔍 Search Treaty", key="search_treaty"):
                selected_path = treaties_path / selected_pdf
                with st.spinner("Reading PDF..."):
                    try:
                        from treaty_reader import (extract_text_from_pdf,
                                                    find_relevant_sections)
                        text = extract_text_from_pdf(selected_path, max_pages=30)

                        if search_topic:
                            relevant = find_relevant_sections(text, search_topic)
                            if relevant:
                                st.markdown(f"#### Results for '{search_topic}'")
                                st.markdown(
                                    f'<div class="output-box">{relevant}</div>',
                                    unsafe_allow_html=True
                                )
                            else:
                                st.info(f"No specific results for '{search_topic}'. "
                                        f"Showing first 2000 characters.")
                                st.text(text[:2000])
                        else:
                            st.markdown("#### Treaty Text (first 3000 characters)")
                            st.text(text[:3000])

                    except Exception as e:
                        st.error(f"Error reading PDF: {str(e)}")

            # Show PDF info
            st.markdown("#### Available Treaties")
            pdf_info = []
            for p in pdfs:
                size_kb = p.stat().st_size // 1024
                pdf_info.append({
                    "File Name": p.name[:60],
                    "Size (KB)": size_kb,
                    "Type": "MLI Synthesised" if "synthes" in p.name.lower()
                            else "Comprehensive"
                })
            st.dataframe(pd.DataFrame(pdf_info), use_container_width=True, hide_index=True)


# ── FOOTER ────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#888; font-size:0.8rem;">
DTAA Advisor — Kapoor Kumar & Associates &nbsp;|&nbsp;
AICA Level 2 Capstone 2026 &nbsp;|&nbsp;
Built under Income Tax Act, 2025 | Income Tax Rules, 2026 &nbsp;|&nbsp;
Form 145 | Form 146 | Form 41 | Section 393<br>
<i>This tool is for professional guidance only. Verify with actual treaty text before filing.</i>
</div>
""", unsafe_allow_html=True)
