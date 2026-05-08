import streamlit as st
import pickle
import json
import os
import csv
import urllib.parse
from datetime import datetime

import pandas as pd

try:
    from streamlit_js_eval import get_geolocation
except ImportError:
    get_geolocation = None


# =========================================================
# FILE PATHS
# =========================================================

MODEL_FILE = "threat_model.pkl"
CONTACTS_FILE = "contacts.json"
LOG_FILE = "incident_logs.csv"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NariSuraksha AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap');

html, body, .stApp, .block-container {
    font-family: 'Manrope', sans-serif !important;
}

p, h1, h2, h3, h4, h5, h6, label, input, textarea {
    font-family: 'Manrope', sans-serif !important;
}

/* Restore Streamlit / Material icon fonts */
.material-symbols-outlined,
.material-symbols-rounded,
.material-icons,
[class*="material-symbols"],
[data-testid="collapsedControl"] span,
button[kind="header"] span,
[data-testid="stIconMaterial"] {
    font-family: "Material Symbols Rounded", "Material Symbols Outlined", "Material Icons" !important;
    font-weight: normal !important;
    font-style: normal !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    direction: ltr !important;
    -webkit-font-smoothing: antialiased !important;
}

.stApp {
    background:
        radial-gradient(circle at 10% 5%, rgba(225, 29, 72, 0.09), transparent 28%),
        radial-gradient(circle at 90% 8%, rgba(59, 130, 246, 0.08), transparent 25%),
        #f4f6fa;
    color: #111827;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: visible !important;
    background: transparent !important;
    box-shadow: none !important;
}

/* Sidebar open/close arrow */
[data-testid="collapsedControl"] {
    background: #e11d48 !important;
    color: white !important;
    border-radius: 999px !important;
    padding: 8px !important;
    box-shadow: 0 10px 25px rgba(225, 29, 72, 0.35) !important;
}

[data-testid="collapsedControl"] svg {
    color: white !important;
    fill: white !important;
}

button[kind="header"] {
    background: #e11d48 !important;
    color: white !important;
    border-radius: 999px !important;
    width: 38px !important;
    height: 38px !important;
    box-shadow: 0 10px 25px rgba(225, 29, 72, 0.35) !important;
}

button[kind="header"] svg {
    color: white !important;
    fill: white !important;
}

/* Fix black iframe issue from geolocation component */
iframe {
    min-height: 0px !important;
    height: 0px !important;
    border: 0 !important;
}

/* Main container */
.block-container {
    max-width: 1180px;
    padding-top: 2.3rem;
    padding-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f172a;
    border-right: 1px solid #1e293b;
}

section[data-testid="stSidebar"] * {
    color: #e5e7eb;
}

