import base64
from datetime import datetime
import html
from pathlib import Path
import re
import streamlit as st
from src.task10_generation import generate_with_citation

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="UniLib Bot • Bạn Thân Chốn Thư Viện",
    page_icon="🦉",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# ASSET HELPER: LOAD OWL BOT ICON AS BASE64 DATA URI
# ==============================================================================
@st.cache_data
def get_owl_bot_base64() -> str:
    """Loads the 3D Owl Bot icon as a base64 encoded data URI."""
    possible_paths = [
        Path(__file__).parent / "assets" / "owl_bot.jpg",
        Path("/Users/doanhuy/.gemini/antigravity/brain/54063422-bc63-49d1-8984-ae976a108402/.user_uploaded/media_1789893760908.jpg"),
    ]
    for p in possible_paths:
        if p.exists():
            with open(p, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{encoded}"
    return "https://api.dicebear.com/7.x/bottts/svg?seed=UniLib"

OWL_ICON_URI = get_owl_bot_base64()

# ==============================================================================
# CUSTOM CSS & DESIGN SYSTEM (Pixel-matched to Image 2)
# ==============================================================================
CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {{
    --bg-page: #F8FAFC;
    --bg-card: #FFFFFF;
    --primary-purple: #5B50E6;
    --primary-purple-hover: #4C41D4;
    --primary-purple-light: #EEF0FD;
    --text-heading: #1E293B;
    --text-body: #334155;
    --text-muted: #64748B;
    --text-subtle: #94A3B8;
    --border-light: #F1F5F9;
    --border-card: #E2E8F0;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --radius-full: 9999px;
    --shadow-subtle: 0 1px 3px rgba(0, 0, 0, 0.03);
    --shadow-card: 0 1px 3px rgba(0, 0, 0, 0.05);
    --shadow-avatar: 0 12px 32px rgba(79, 70, 229, 0.12);
}}

/* Global resets & Multi-layer Gradient Background for Main Content */
html, body, [class*="css"], .stApp {{
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: 
        radial-gradient(ellipse 70% 55% at 85% 15%, rgba(236, 253, 245, 0.75) 0%, rgba(236, 253, 245, 0) 70%),
        radial-gradient(ellipse 65% 50% at 15% 10%, rgba(243, 232, 255, 0.65) 0%, rgba(243, 232, 255, 0) 70%),
        radial-gradient(circle 800px at 50% 45%, rgba(255, 255, 255, 0.88) 0%, rgba(250, 250, 250, 0.6) 65%, transparent 100%),
        linear-gradient(160deg, #F8FAFC 0%, #F5F3FF 50%, #F0FDF4 100%) fixed !important;
    color: var(--text-body) !important;
    -webkit-font-smoothing: antialiased;
}}

[data-testid="stAppViewContainer"],
section[data-testid="stMain"],
.main {{
    background: 
        radial-gradient(ellipse 70% 55% at 85% 15%, rgba(236, 253, 245, 0.75) 0%, rgba(236, 253, 245, 0) 70%),
        radial-gradient(ellipse 65% 50% at 15% 10%, rgba(243, 232, 255, 0.65) 0%, rgba(243, 232, 255, 0) 70%),
        radial-gradient(circle 800px at 50% 45%, rgba(255, 255, 255, 0.88) 0%, rgba(250, 250, 250, 0.6) 65%, transparent 100%),
        linear-gradient(160deg, #F8FAFC 0%, #F5F3FF 50%, #F0FDF4 100%) fixed !important;
}}

/* Hide Streamlit default header decoration completely */
header[data-testid="stHeader"],
[data-testid="stHeader"] {{
    background-color: transparent !important;
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}}
#MainMenu, footer {{
    visibility: hidden;
    display: none !important;
}}

/* Main Block Container adjustments (full width so top bar reaches near sidebar) */
.main .block-container,
[data-testid="stMainBlockContainer"],
[data-testid="block-container"],
.stMainBlockContainer,
section[data-testid="stMain"] > div {{
    padding-top: 0.5rem !important;
    padding-bottom: 5.5rem !important;
    padding-left: 1.25rem !important;
    padding-right: 1.5rem !important;
    max-width: 100% !important;
    margin: 0 !important;
}}

/* Centered container for main landing & chat content */
.main-centered-container {{
    max-width: 760px;
    margin: 0 auto;
    width: 100%;
}}

/* ==============================================================================
   SIDEBAR STYLING — LOCKED FLUSH AT TOP & BOTTOM
   ============================================================================== */
[data-testid="stSidebar"] {{
    background-color: #FFFFFF !important;
    border-right: 1px solid #F1F5F9 !important;
    box-shadow: 1px 0 8px rgba(0, 0, 0, 0.02) !important;
    position: relative !important;
    height: 100vh !important;
}}

/* Hide Streamlit default sidebar header to eliminate giant top space */
[data-testid="stSidebarHeader"],
header[data-testid="stSidebarHeader"] {{
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}}

/* Reset Streamlit default sidebar content paddings */
[data-testid="stSidebarContent"] {{
    height: 100vh !important;
    max-height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    padding: 0.5rem 0.8rem 0 0.8rem !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}}

[data-testid="stSidebarUserContent"] {{
    display: flex !important;
    flex-direction: column !important;
    flex: 1 1 auto !important;
    min-height: calc(100vh - 1.2rem) !important;
    height: 100% !important;
    justify-content: space-between !important;
    box-sizing: border-box !important;
    padding: 0 !important;
}}

/* Sidebar Brand Header (tight to top) */
.sidebar-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 4px 10px 4px;
    border-bottom: 1px solid #F8FAFC;
    margin-bottom: 10px;
}}
.sidebar-brand {{
    display: flex;
    align-items: center;
    gap: 10px;
}}
.sidebar-brand-avatar {{
    width: 32px;
    height: 32px;
    border-radius: 9px;
    object-fit: cover;
    box-shadow: 0 2px 6px rgba(79, 70, 229, 0.15);
}}
.sidebar-brand-title {{
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--text-heading);
    line-height: 1.2;
}}
.sidebar-brand-subtitle {{
    font-size: 0.7rem;
    color: var(--text-muted);
    font-weight: 500;
}}
.sidebar-collapse-btn {{
    background: transparent;
    border: none;
    color: var(--text-subtle);
    cursor: pointer;
    padding: 4px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    width: 24px;
    height: 24px;
}}
.sidebar-collapse-btn svg {{
    width: 18px;
    height: 18px;
    stroke: currentColor;
    fill: none;
    stroke-width: 1.5;
    stroke-linecap: round;
    stroke-linejoin: round;
}}
.sidebar-collapse-btn:hover {{
    color: var(--text-heading);
}}

