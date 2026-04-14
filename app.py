import streamlit as st
from agent import process

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="NBA Championship Predictor",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

import base64
import os

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_img = get_base64_of_bin_file("bg.jpg")

# ==========================================
# Session State
# ==========================================
if "result" not in st.session_state:
    st.session_state.result = None
if "active_query" not in st.session_state:
    st.session_state.active_query = ""

# Determine background CSS dynamically
if st.session_state.result is None:
    # Front page: show subtle watermark background
    bg_css = f'background-image: linear-gradient(rgba(250, 251, 252, 0.88), rgba(250, 251, 252, 0.88)), url("data:image/jpeg;base64,{bg_img}"); background-size: cover; background-position: center; background-attachment: fixed;'
else:
    # Results page: plain background for readability
    bg_css = "background: #fafbfc;"

# ==========================================
# Custom CSS — Manus-Inspired Design
# ==========================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global */
.stApp {{ 
    font-family: 'Inter', sans-serif; 
    color: #1f2937; 
    font-family: 'Inter', sans-serif; 
    color: #1f2937; 
    {bg_css}
}}
.stMarkdown {{ color: #1f2937; }}
p, h1, h2, h3, h4, h5, h6, li {{ color: #1f2937 !important; }}

/* Hero heading */
.hero-title {{
    text-align: center; font-size: 3.2rem; font-weight: 700;
    color: #111827 !important; margin-top: 14vh; margin-bottom: 0.8rem;
    letter-spacing: -0.035em;
}}
.hero-subtitle {{
    text-align: center; font-size: 1.35rem; color: #6b7280 !important;
    margin-bottom: 2.5rem; font-weight: 400;
}}

/* Text input */
div[data-testid="stTextInput"] > div > div > input {{
    border-radius: 14px !important; border: 1.5px solid #e5e7eb !important;
    padding: 14px 18px !important; font-size: 1rem !important;
    background: #ffffff !important; color: #1f2937 !important;
    caret-color: #1f2937 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}}
div[data-testid="stTextInput"] > div > div > input:focus {{
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}}

/* Buttons */
.stButton > button {{
    border-radius: 12px !important; font-weight: 500 !important;
    transition: all 0.2s ease !important;
}}
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border: none !important; color: white !important;
}}
.stButton > button[kind="primary"]:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35) !important;
}}
.stButton > button[kind="secondary"] {{
    background: #f3f4f6 !important; border: 1px solid #e5e7eb !important;
    color: #374151 !important;
}}
.stButton > button[kind="secondary"]:hover {{ background: #e5e7eb !important; }}

/* Sidebar & misc */
section[data-testid="stSidebar"] {{ background: #ffffff; border-right: 1px solid #f0f0f0; }}
.quick-label {{ text-align: center; color: #b0b7c3; font-size: 0.85rem; margin: 1.2rem 0 0.6rem; }}
.status-badge {{
    display: inline-block; background: linear-gradient(135deg, #10b981, #059669);
    color: white; padding: 5px 16px; border-radius: 20px;
    font-size: 0.82rem; font-weight: 500;
}}
.query-box {{
    background: #fff; border: 1px solid #e5e7eb; border-radius: 12px;
    padding: 1rem 1.25rem; margin-bottom: 1.5rem; color: #6b7280;
}}

/* Hide default header/footer */
#MainMenu, footer, header {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)


# ==========================================
# Sidebar — Configuration
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.3, 0.1,
        help="Higher = more creative, lower = more focused",
    )
    num_teams = st.selectbox(
        "Teams to Analyze", [3, 5, 8], index=1,
        help="Number of NBA teams the researcher will investigate",
    )
    depth = st.selectbox(
        "Analysis Depth", ["Quick", "Standard", "Deep"], index=1,
        help="Quick ≈ 30s | Standard ≈ 60s | Deep ≈ 90s+",
    )
    st.divider()
    st.caption("🏀 **NBA Championship Predictor**")
    st.caption("Powered by CrewAI × DeepSeek")
    st.divider()
    
    import os
    if os.path.exists("front_page.png"):
        st.image("front_page.png", caption="Dashboard Overview", use_container_width=True)
    if os.path.exists("results_page.png"):
        st.image("results_page.png", caption="Analysis Results", use_container_width=True)

# ==========================================



# ==========================================
# View: Query Page (Manus-Style)
# ==========================================
if st.session_state.result is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            '<p class="hero-title">🏀 What can I predict for you?</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="hero-subtitle">'
            'AI-powered NBA Championship predictions using multi-agent intelligence'
            '</p>',
            unsafe_allow_html=True,
        )

        # --- Query Input ---
        query = st.text_input(
            "query",
            placeholder="Ask about NBA championship predictions…",
            label_visibility="collapsed",
            key="user_query",
        )
        submitted = st.button(
            "🔍  Analyze", use_container_width=True, type="primary"
        )

        # --- Quick-Action Buttons ---
        st.markdown('<p class="quick-label">or try a quick action</p>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏆 Predict Champion", use_container_width=True):
                st.session_state.active_query = (
                    "Predict the 2026 NBA Championship winner with data-backed analysis"
                )
                st.rerun()
            if st.button("📊 Top Contenders", use_container_width=True):
                st.session_state.active_query = (
                    "Analyze the top NBA championship contenders for the 2025-26 season"
                )
                st.rerun()
        with c2:
            if st.button("🌟 MVP Candidates", use_container_width=True):
                st.session_state.active_query = (
                    "Analyze the current top MVP candidates for the 2025-26 NBA season"
                )
                st.rerun()
            if st.button("🔥 Playoff Preview", use_container_width=True):
                st.session_state.active_query = (
                    "Preview the 2026 NBA Playoffs bracket and predict the outcomes"
                )
                st.rerun()

    # --- Determine active query ---
    final_query = (query.strip() if submitted and query else st.session_state.active_query)

    # --- Input Validation ---
    if submitted and not query.strip():
        st.warning("⚠️ Please enter a question before submitting.")

    # --- Run Agent Pipeline ---
    elif final_query:
        st.session_state.active_query = final_query
        with st.status("🏀 Running NBA Analysis Pipeline…", expanded=True) as status:
            st.write("🔍 **Processing** — Researching and writing analysis in one shot…")
            try:
                # Validate API Key exists before running
                import os
                if not os.getenv("DEEPSEEK_API_KEY"):
                    raise ValueError("DEEPSEEK_API_KEY environment variable is not set. Please check your .env file.")
                
                result = process(
                    final_query,
                    temperature=temperature,
                    num_teams=num_teams,
                    depth=depth,
                )

                if not result or str(result).strip() == "":
                    raise RuntimeError("The agent returned an empty response. This might be due to an API timeout or rate limit.")

                st.session_state.result = result
                status.update(label="✅ Analysis Complete!", state="complete")
                st.success("Done! Scroll down or click below to view results.")
                st.rerun()
            except ValueError as ve:
                status.update(label="❌ Configuration Error", state="error")
                st.error(f"**Configuration Error:** {ve}")
                st.session_state.active_query = ""
            except Exception as e:
                status.update(label="❌ Analysis Failed", state="error")
                error_msg = str(e)
                if "rate_limit" in error_msg.lower() or "429" in error_msg:
                    st.error("**Rate Limit Exceeded:** The API is currently blocking requests due to too many attempts. Please wait a few minutes and try again.")
                elif "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                    st.error("**Network Error:** The connection to the LLM API timed out or failed. Please check your internet connection or try again later.")
                else:
                    st.error(f"**Agent execution encountered an error:**\n\n```\n{error_msg}\n```")
                st.session_state.active_query = ""


# ==========================================
# View: Results Page
# ==========================================
else:
    st.markdown(
        '<span class="status-badge">✅ Analysis Complete</span>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="query-box">📝 <strong>Query:</strong> '
        f'{st.session_state.active_query}</div>',
        unsafe_allow_html=True,
    )

    # Render the agent's Markdown output
    st.markdown(st.session_state.result)

    st.divider()
    if st.button("🔄 New Prediction", type="primary"):
        st.session_state.result = None
        st.session_state.active_query = ""
        st.rerun()