section[data-testid="stSidebar"] input {
    background: #111827 !important;
    color: #ffffff !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

section[data-testid="stSidebar"] input::placeholder {
    color: #64748b !important;
}

section[data-testid="stSidebar"] .stButton > button {
    background: #e11d48 !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    font-weight: 800 !important;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 850;
    color: #ffffff;
    margin-bottom: 6px;
}

.sidebar-subtitle {
    font-size: 13px;
    color: #94a3b8 !important;
    line-height: 1.55;
    margin-bottom: 18px;
}

.sidebar-section {
    font-size: 12px;
    font-weight: 800;
    color: #fb7185 !important;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    margin-top: 20px;
    margin-bottom: 8px;
}

.sidebar-contact {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
}

.sidebar-contact strong {
    color: #ffffff !important;
}

.sidebar-contact span {
    color: #94a3b8 !important;
    font-size: 13px;
}

.sidebar-call {
    display: block;
    text-decoration: none !important;
    background: #dc2626;
    color: white !important;
    padding: 12px 14px;
    border-radius: 12px;
    font-weight: 800;
    margin-bottom: 10px;
    text-align: center;
}

.sidebar-call-pink {
    display: block;
    text-decoration: none !important;
    background: #be123c;
    color: white !important;
    padding: 12px 14px;
    border-radius: 12px;
    font-weight: 800;
    margin-bottom: 10px;
    text-align: center;
}

/* Hero */
.hero {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 28px;
    padding: 30px;
    box-shadow: 0 20px 48px rgba(15, 23, 42, 0.06);
    margin-bottom: 22px;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #fff1f2;
    color: #be123c;
    border: 1px solid #fecdd3;
    padding: 7px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 850;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    font-family: 'IBM Plex Mono', monospace !important;
    margin-bottom: 14px;
}

.hero-title {
    font-size: 42px;
    font-weight: 850;
    color: #0f172a;
    letter-spacing: -1.2px;
    line-height: 1.08;
    margin-bottom: 10px;
}

.hero-title span {
    color: #e11d48;
}

.hero-desc {
    max-width: 850px;
    color: #64748b;
    line-height: 1.7;
    font-size: 15.5px;
}

/* Text */
.card-label {
    color: #e11d48;
    font-size: 12px;
    font-weight: 850;
    letter-spacing: 0.75px;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace !important;
    margin-bottom: 8px;
}

.card-title {
    color: #111827;
    font-size: 22px;
    font-weight: 850;
    letter-spacing: -0.4px;
    margin-bottom: 8px;
}

.card-desc {
    color: #64748b;
    font-size: 14px;
    line-height: 1.65;
    margin-bottom: 18px;
}

.small-note {
    color: #64748b;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 12px;
}

/* Streamlit bordered container */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff;
    border: 1px solid #e5e7eb !important;
    border-radius: 24px !important;
    box-shadow: 0 16px 38px rgba(15, 23, 42, 0.055);
}

/* Stats */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 22px;
}

.stat-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 14px 34px rgba(15, 23, 42, 0.055);
}

.stat-label {
    color: #64748b;
    font-size: 12px;
    font-weight: 850;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace !important;
}

.stat-value {
    color: #111827;
    font-size: 25px;
    font-weight: 850;
    margin-top: 10px;
}

/* Result boxes */
.result-safe {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #047857;
    padding: 18px;
    border-radius: 18px;
    font-size: 20px;
    font-weight: 850;
    text-align: center;
    margin-top: 16px;
}

.result-warning {
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #b45309;
    padding: 18px;
    border-radius: 18px;
    font-size: 20px;
    font-weight: 850;
    text-align: center;
    margin-top: 16px;
}

.result-danger {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #b91c1c;
    padding: 18px;
    border-radius: 18px;
    font-size: 20px;
    font-weight: 850;
    text-align: center;
    margin-top: 16px;
}

/* Metrics */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 16px;
}

.metric-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 15px;
    text-align: center;
}

.metric-label {
    color: #64748b;
    font-size: 12px;
    font-weight: 850;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace !important;
}

.metric-value {
    color: #111827;
    font-size: 18px;
    font-weight: 850;
    margin-top: 6px;
}

.recommendation {
    background: #f8fafc;
    border-left: 5px solid #e11d48;
    border-radius: 16px;
    padding: 15px;
    color: #334155;
    line-height: 1.7;
    margin-top: 16px;
}

/* SOS */
.sos-wrapper {
    background: #fff7f8;
    border: 1px solid #fecdd3;
    border-radius: 26px;
    padding: 24px;
    box-shadow: 0 18px 44px rgba(225, 29, 72, 0.08);
    margin-bottom: 18px;
}

.step-badge {
    width: 34px;
    height: 34px;
    background: #e11d48;
    color: white;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 850;
    margin-bottom: 12px;
}

.location-success {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #065f46;
    padding: 13px;
    border-radius: 15px;
    line-height: 1.6;
    font-size: 13.5px;
    margin-top: 12px;
    word-break: break-word;
}

.location-error {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
    padding: 13px;
    border-radius: 15px;
    line-height: 1.6;
    font-size: 13.5px;
    margin-top: 12px;
}

.message-box {
    background: #f8fafc;
    border: 1px dashed #94a3b8;
    color: #334155;
    padding: 14px;
    border-radius: 15px;
    line-height: 1.7;
    font-size: 13.5px;
    margin-top: 12px;
    word-break: break-word;
}