/* "+ Đoạn chat mới" Button */
[data-testid="stSidebar"] div.stButton > button {{
    background-color: var(--primary-purple) !important;
    color: #FFFFFF !important;
    border-radius: var(--radius-md) !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 9px 14px !important;
    box-shadow: 0 3px 10px rgba(79, 70, 229, 0.25) !important;
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;
    width: 100% !important;
    margin-bottom: 12px !important;
    transition: all 0.15s ease !important;
}}
[data-testid="stSidebar"] div.stButton > button:hover {{
    background-color: var(--primary-purple-hover) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 14px rgba(79, 70, 229, 0.35) !important;
}}
[data-testid="stSidebar"] div.stButton > button::after {{
    content: "Ctrl K";
    background: rgba(255, 255, 255, 0.22);
    padding: 2px 6px;
    border-radius: 5px;
    font-size: 0.68rem;
    font-weight: 500;
    margin-left: auto;
}}

/* Sidebar Chat History */
.sidebar-section-title {{
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--text-subtle);
    padding: 4px 8px 3px 8px;
}}
.sidebar-history-item {{
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 7px 10px;
    border-radius: 10px;
    color: var(--text-body);
    font-size: 0.82rem;
    font-weight: 500;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.15s ease;
    margin-bottom: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.sidebar-history-item:hover {{
    background-color: #F8FAFC;
    color: var(--primary-purple);
}}
.sidebar-history-item.active {{
    background-color: var(--primary-purple-light);
    color: var(--primary-purple);
    font-weight: 600;
}}
.sidebar-history-icon {{
    flex-shrink: 0;
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
}}
.sidebar-history-icon svg {{
    width: 16px;
    height: 16px;
    stroke: var(--text-subtle);
    fill: none;
    stroke-width: 1.5;
    stroke-linecap: round;
    stroke-linejoin: round;
}}

/* User Profile Section at Bottom (FLUSH SÁT BOTTOM 100%) */
[data-testid="stSidebarUserContent"] > div:has(.sidebar-user-footer) {{
    margin-top: auto !important;
    position: sticky !important;
    bottom: 0 !important;
    background-color: #FFFFFF !important;
    z-index: 99 !important;
    width: 100% !important;
    padding-bottom: 4px !important;
}}
.sidebar-user-footer {{
    position: sticky !important;
    bottom: 0 !important;
    margin-top: auto !important;
    background-color: #FFFFFF !important;
    padding: 12px 4px 8px 4px !important;
    border-top: 1px solid #F1F5F9 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    width: 100% !important;
    z-index: 99 !important;
}}
.user-info-wrapper {{
    display: flex;
    align-items: center;
    gap: 9px;
}}
.user-avatar-badge-wrapper {{
    position: relative;
    width: 32px;
    height: 32px;
}}
.user-avatar-badge {{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #7C3AED;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
}}
.user-online-indicator {{
    position: absolute;
    bottom: -1px;
    right: -1px;
    width: 9px;
    height: 9px;
    background-color: #10B981;
    border: 2px solid #FFFFFF;
    border-radius: 50%;
}}
.user-name {{
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--text-heading);
    line-height: 1.2;
}}
.user-id {{
    font-size: 0.68rem;
    color: var(--text-muted);
    font-weight: 500;
}}
.user-settings-btn {{
    background: transparent;
    border: none;
    color: var(--text-subtle);
    font-size: 15px;
    cursor: pointer;
    padding: 5px;
    border-radius: 6px;
    transition: color 0.15s;
}}
.user-settings-btn:hover {{
    color: var(--text-heading);
}}

/* ==============================================================================
   TOP NAVIGATION BAR
   ============================================================================== */
.top-nav-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 4px 10px 4px;
    margin-bottom: 0;
    background: transparent;
}}
.top-nav-left {{
    display: flex;
    align-items: center;
    gap: 10px;
}}
.top-nav-brand {{
    font-weight: 700;
    font-size: 0.95rem;
    color: var(--text-heading);
}}
.top-nav-tag {{
    background-color: var(--primary-purple-light);
    color: #4338CA;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: var(--radius-full);
}}
.top-nav-status {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.72rem;
    font-weight: 500;
    color: #059669;
}}
.status-dot-pulse {{
    width: 6px;
    height: 6px;
    background-color: #10B981;
    border-radius: 50%;
}}

.top-nav-right {{
    display: flex;
    align-items: center;
    gap: 12px;
}}
.top-nav-link-opac {{
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--primary-purple);
    background-color: var(--primary-purple-light);
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 5px 12px;
    border-radius: var(--radius-full);
    transition: opacity 0.15s;
}}
.top-nav-link-opac:hover {{
    opacity: 0.85;
}}
.top-nav-icon-btn {{
    background: transparent;
    border: none;
    color: var(--text-muted);
    font-size: 14px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 3px;
    padding: 4px 6px;
    font-weight: 600;
    font-size: 0.78rem;
}}
.top-nav-icon-btn:hover {{
    color: var(--text-heading);
}}

/* ==============================================================================
   SCREEN 1: LANDING SCREEN
   ============================================================================== */
.landing-wrapper {{
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    min-height: auto;
    padding: 0 10px 10px 10px;
}}
.landing-hero {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 10px;
}}
.landing-avatar-card {{
    position: relative;
    width: 92px;
    height: 92px;
    border-radius: 18px;
    background: linear-gradient(135deg, #E0F2FE 0%, #DBEAFE 40%, #EDE9FE 100%);
    padding: 6px;
    box-shadow: var(--shadow-card);
    border: none;
    margin-bottom: 10px;
}}
.landing-avatar-img {{
    width: 100%;
    height: 100%;
    border-radius: 13px;
    object-fit: cover;
}}
.landing-avatar-tag {{
    position: absolute;
    bottom: -11px;
    left: 50%;
    transform: translateX(-50%);
    background: #FFFFFF;
    border: 1px solid #F1F5F9;
    border-radius: var(--radius-full);
    padding: 2px 12px;
    font-size: 0.7rem;
    font-weight: 700;
    color: var(--text-heading);
    white-space: nowrap;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}}
.landing-title {{
    font-size: 1.55rem;
    font-weight: 800;
    color: var(--text-heading);
    margin-top: 10px;
    margin-bottom: 4px;
    letter-spacing: -0.02em;
}}
.landing-title-accent {{
    color: #4F46E5;
}}
.landing-subtitle {{
    font-size: 0.86rem;
    color: var(--text-muted);
    max-width: 580px;
    margin-bottom: 14px;
    line-height: 1.45;
}}

/* Form Input Styling on Landing (Single Unified White Pill Box) */
div[data-testid="stForm"] {{
    background: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 9999px !important;
    padding: 4px 6px 4px 18px !important;
    max-width: 680px !important;
    margin: 0 auto 16px auto !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05) !important;
    transition: all 0.2s ease !important;
    box-sizing: border-box !important;
    width: 100% !important;
}}
div[data-testid="stForm"]:focus-within {{
    border-color: #5B50E6 !important;
    box-shadow: 0 6px 24px rgba(91, 80, 230, 0.15) !important;
}}
div[data-testid="stForm"] > div:first-child {{
    width: 100% !important;
}}
div[data-testid="stForm"] [data-testid="stHorizontalBlock"] {{
    align-items: center !important;
    width: 100% !important;
    gap: 8px !important;
}}
/* Strip all default Streamlit input borders & backgrounds */
div[data-testid="stForm"] div[data-testid="stTextInput"],
div[data-testid="stForm"] div[data-testid="stTextInput"] > div,
div[data-testid="stForm"] div[data-testid="stTextInput"] > div > div,
div[data-testid="stForm"] div[data-testid="stTextInput"] input {{
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
}}
div[data-testid="stForm"] div[data-testid="stTextInput"] input {{
    padding: 8px 0 !important;
    font-size: 0.86rem !important;
    color: #1E293B !important;
    font-family: inherit !important;
}}
div[data-testid="stForm"] div[data-testid="stTextInput"] input::placeholder {{
    color: #94A3B8 !important;
    font-size: 0.84rem !important;
}}
/* Submit button as purple pill on the right */
div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] {{
    margin: 0 !important;
    display: flex !important;
    align-items: center !important;
}}
div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button {{
    background-color: #5B50E6 !important;
    background: #5B50E6 !important;
    color: #FFFFFF !important;
    border-radius: 9999px !important;
    padding: 8px 20px !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 2px 6px rgba(91, 80, 230, 0.3) !important;
    white-space: nowrap !important;
    transition: all 0.15s ease !important;
}}
div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] button:hover {{
    background-color: #4C41D4 !important;
    transform: translateY(-1px) !important;
}}

/* Suggestion Chips styling (clean white pills) */
[data-testid="stMain"] div.stButton > button,
[data-testid="stMainBlockContainer"] div.stButton > button,
.stMain div.stButton > button,
.main div.stButton > button,
div[data-testid="stButton"] > button:not([data-testid="stSidebar"] *) {{
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 9999px !important;
    color: #334155 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 7px 14px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    white-space: nowrap !important;
    transition: all 0.15s ease !important;
    line-height: 1.4 !important;
    margin-bottom: 8px !important;
}}

[data-testid="stMain"] div.stButton > button *,
[data-testid="stMainBlockContainer"] div.stButton > button *,
.stMain div.stButton > button *,
.main div.stButton > button *,
div[data-testid="stButton"] > button:not([data-testid="stSidebar"] *) * {{
    color: #334155 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
}}

[data-testid="stMain"] div.stButton > button:hover,
[data-testid="stMainBlockContainer"] div.stButton > button:hover,
.stMain div.stButton > button:hover,
.main div.stButton > button:hover,
div[data-testid="stButton"] > button:not([data-testid="stSidebar"] *):hover {{
    background: #EEF0FD !important;
    background-color: #EEF0FD !important;
    border-color: #C7D2FE !important;
    color: #5B50E6 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(91, 80, 230, 0.12) !important;
}}