/* Link buttons */
.link-btn {
    display: inline-block;
    text-decoration: none !important;
    color: white !important;
    padding: 12px 15px;
    border-radius: 13px;
    font-weight: 850;
    margin: 8px 8px 0 0;
    box-shadow: 0 10px 22px rgba(15, 23, 42, 0.14);
}

.whatsapp {
    background: #16a34a;
}

.call {
    background: #dc2626;
}

.women {
    background: #be123c;
}

.priority-call {
    background: #7c3aed;
}

/* Streamlit widgets */
.stButton > button {
    border-radius: 13px !important;
    border: none !important;
    background: #e11d48 !important;
    color: white !important;
    font-weight: 850 !important;
    padding: 0.72rem 1rem !important;
    box-shadow: 0 10px 22px rgba(225, 29, 72, 0.16) !important;
}

.stTextInput input,
.stTextArea textarea {
    background: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #dbe3ef !important;
    border-radius: 13px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #e11d48 !important;
    box-shadow: 0 0 0 2px rgba(225, 29, 72, 0.12) !important;
}

.stAlert {
    border-radius: 14px !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background: #ffffff;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    padding: 10px 16px;
    font-weight: 800;
}

.stTabs [aria-selected="true"] {
    background: #e11d48 !important;
    color: white !important;
}

/* Responsive */
@media (max-width: 950px) {
    .stat-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .metric-grid {
        grid-template-columns: 1fr;
    }

    .hero-title {
        font-size: 32px;
    }
}

@media (max-width: 620px) {
    .stat-grid {
        grid-template-columns: 1fr;
    }

    .hero {
        padding: 22px;
    }

    .link-btn {
        display: block;
        width: 100%;
        text-align: center;
        margin-right: 0;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCTIONS
# =========================================================

@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_FILE):
        st.error("Model file not found. Please run: python train_model.py")
        st.stop()

    with open(MODEL_FILE, "rb") as file:
        return pickle.load(file)


def load_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []

    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def save_contacts(contacts):
    with open(CONTACTS_FILE, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


def create_whatsapp_link(number, message):
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{number}?text={encoded_message}"


def clean_phone_number(number):
    return "".join(ch for ch in str(number) if ch.isdigit())


def get_prediction_details(model, text):
    message = text.lower()

    danger_keywords = [
        "help me", "urgent help", "sos", "danger", "save me",
        "following me", "chasing", "grabbed", "threatening",
        "not safe", "harassed", "force", "forced", "trapped",
        "bachao", "peecha", "danger me", "darr lag raha",
        "help bhejo", "haath pakad", "zabardasti", "phas gayi"
    ]

    warning_keywords = [
        "uncomfortable", "staring", "watching", "unsafe feel",
        "alone", "empty road", "dark", "stranger",
        "route change", "driver changed", "following from distance",
        "comfortable nahi", "akeli", "dekh raha", "route change"
    ]

    prediction = model.predict([text])[0]

    confidence = 0
    try:
        if hasattr(model.named_steps["classifier"], "predict_proba"):
            probabilities = model.predict_proba([text])[0]
            confidence = round(max(probabilities) * 100, 2)
    except Exception:
        confidence = 0

    if any(keyword in message for keyword in danger_keywords):
        prediction = "danger"
        confidence = max(confidence, 92)

    elif any(keyword in message for keyword in warning_keywords) and prediction == "safe":
        prediction = "warning"
        confidence = max(confidence, 78)

    return prediction, confidence


def detect_threat_type(message):
    msg = message.lower()

    if any(word in msg for word in ["follow", "following", "chasing", "behind", "peecha"]):
        return "Stalking Risk"

    if any(word in msg for word in ["cab", "driver", "route", "vehicle", "auto"]):
        return "Travel Risk"

    if any(word in msg for word in ["harass", "troubling", "staring", "forcing", "grab"]):
        return "Harassment Risk"

    if any(word in msg for word in ["alone", "empty", "dark", "isolated", "unknown", "akeli"]):
        return "Isolation Risk"

    if any(word in msg for word in ["help", "danger", "threatened", "unsafe", "scared", "bachao"]):
        return "Emergency Distress"

    return "General Safety Check"


def get_recommendation(prediction):
    if prediction == "safe":
        return "Situation looks safe. Stay aware, keep your phone reachable, and continue normally."

    if prediction == "warning":
        return "Medium risk detected. Move towards a public or well-lit place and inform your trusted contacts."

    return "High risk detected. Generate location link, send SOS to all priority contacts, and use call options if needed."


def get_location_link(location_data):
    if not location_data or "error" in location_data:
        return None

    coords = location_data.get("coords", {})
    lat = coords.get("latitude")
    lon = coords.get("longitude")

    if lat is None or lon is None:
        return None

    return f"https://www.google.com/maps?q={lat},{lon}"


def get_location_error_message(location_data):
    if not location_data or "error" not in location_data:
        return "Location unavailable. Please try again."

    error = location_data.get("error", {})
    code = error.get("code")
    message = error.get("message", "Location unavailable")

    if code == 1:
        return "Location permission is blocked. Click the site icon near the address bar, allow Location, reload the page, and try again."

    if code == 2:
        return "Location unavailable. Turn ON Windows Location Services and allow browser location access."

    if code == 3:
        return "Location request timed out. Please click the location button again."

    return f"Location error: {message}"


def save_incident(message, prediction, threat_type, confidence, location_link, sos_status):
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "date_time",
                "message",
                "risk_level",
                "threat_type",
                "confidence",
                "location_link",
                "sos_status"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            message,
            prediction,
            threat_type,
            confidence,
            location_link if location_link else "Not Available",
            sos_status
        ])