[data-testid="stMain"] div.stButton > button:hover *,
[data-testid="stMainBlockContainer"] div.stButton > button:hover *,
.stMain div.stButton > button:hover *,
.main div.stButton > button:hover *,
div[data-testid="stButton"] > button:not([data-testid="stSidebar"] *):hover * {{
    color: #5B50E6 !important;
}}

[data-testid="stMain"] div.stButton > button:active,
[data-testid="stMainBlockContainer"] div.stButton > button:active,
.stMain div.stButton > button:active,
.main div.stButton > button:active,
div[data-testid="stButton"] > button:not([data-testid="stSidebar"] *):active {{
    background: #E0E7FF !important;
    background-color: #E0E7FF !important;
    border-color: #A5B4FC !important;
    color: #4338CA !important;
    transform: translateY(0px) !important;
}}

/* Core Regulations Cards */
.core-rules-section {{
    width: 100%;
    max-width: 760px;
    text-align: left;
    margin: 0 auto;
}}
.core-rules-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    padding: 0 4px;
}}
.core-rules-title {{
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-subtle);
}}
.core-rules-badge {{
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--primary-purple);
    background-color: var(--primary-purple-light);
    padding: 2px 9px;
    border-radius: var(--radius-full);
}}

.core-rules-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}}
.rule-card {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: var(--radius-md);
    padding: 11px 13px;
    box-shadow: var(--shadow-subtle);
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.2s ease;
}}
.rule-card:hover {{
    transform: translateY(-2px);
    box-shadow: var(--shadow-card);
    border-color: #CBD5E1;
}}
.rule-card-icon {{
    width: 32px;
    height: 32px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
}}
.rule-card-icon.blue {{
    background-color: #EFF6FF;
    color: #2563EB;
}}
.rule-card-icon.green {{
    background-color: #ECFDF5;
    color: #059669;
}}
.rule-card-icon.orange {{
    background-color: #FFFBEB;
    color: #D97706;
}}
.rule-card-icon.red {{
    background-color: #FEF2F2;
    color: #DC2626;
}}
.rule-card-label {{
    font-size: 0.68rem;
    font-weight: 500;
    color: var(--text-muted);
    margin-bottom: 2px;
}}
.rule-card-value {{
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--text-heading);
    margin-bottom: 1px;
}}
.rule-card-sub {{
    font-size: 0.68rem;
    color: var(--text-subtle);
}}

/* ==============================================================================
   SCREEN 2: ACTIVE CHAT SCREEN
   ============================================================================== */
.chat-container {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 20px;
}}
.chat-date-divider {{
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 4px 0 12px 0;
}}
.chat-date-badge {{
    background-color: #F1F5F9;
    color: var(--text-muted);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 3px 12px;
    border-radius: var(--radius-full);
}}

/* User Message */
.chat-row-user {{
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 5px;
    margin-bottom: 6px;
}}
.chat-meta-user {{
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 0.72rem;
    color: var(--text-muted);
    font-weight: 600;
}}
.user-avatar-mini {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #7C3AED;
    color: #FFFFFF;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.62rem;
    font-weight: 700;
}}
.chat-bubble-user {{
    background-color: #4F46E5;
    color: #FFFFFF !important;
    border-radius: 16px 4px 16px 16px;
    padding: 12px 17px;
    max-width: 68%;
    font-size: 0.85rem;
    line-height: 1.55;
    box-shadow: 0 3px 10px rgba(79, 70, 229, 0.2);
}}

/* Bot Message */
.chat-row-bot {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 10px;
}}
.bot-avatar-img {{
    width: 36px;
    height: 36px;
    border-radius: 11px;
    object-fit: cover;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    flex-shrink: 0;
}}
.chat-content-bot {{
    flex: 1;
    max-width: 85%;
}}
.chat-meta-bot {{
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 0.72rem;
    margin-bottom: 5px;
}}
.chat-meta-bot-name {{
    font-weight: 700;
    color: var(--text-heading);
}}
.chat-meta-bot-tag {{
    color: #4338CA;
    background-color: var(--primary-purple-light);
    font-size: 0.66rem;
    font-weight: 600;
    padding: 2px 7px;
    border-radius: var(--radius-full);
}}
.chat-meta-bot-time {{
    color: var(--text-subtle);
}}

.chat-bubble-bot {{
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 4px 16px 16px 16px;
    padding: 16px 20px;
    box-shadow: var(--shadow-card);
    font-size: 0.85rem;
    line-height: 1.6;
    color: var(--text-heading);
}}

/* Styled Table inside Bot Message */
.bot-table-container {{
    margin: 12px 0;
    overflow-x: auto;
    border: 1px solid #E2E8F0;
    border-radius: var(--radius-sm);
}}
.bot-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.8rem;
    text-align: left;
}}
.bot-table th {{
    background-color: #F8FAFC;
    color: var(--text-muted);
    font-weight: 700;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 9px 13px;
    border-bottom: 1px solid #E2E8F0;
}}
.bot-table td {{
    padding: 9px 13px;
    border-bottom: 1px solid #F1F5F9;
    color: var(--text-body);
}}
.bot-table tr:last-child td {{
    border-bottom: none;
}}
.pill-badge-green {{
    background-color: #ECFDF5;
    color: #059669;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: var(--radius-full);
    font-size: 0.74rem;
}}
.text-purple-bold {{
    color: #4F46E5;
    font-weight: 600;
}}

/* 3-Steps Box */
.steps-box {{
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: var(--radius-md);
    padding: 13px 15px;
    margin: 13px 0;
}}
.steps-box-title {{
    font-weight: 700;
    font-size: 0.82rem;
    color: var(--text-heading);
    margin-bottom: 7px;
    display: flex;
    align-items: center;
    gap: 6px;
}}
.steps-box-list {{
    margin: 0;
    padding-left: 17px;
    font-size: 0.8rem;
    color: var(--text-body);
    line-height: 1.6;
}}

/* Warning Notice Box */
.warning-box {{
    background-color: #FFFBEB;
    border: 1px solid #FDE68A;
    border-radius: var(--radius-md);
    padding: 11px 15px;
    margin: 13px 0;
    display: flex;
    align-items: flex-start;
    gap: 9px;
    font-size: 0.8rem;
    color: #92400E;
    line-height: 1.55;
}}

/* Bot Action Buttons */
.bot-actions-row {{
    display: flex;
    align-items: center;
    gap: 9px;
    margin-top: 15px;
    margin-bottom: 10px;
}}
.btn-bot-action-primary {{
    background-color: #4F46E5;
    color: #FFFFFF !important;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 7px 15px;
    border-radius: var(--radius-sm);
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    box-shadow: 0 2px 5px rgba(79, 70, 229, 0.2);
    transition: all 0.15s ease;
}}
.btn-bot-action-primary:hover {{
    background-color: #4338CA;
}}
.btn-bot-action-secondary {{
    background-color: #FFFFFF;
    color: var(--text-body) !important;
    border: 1px solid #E2E8F0;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 7px 15px;
    border-radius: var(--radius-sm);
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    transition: all 0.15s ease;
}}
.btn-bot-action-secondary:hover {{
    background-color: #F8FAFC;
}}

/* Two return cards in Message 2 */
.return-cards-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 11px;
    margin: 13px 0;
}}
.return-card {{
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: var(--radius-md);
    padding: 11px 13px;
}}
.return-card-title {{
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-heading);
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 5px;
}}
.return-card-desc {{
    font-size: 0.74rem;
    color: var(--text-muted);
    line-height: 1.45;
}}

/* Related Topics Section */
.related-topics-row {{
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 7px;
    margin-top: 13px;
    font-size: 0.74rem;
    color: var(--text-muted);
}}
.related-topic-tag {{
    background-color: #FFFFFF !important;
    color: #334155 !important;
    border: 1px solid #E2E8F0 !important;
    padding: 5px 12px !important;
    border-radius: var(--radius-full) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.15s ease !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 4px !important;
}}
.related-topic-tag:hover {{
    background-color: #EEF0FD !important;
    border-color: #C7D2FE !important;
    color: #5B50E6 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 3px 8px rgba(91, 80, 230, 0.12) !important;
}}

/* Message Feedback Bar */
.msg-feedback-bar {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 13px;
    padding-top: 11px;
    border-top: 1px solid #F1F5F9;
}}
.feedback-action-pill {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--text-subtle);
    cursor: pointer;
    padding: 2px 5px;
    border-radius: 4px;
    transition: color 0.15s;
}}
.feedback-action-pill:hover {{
    color: var(--primary-purple);
}}

/* ==============================================================================
   NATIVE STREAMLIT CHAT INPUT STYLING (FLOATING PILL AT BOTTOM)
   ============================================================================== */
[data-testid="stChatInput"] {{
    position: fixed !important;
    bottom: 22px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 100% !important;
    max-width: 780px !important;
    z-index: 999 !important;
    background: #FFFFFF !important;
    border-radius: var(--radius-full) !important;
    border: 1.5px solid #E2E8F0 !important;
    box-shadow: 0 6px 28px rgba(0, 0, 0, 0.08) !important;
    padding: 4px 6px 4px 16px !important;
    transition: all 0.2s ease !important;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: #5B50E6 !important;
    box-shadow: 0 8px 32px rgba(91, 80, 230, 0.16) !important;
}}
[data-testid="stChatInput"] textarea {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
    color: #1E293B !important;
}}
[data-testid="stChatInput"] button {{
    background-color: #4F46E5 !important;
    color: #FFFFFF !important;
    border-radius: 50% !important;
    border: none !important;
    box-shadow: 0 2px 6px rgba(79, 70, 229, 0.3) !important;
}}

.chat-input-disclaimer {{
    position: fixed;
    bottom: 4px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.68rem;
    color: var(--text-subtle);
    white-space: nowrap;
    z-index: 999;
    text-align: center;
}}

@media (max-width: 768px) {{
    .core-rules-grid {{
        grid-template-columns: 1fr 1fr;
    }}
    .return-cards-grid {{
        grid-template-columns: 1fr;
    }}
    .chat-bubble-user, .chat-content-bot {{
        max-width: 95%;
    }}
    [data-testid="stChatInput"] {{
        max-width: 90% !important;
    }}
}}