def render_result(prediction):
    if prediction == "safe":
        st.markdown("<div class='result-safe'>✅ LOW RISK · Safe Situation Detected</div>", unsafe_allow_html=True)
    elif prediction == "warning":
        st.markdown("<div class='result-warning'>⚠️ MEDIUM RISK · Warning Situation Detected</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='result-danger'>🚨 HIGH RISK · Danger Situation Detected</div>", unsafe_allow_html=True)


def render_stats():
    contacts_count = len(st.session_state.contacts)
    sos_status = "Ready" if contacts_count > 0 else "Add Contact"

    st.markdown(
        f"""
        <div class="stat-grid">
            <div class="stat-card">
                <div class="stat-label">Model</div>
                <div class="stat-value">Active</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Contacts</div>
                <div class="stat-value">{contacts_count}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Last Risk</div>
                <div class="stat-value">{st.session_state.last_prediction.upper()}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">SOS Mode</div>
                <div class="stat-value">{sos_status}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metrics(prediction, threat_type, confidence):
    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Risk Level</div>
                <div class="metric-value">{prediction.upper()}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Threat Type</div>
                <div class="metric-value">{threat_type}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Confidence</div>
                <div class="metric-value">{confidence}%</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SESSION STATE
# =========================================================

model = load_model()

if "contacts" not in st.session_state:
    st.session_state.contacts = load_contacts()

if "last_danger_message" not in st.session_state:
    st.session_state.last_danger_message = ""

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = "Not Checked"

if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = 0

if "last_threat_type" not in st.session_state:
    st.session_state.last_threat_type = "None"

if "last_location_link" not in st.session_state:
    st.session_state.last_location_link = None

if "location_requested" not in st.session_state:
    st.session_state.location_requested = False

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "last_logged_message" not in st.session_state:
    st.session_state.last_logged_message = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("<div class='sidebar-title'>NariSuraksha AI</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sidebar-subtitle'>Priority contacts and emergency actions for the SOS workflow. Use the top-left arrow to open or close this panel.</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='sidebar-section'>Priority Contact</div>", unsafe_allow_html=True)

    contact_name = st.text_input("Contact Name", placeholder="Example: Sana")
    contact_number = st.text_input("WhatsApp Number", placeholder="Example: 919876543210")

    if st.button("Add Contact", use_container_width=True):
        cleaned_number = clean_phone_number(contact_number)

        if contact_name.strip() == "" or cleaned_number == "":
            st.warning("Enter both name and number.")
        elif not cleaned_number.isdigit():
            st.warning("Use digits only. Example: 919876543210")
        elif len(cleaned_number) < 10:
            st.warning("Number is too short. Add country code also. Example: 919876543210")
        else:
            st.session_state.contacts.append({
                "name": contact_name.strip(),
                "number": cleaned_number
            })
            save_contacts(st.session_state.contacts)
            st.success("Contact added.")
            st.rerun()

    if st.session_state.contacts:
        st.markdown("<div class='sidebar-section'>Saved Contacts</div>", unsafe_allow_html=True)

        for index, contact in enumerate(st.session_state.contacts):
            st.markdown(
                f"""
                <div class="sidebar-contact">
                    <strong>Priority {index + 1}: {contact["name"]}</strong><br>
                    <span>{contact["number"]}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("Clear Contacts", use_container_width=True):
            st.session_state.contacts = []
            save_contacts([])
            st.success("Contacts cleared.")
            st.rerun()

    st.markdown("<div class='sidebar-section'>Emergency Calls</div>", unsafe_allow_html=True)
    st.markdown("<a class='sidebar-call' href='tel:112'>📞 Call 112 Emergency</a>", unsafe_allow_html=True)
    st.markdown("<a class='sidebar-call-pink' href='tel:181'>📞 Call 181 Women Helpline</a>", unsafe_allow_html=True)

    if st.session_state.contacts:
        st.markdown("<div class='sidebar-section'>Call Saved Contacts</div>", unsafe_allow_html=True)
        for contact in st.session_state.contacts:
            st.markdown(
                f"<a class='sidebar-call-pink' href='tel:{contact['number']}'>📞 Call {contact['name']}</a>",
                unsafe_allow_html=True
            )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">AI/ML · NLP Threat Detection</div>
        <div class="hero-title">NariSuraksha <span>AI</span></div>
        <div class="hero-desc">
            A professional women safety system that analyzes text messages, detects safety risks,
            prepares location-aware WhatsApp SOS alerts for all priority contacts, and provides one-tap emergency call actions.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

render_stats()


# =========================================================
# TABS
# =========================================================

tab_analyze, tab_sos, tab_logs = st.tabs([
    "Threat Detection",
    "SOS Response",
    "Incident History"
])


# =========================================================
# TAB 1: THREAT DETECTION
# =========================================================

with tab_analyze:
    with st.container(border=True):
        st.markdown("<div class='card-label'>Threat Intelligence</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>AI Safety Message Analysis</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='card-desc'>Enter a situation message. The ML model classifies it as safe, warning, or danger.</div>",
            unsafe_allow_html=True
        )

        user_message = st.text_area(
            "Safety Message",
            placeholder="Example: Someone is following me and I feel unsafe...",
            height=160
        )

        analyze_clicked = st.button("Analyze Safety Message", use_container_width=True)

        if analyze_clicked:
            if user_message.strip() == "":
                st.warning("Please enter a message first.")
            else:
                prediction, confidence = get_prediction_details(model, user_message)
                threat_type = detect_threat_type(user_message)

                st.session_state.analysis_done = True
                st.session_state.last_prediction = prediction
                st.session_state.last_confidence = confidence
                st.session_state.last_threat_type = threat_type

                if prediction == "danger":
                    st.session_state.last_danger_message = user_message
                    st.session_state.location_requested = False
                    st.session_state.last_location_link = None
                else:
                    st.session_state.last_danger_message = ""
                    st.session_state.location_requested = False
                    st.session_state.last_location_link = None

                log_key = f"{user_message.strip()}-{prediction}-{datetime.now().strftime('%Y-%m-%d %H:%M')}"

                if st.session_state.last_logged_message != log_key:
                    save_incident(
                        message=user_message,
                        prediction=prediction,
                        threat_type=threat_type,
                        confidence=confidence,
                        location_link="Pending Permission" if prediction == "danger" else "Not Required",
                        sos_status="Danger Detected" if prediction == "danger" else "No SOS Required"
                    )
                    st.session_state.last_logged_message = log_key

        if st.session_state.analysis_done:
            prediction = st.session_state.last_prediction
            confidence = st.session_state.last_confidence
            threat_type = st.session_state.last_threat_type
            recommendation = get_recommendation(prediction)

            render_result(prediction)
            render_metrics(prediction, threat_type, confidence)

            st.markdown(
                f"""
                <div class="recommendation">
                    <b>Recommended Action:</b><br>
                    {recommendation}
                </div>
                """,
                unsafe_allow_html=True
            )

            if prediction == "danger":
                st.error("High risk detected. Open the SOS Response tab to generate location and send alert to all contacts.")


# =========================================================
# TAB 2: SOS RESPONSE
# =========================================================

with tab_sos:
    if not st.session_state.last_danger_message:
        with st.container(border=True):
            st.markdown("<div class='card-label'>Emergency Response</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>SOS Workflow Not Active</div>", unsafe_allow_html=True)
            st.markdown(
                "<div class='card-desc'>The SOS workflow activates automatically after the AI model detects a danger message. Go to Threat Detection and analyze a high-risk message first.</div>",
                unsafe_allow_html=True
            )

            st.info("Example test message: Someone is following me and I feel unsafe")

    else:
        st.markdown(
            """
            <div class="sos-wrapper">
                <div class="card-label">Emergency Escalation Module</div>
                <div class="card-title">Location-Aware SOS Response</div>
                <div class="card-desc">
                    Generate your recent location, prepare WhatsApp SOS alerts for all priority contacts,
                    and use one-tap emergency call actions when required.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        step1, step2, step3 = st.columns([0.32, 0.42, 0.26], gap="medium")

        with step1:
            with st.container(border=True):
                st.markdown("<div class='step-badge'>1</div>", unsafe_allow_html=True)
                st.markdown("<div class='card-title'>Get Location</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='card-desc'>Click the button and allow browser location permission.</div>",
                    unsafe_allow_html=True
                )

                if get_geolocation is None:
                    st.error("streamlit-js-eval is not installed. Run: pip install streamlit-js-eval")
                else:
                    if st.button("📍 Get Current Location", use_container_width=True):
                        st.session_state.location_requested = True

                    if st.session_state.location_requested:
                        location_data = get_geolocation()

                        if location_data:
                            if "error" in location_data:
                                st.session_state.last_location_link = None
                                error_text = get_location_error_message(location_data)

                                st.markdown(
                                    f"""
                                    <div class="location-error">
                                        <b>Location Error</b><br>
                                        {error_text}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            else:
                                location_link = get_location_link(location_data)
                                st.session_state.last_location_link = location_link

                                if location_link:
                                    st.markdown(
                                        f"""
                                        <div class="location-success">
                                            <b>Location link generated.</b><br>
                                            {location_link}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                                else:
                                    st.warning("Location received, but coordinates were unavailable.")
                        else:
                            st.info("Waiting for browser permission...")

                st.markdown(
                    "<div class='small-note'>If blocked: browser site icon → Location → Allow → Reload.</div>",
                    unsafe_allow_html=True
                )

        with step2:
            with st.container(border=True):
                st.markdown("<div class='step-badge'>2</div>", unsafe_allow_html=True)
                st.markdown("<div class='card-title'>WhatsApp SOS to All Contacts</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='card-desc'>Each saved contact gets their own WhatsApp SOS button. Click each button to send the alert.</div>",
                    unsafe_allow_html=True
                )

                location_link = st.session_state.last_location_link

                if st.session_state.contacts:
                    if location_link:
                        sos_message = (
                            "SOS Alert! High risk situation detected. "
                            "Please contact me immediately. "
                            f"My recent location: {location_link}"
                        )
                        sos_status = f"SOS Prepared With Location for {len(st.session_state.contacts)} contacts"
                    else:
                        sos_message = (
                            "SOS Alert! High risk situation detected. "
                            "Please contact me immediately. "
                            "Location is not available yet."
                        )
                        sos_status = f"SOS Prepared Without Location for {len(st.session_state.contacts)} contacts"

                    st.success(f"{len(st.session_state.contacts)} priority contact(s) ready for SOS alert.")

                    st.markdown(
                        f"""
                        <div class="message-box">
                            <b>Auto-filled WhatsApp Message:</b><br>
                            {sos_message}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    for index, contact in enumerate(st.session_state.contacts):
                        whatsapp_link = create_whatsapp_link(contact["number"], sos_message)

                        st.markdown(
                            f"""
                            <a class="link-btn whatsapp" href="{whatsapp_link}" target="_blank">
                                💬 Send SOS to {contact["name"]}
                            </a>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        "<div class='small-note'>WhatsApp does not allow a normal web app to auto-send to everyone at once. For safety and privacy, you must click each contact button once.</div>",
                        unsafe_allow_html=True
                    )

                    if st.button("Save All SOS Status to Logs", use_container_width=True):
                        save_incident(
                            message=st.session_state.last_danger_message,
                            prediction="danger",
                            threat_type=detect_threat_type(st.session_state.last_danger_message),
                            confidence=st.session_state.last_confidence,
                            location_link=location_link if location_link else "Not Available",
                            sos_status=sos_status
                        )
                        st.success("All SOS status saved in incident logs.")
                else:
                    st.warning("Add at least one priority contact from the sidebar.")

        with step3:
            with st.container(border=True):
                st.markdown("<div class='step-badge'>3</div>", unsafe_allow_html=True)
                st.markdown("<div class='card-title'>Emergency Calls</div>", unsafe_allow_html=True)
                st.markdown(
                    "<div class='card-desc'>These buttons open the phone dialer. On laptop, they work only if a calling app is configured.</div>",
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <a class="link-btn call" href="tel:112">📞 Call 112</a>
                    <a class="link-btn women" href="tel:181">📞 Call 181</a>
                    """,
                    unsafe_allow_html=True
                )

                if st.session_state.contacts:
                    st.markdown("<div class='small-note'><b>Call saved contacts:</b></div>", unsafe_allow_html=True)

                    for contact in st.session_state.contacts:
                        st.markdown(
                            f"""
                            <a class="link-btn priority-call" href="tel:{contact["number"]}">
                                📞 Call {contact["name"]}
                            </a>
                            """,
                            unsafe_allow_html=True
                        )

                st.markdown(
                    "<div class='small-note'>If call buttons do not work on laptop, test on mobile browser or configure Windows Phone Link/Skype/default calling app.</div>",
                    unsafe_allow_html=True
                )

                if st.button("Reset SOS Workflow", use_container_width=True):
                    st.session_state.last_danger_message = ""
                    st.session_state.last_location_link = None
                    st.session_state.location_requested = False
                    st.session_state.analysis_done = False
                    st.session_state.last_prediction = "Not Checked"
                    st.session_state.last_confidence = 0
                    st.session_state.last_threat_type = "None"
                    st.rerun()


# =========================================================
# TAB 3: INCIDENT HISTORY
# =========================================================

with tab_logs:
    with st.container(border=True):
        st.markdown("<div class='card-label'>System Records</div>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>Incident History</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='card-desc'>Recent safety analysis and SOS workflow records are stored locally in incident_logs.csv.</div>",
            unsafe_allow_html=True
        )

        clear_col, note_col = st.columns([0.22, 0.78])

        with clear_col:
            if st.button("Clear History", use_container_width=True):
                if os.path.exists(LOG_FILE):
                    os.remove(LOG_FILE)
                st.success("Incident history cleared.")
                st.rerun()

        with note_col:
            st.markdown(
                "<div class='small-note'>Use this table during your project demo to show AI predictions and SOS activity.</div>",
                unsafe_allow_html=True
            )

        if os.path.exists(LOG_FILE):
            try:
                logs = pd.read_csv(LOG_FILE)

                if logs.empty:
                    st.info("No incident logs yet.")
                else:
                    st.dataframe(logs.tail(10), use_container_width=True)

            except Exception:
                st.warning("Unable to read incident logs.")
        else:
            st.info("No incident logs created yet.")


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="small-note">
        Academic project note: NariSuraksha AI prepares SOS alerts and opens WhatsApp/call actions for user confirmation.
        It does not automatically call emergency services.
    </div>
    """,
    unsafe_allow_html=True
)