.doc-citation-badge {{
    background: #EEF0FD;
    color: #5B50E6;
    font-weight: 700;
    font-size: 11.5px;
    padding: 2px 7px;
    border-radius: 6px;
    margin: 0 3px;
    border: 1px solid rgba(91, 80, 230, 0.25);
    display: inline-block;
}}
</style>
"""

st.html(CUSTOM_CSS)


# ==============================================================================
# RAG PIPELINE INTEGRATION
# ==============================================================================
def generate_bot_response(query: str) -> str:
    """Gọi pipeline RAG thực tế từ src.task10_generation và sinh HTML hiển thị."""
    top_k = st.session_state.get("top_k", 5)
    try:
        result = generate_with_citation(query, top_k=top_k)
        answer = result.get("answer", "")
        sources = result.get("sources", [])
        method = result.get("retrieval_source", "hybrid")
    except Exception as e:
        answer = f"Đã xảy ra lỗi khi kết nối RAG Pipeline: {e}"
        sources = []
        method = "none"

    # Chuyển đổi trích dẫn markdown [Document X] thành badge nổi bật
    formatted_answer = html.escape(answer)
    formatted_answer = re.sub(
        r'\[(Document\s*\d+(?:,\s*Document\s*\d+)*)\]',
        r'<span class="doc-citation-badge">\1</span>',
        formatted_answer,
    )
    formatted_answer = formatted_answer.replace("\n\n", "<br><br>").replace("\n", "<br>")

    sources_html = ""
    if sources:
        sources_cards = []
        for idx, src in enumerate(sources, 1):
            meta = src.get("metadata", {})
            title = html.escape(str(meta.get("title", "Tài liệu")))
            source_file = html.escape(str(meta.get("source", "")))
            score = src.get("score", 0.0)
            src_method = src.get("retrieval_method", "dense")
            url = meta.get("url")
            url_link = (
                f'<a href="{url}" target="_blank" style="color: var(--primary-purple); text-decoration: underline;">🔗 Xem tài liệu gốc</a>'
                if url
                else f'<span style="color: var(--text-muted);">📄 {source_file}</span>'
            )
            raw_content = str(src.get("content", ""))
            content_snippet = html.escape(raw_content[:260]) + ("..." if len(raw_content) > 260 else "")

            sources_cards.append(f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 10px 14px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-weight: 700; color: #1E293B; font-size: 13px;">[{idx}] {title}</span>
                        <span style="font-size: 11px; background: #EEF0FD; color: #5B50E6; padding: 2px 8px; border-radius: 999px; font-weight: 600;">Score: {score:.3f} ({src_method})</span>
                    </div>
                    <div style="font-size: 12px; color: #475569; line-height: 1.5; margin-bottom: 6px; font-style: italic;">
                        "{content_snippet}"
                    </div>
                    <div style="font-size: 11px;">{url_link}</div>
                </div>
            """)

        sources_html = f"""
            <details style="margin-top: 14px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 10px 14px; cursor: pointer;">
                <summary style="font-weight: 700; color: #5B50E6; font-size: 13px; outline: none;">
                    📚 Xem {len(sources)} tài liệu nguồn tham khảo • Phương thức: <strong>{method.upper()}</strong>
                </summary>
                <div style="margin-top: 10px;">
                    {''.join(sources_cards)}
                </div>
            </details>
        """

    return f"""
        <div style="line-height: 1.6; font-size: 14.5px; color: var(--text-body);">
            {formatted_answer}
        </div>
        {sources_html}
        <div class="msg-feedback-bar" style="margin-top: 12px;">
            <span class="feedback-action-pill">📋 Sao chép</span>
            <span class="feedback-action-pill">👍 Hữu ích</span>
            <span class="feedback-action-pill">👎 Chưa rõ</span>
            <span class="feedback-action-pill">🔄 Tạo lại</span>
        </div>
    """


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
def init_session_state():
    if "view_mode" not in st.session_state:
        st.session_state["view_mode"] = "landing"

    if "top_k" not in st.session_state:
        st.session_state["top_k"] = 5

    if "messages" not in st.session_state:
        st.session_state["messages"] = []


def process_user_query(query: str):
    """Adds user query and bot response to chat history and switches to chat view."""
    now_str = datetime.now().strftime("%I:%M %p")
    st.session_state["messages"].append({
        "role": "user",
        "time": now_str,
        "user_name": "Nguyễn Văn An",
        "user_avatar": "NV",
        "content": query,
    })
    bot_reply = generate_bot_response(query)
    st.session_state["messages"].append({
        "role": "bot",
        "time": now_str,
        "content_html": bot_reply,
    })
    st.session_state["view_mode"] = "chat"


# ==============================================================================
# COMPONENT: SIDEBAR (LOCKED FLUSH AT BOTTOM)
# ==============================================================================
def render_sidebar():
    with st.sidebar:
        # 1. Header with Owl Bot Icon & Title
        st.html(
            f"""
            <div class="sidebar-header">
                <div class="sidebar-brand">
                    <img class="sidebar-brand-avatar" src="{OWL_ICON_URI}" alt="UniLib Bot" />
                    <div>
                        <div class="sidebar-brand-title">UniLib Bot</div>
                        <div class="sidebar-brand-subtitle">Trợ lý Thư viện</div>
                    </div>
                </div>
                <button class="sidebar-collapse-btn" title="Thu gọn sidebar">
                    <svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3" /><line x1="9" y1="3" x2="9" y2="21" /></svg>
                </button>
            </div>
            """
        )

        # 2. New Chat Button
        new_chat_clicked = st.button("➕ Đoạn chat mới", key="btn_new_chat", use_container_width=True)
        if new_chat_clicked:
            st.session_state["view_mode"] = "landing"
            st.rerun()

        # 3. Chat History: HÔM NAY
        history_active = "active" if st.session_state.get("view_mode") == "chat" else ""
        st.html(
            f"""
            <div class="sidebar-section-title">HÔM NAY</div>
            <a class="sidebar-history-item {history_active}" href="?view=chat" target="_self">
                <span class="sidebar-history-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg></span>
                <span>Quy định gia hạn mượn sá...</span>
            </a>
            <a class="sidebar-history-item" href="?q=open_hours" target="_self">
                <span class="sidebar-history-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg></span>
                <span>Giờ mở cửa phòng tự học đê...</span>
            </a>
            <a class="sidebar-history-item" href="?q=rfid_card" target="_self">
                <span class="sidebar-history-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg></span>
                <span>Cách đăng ký thẻ thư viện onli...</span>
            </a>
            """
        )

        # 4. Chat History: 7 NGÀY QUA
        st.html(
            """
            <div class="sidebar-section-title" style="margin-top: 14px;">7 NGÀY QUA</div>
            <a class="sidebar-history-item" href="#">
                <span class="sidebar-history-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg></span>
                <span>Mức phạt trễ hạn sách tham k...</span>
            </a>
            <a class="sidebar-history-item" href="#">
                <span class="sidebar-history-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg></span>
                <span>Mượn luận văn tốt nghiệp ngà...</span>
            </a>
            <a class="sidebar-history-item" href="#">
                <span class="sidebar-history-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg></span>
                <span>Tài khoản cơ sở dữ liệu Scopus...</span>
            </a>
            <a class="sidebar-history-item" href="#">
                <span class="sidebar-history-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg></span>
                <span>Đặt phòng học nhóm tầng 3</span>
            </a>
            """
        )

        # 5. User Profile Footer (Pinned to bottom)
        st.html(
            """
            <div class="sidebar-user-footer">
                <div class="user-info-wrapper">
                    <div class="user-avatar-badge-wrapper">
                        <div class="user-avatar-badge">NV</div>
                        <div class="user-online-indicator"></div>
                    </div>
                    <div>
                        <div class="user-name">Nguyễn Văn An</div>
                        <div class="user-id">MSSV: 2024001 • K24</div>
                    </div>
                </div>
                <button class="user-settings-btn" title="Cài đặt">
                    <svg viewBox="0 0 24 24" width="17" height="17" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="12" cy="12" r="3"></circle>
                        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                    </svg>
                </button>
            </div>
            """
        )



# ==============================================================================
# COMPONENT: TOP NAVIGATION BAR
# ==============================================================================
def render_top_nav():
    st.html(
        f"""
        <div class="top-nav-bar">
            <div class="top-nav-left">
                <span class="top-nav-brand">UniLib Bot</span>
                <span class="top-nav-tag">AI Trợ lý Quy định Thư viện</span>
                <span class="top-nav-status">
                    <span class="status-dot-pulse"></span>
                    Trực tuyến
                </span>
            </div>
        </div>
        """
    )


# ==============================================================================
# COMPONENT: SCREEN 1 — LANDING / EMPTY STATE
# ==============================================================================
def render_landing_screen():
    # Centered container for the main landing content
    col_l_sp, col_main_content, col_r_sp = st.columns([0.8, 8.4, 0.8])
    with col_main_content:
        st.html(
            f"""
            <div class="landing-wrapper">
                <!-- Hero Section (grouped, pushed up) -->
                <div class="landing-hero">
                    <!-- 3D Owl Bot Character with Badge -->
                    <div class="landing-avatar-card">
                        <img class="landing-avatar-img" src="{OWL_ICON_URI}" alt="UniLib Owl Bot" />
                        <div class="landing-avatar-tag">Hi sinh viên! &#128075;</div>
                    </div>

                    <!-- Hero Titles -->
                    <div class="landing-title">
                        UniLib Bot • <span class="landing-title-accent">Bạn Thân Chốn Thư Viện</span> &#129417;✨
                    </div>
                    <div class="landing-subtitle">
                        Hỏi tất tần tật quy định mượn sách, giờ mở cửa máy lạnh 24/7 và hạn gia hạn online nhé!
                    </div>
                </div>
            </div>
            """
        )

        # Centered Interactive Search Form on Landing
        with st.form("landing_chat_form", clear_on_submit=True, border=False):
            col_input, col_submit = st.columns([5.5, 1])
            with col_input:
                user_text = st.text_input(
                    "Hỏi bot",
                    placeholder="Hỏi quy định mượn trả, giờ mở cửa, cách gia hạn sách online... (Nhấn Enter)",
                    label_visibility="collapsed",
                    key="landing_input_field",
                )
            with col_submit:
                submit_clicked = st.form_submit_button("Gửi ➔", use_container_width=True)

            if submit_clicked and user_text.strip():
                process_user_query(user_text.strip())
                st.rerun()

        # Interactive Suggestion Chips (2 Balanced Rows without truncation)
        row1_c1, row1_c2, row1_c3 = st.columns([1, 1.1, 1.1])
        with row1_c1:
            if st.button("⚡ Gia hạn sách online 30s", key="chip_renew", use_container_width=True):
                process_user_query("Làm thế nào để gia hạn sách online?")
                st.rerun()
        with row1_c2:
            if st.button("❄️ Phòng tự học 24/7 mùa thi", key="chip_room", use_container_width=True):
                process_user_query("Giờ mở cửa phòng tự học 24/7 máy lạnh mùa thi")
                st.rerun()
        with row1_c3:
            if st.button("⚠️ Phạt trễ hạn & khóa thẻ", key="chip_fine", use_container_width=True):
                process_user_query("Mức phạt trễ hạn sách và quy định khóa thẻ")
                st.rerun()

        row2_sp1, row2_c4, row2_c5, row2_sp2 = st.columns([0.4, 1.1, 0.9, 0.4])
        with row2_c4:
            if st.button("🪪 Kích hoạt thẻ Tân sinh viên", key="chip_card", use_container_width=True):
                process_user_query("Cách kích hoạt thẻ RFID tân sinh viên")
                st.rerun()
        with row2_c5:
            if st.button("🔄 Đổi gợi ý khác", key="chip_refresh", use_container_width=True):
                st.rerun()

        # Core Rules Grid
        st.html(
            """
            <div class="core-rules-section">
                <div class="core-rules-header">
                    <span class="core-rules-title">QUY ĐỊNH CỐT LÕI SINH VIÊN CẦN NẮM</span>
                    <span class="core-rules-badge">Học kỳ 2 • 2024 - 2025</span>
                </div>
                <div class="core-rules-grid">
                    <!-- Card 1 -->
                    <div class="rule-card">
                        <div class="rule-card-icon blue">📘</div>
                        <div>
                            <div class="rule-card-label">Mượn sách</div>
                            <div class="rule-card-value">05 cuốn / lần</div>
                            <div class="rule-card-sub">Gia hạn 2 lần</div>
                        </div>
                    </div>
                    <!-- Card 2 -->
                    <div class="rule-card">
                        <div class="rule-card-icon green">🪪</div>
                        <div>
                            <div class="rule-card-label">Thẻ bạn đọc</div>
                            <div class="rule-card-value">Tích hợp thẻ SV</div>
                            <div class="rule-card-sub">Quản lý qua RFID</div>
                        </div>
                    </div>
                    <!-- Card 3 -->
                    <div class="rule-card">
                        <div class="rule-card-icon orange">⏰</div>
                        <div>
                            <div class="rule-card-label">Giờ mở cửa</div>
                            <div class="rule-card-value">07:30 – 21:00</div>
                            <div class="rule-card-sub">Tầng trệt 24/7</div>
                        </div>
                    </div>
                    <!-- Card 4 -->
                    <div class="rule-card">
                        <div class="rule-card-icon red">⚠️</div>
                        <div>
                            <div class="rule-card-label">Phạt trễ hạn</div>
                            <div class="rule-card-value">3.000 đ / ngày</div>
                            <div class="rule-card-sub">Khóa thẻ > 30 ngày</div>
                        </div>
                    </div>
                </div>
            </div>
            """
        )


# ==============================================================================
# COMPONENT: SCREEN 2 — ACTIVE CHAT SCREEN (INTERACTIVE)
# ==============================================================================
def render_chat_screen():
    col_l_sp, col_main_chat, col_r_sp = st.columns([0.8, 8.4, 0.8])
    with col_main_chat:
        messages_html = ['<div class="chat-container">', '<div class="chat-date-divider"><span class="chat-date-badge">HÔM NAY</span></div>']

        for msg in st.session_state.get("messages", []):
            if msg["role"] == "user":
                messages_html.append(f"""
                    <div class="chat-row-user">
                        <div class="chat-meta-user">
                            <span>{msg.get('time', 'Vừa xong')} {msg.get('user_name', 'Sinh viên')}</span>
                            <span class="user-avatar-mini">{msg.get('user_avatar', 'SV')}</span>
                        </div>
                        <div class="chat-bubble-user">
                            {msg.get('content', '')}
                        </div>
                    </div>
                """)
            else:
                messages_html.append(f"""
                    <div class="chat-row-bot">
                        <img class="bot-avatar-img" src="{OWL_ICON_URI}" alt="UniLib Bot" />
                        <div class="chat-content-bot">
                            <div class="chat-meta-bot">
                                <span class="chat-meta-bot-name">UniLib Bot</span>
                                <span class="chat-meta-bot-tag">AI Trợ lý Thư viện</span>
                                <span class="chat-meta-bot-time">{msg.get('time', 'Vừa xong')}</span>
                            </div>
                            <div class="chat-bubble-bot">
                                {msg.get('content_html', '')}
                            </div>
                        </div>
                    </div>
                """)

        messages_html.append('</div>')
        st.html("".join(messages_html))

    # Native interactive chat input (Floating pill at bottom)
    if prompt := st.chat_input("Nhập thắc mắc về mượn trả, quy định, số ngày gia hạn... (Nhấn Enter)"):
        process_user_query(prompt)
        st.rerun()

    # Sticky disclaimer underneath
    st.html(
        """
        <div class="chat-input-disclaimer">
            UniLib Bot đồng hành cùng sinh viên • Dữ liệu trích xuất chính thức từ Sổ tay Quy chế Thư viện 2024–2025
        </div>
        """
    )


# ==============================================================================
# MAIN PAGE CONTROLLER
# ==============================================================================
def main():
    init_session_state()

    # Query params routing
    query_params = st.query_params
    if "view" in query_params:
        st.session_state["view_mode"] = query_params["view"]
    elif "q" in query_params:
        q_key = query_params["q"]
        if q_key == "open_hours":
            process_user_query("Giờ mở cửa phòng tự học 24/7 máy lạnh mùa thi")
        elif q_key == "rfid_card":
            process_user_query("Cách đăng ký và sử dụng thẻ thư viện RFID")

    # 1. Render Left Sidebar
    render_sidebar()

    # 2. Render Top Navigation Bar
    render_top_nav()

    # 3. Render Selected Screen
    if st.session_state["view_mode"] == "landing":
        render_landing_screen()
    else:
        render_chat_screen()


if __name__ == "__main__":
    main()
