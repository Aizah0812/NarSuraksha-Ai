import streamlit as st
import streamlit.components.v1 as components
import pickle
import json
import os
import csv
import urllib.parse
from datetime import datetime
import pandas as pd
import html

try:
    from streamlit_js_eval import get_geolocation
except ImportError:
    get_geolocation = None

# =========================================================
# APP CONFIG
# =========================================================
MODEL_FILE = "threat_model.pkl"
CONTACTS_FILE = "contacts.json"
LOG_FILE = "incident_logs.csv"

st.set_page_config(
    page_title="NariSuraksha | Women Safety System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PREMIUM DARK UI
# =========================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

:root{
  --bg:#05070c;
  --panel:#0c111b;
  --card:#111827;
  --card2:#151c2b;
  --line:#283244;
  --text:#f4f7fb;
  --muted:#a3adbf;
  --soft:#cbd5e1;
  --accent:#ff5c00;
  --pink:#ff2e63;
  --green:#22c55e;
  --red:#ef4444;
  --blue:#60a5fa;
}

.stApp{
  background:
    radial-gradient(circle at top left, rgba(255,92,0,.15), transparent 32%),
    radial-gradient(circle at top right, rgba(96,165,250,.12), transparent 32%),
    linear-gradient(135deg,#05070c 0%,#080d15 48%,#020305 100%);
  color:var(--text);
  font-family:'Plus Jakarta Sans',sans-serif;
}

.block-container{
  padding-top:2rem;
  padding-bottom:3rem;
  max-width:1340px;
}

h1,h2,h3,h4{
  color:var(--text)!important;
  font-weight:800!important;
  letter-spacing:-.045em;
}

p,label,span,div{
  font-family:'Plus Jakarta Sans',sans-serif;
}

.stTabs [data-baseweb="tab-list"]{
  gap:10px;
  border-bottom:1px solid rgba(148,163,184,.16);
}

.stTabs [data-baseweb="tab"]{
  background:#111827;
  border:1px solid rgba(148,163,184,.16);
  border-radius:14px 14px 0 0;
  color:#cbd5e1;
  padding:10px 18px;
  font-weight:800;
}

.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,#ff5c00,#ff2e63)!important;
  color:white!important;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"]{
  background:#1d2431!important;
  color:#fff!important;
  border:1px solid #313b4f!important;
  border-radius:14px!important;
  box-shadow:none!important;
}

.stTextInput input:focus,
.stTextArea textarea:focus{
  border-color:rgba(255,92,0,.9)!important;
  box-shadow:0 0 0 3px rgba(255,92,0,.14)!important;
}

.stTextArea textarea{
  min-height:170px!important;
  line-height:1.65!important;
}

.stButton>button,
.stDownloadButton>button{
  background:linear-gradient(135deg,#202838,#151b28)!important;
  color:#fff!important;
  border:1px solid #344155!important;
  border-radius:15px!important;
  font-weight:800!important;
  min-height:46px!important;
  box-shadow:0 14px 36px rgba(0,0,0,.28)!important;
  transition:all .2s ease!important;
}

.stButton>button:hover,
.stDownloadButton>button:hover{
  border-color:rgba(255,92,0,.9)!important;
  transform:translateY(-1px);
}

div[data-testid="stSidebar"]{
  background:#080c13!important;
  border-right:1px solid rgba(148,163,184,.14);
}

div[data-testid="stSidebar"] .stButton>button:first-child{
  background:linear-gradient(135deg,#ff5c00,#ff2e63)!important;
  border:none!important;
}

.ns-title{
  margin-bottom:20px;
}

.ns-title h1{
  font-size:2.55rem!important;
  margin-bottom:6px!important;
}

.ns-title h2{
  font-size:2rem!important;
  margin-bottom:6px!important;
}

.ns-title p{
  color:var(--muted);
  margin-top:0;
  font-size:1rem;
}

.glass-card,
.hub-card,
.logs-panel,
.stat-box{
  background:linear-gradient(180deg,rgba(17,24,39,.96),rgba(8,12,20,.96));
  border:1px solid rgba(148,163,184,.18);
  border-radius:28px;
  padding:24px;
  box-shadow:0 24px 80px rgba(0,0,0,.32);
}

.hub-card{
  margin-bottom:18px;
}

.hub-head{
  display:flex;
  align-items:center;
  gap:14px;
  margin-bottom:18px;
}

.hub-icon{
  min-width:48px;
  height:48px;
  border-radius:17px;
  display:flex;
  align-items:center;
  justify-content:center;
  background:linear-gradient(135deg,var(--accent),var(--pink));
  box-shadow:0 14px 34px rgba(255,92,0,.28);
  font-size:22px;
}

.hub-head h3{
  margin:0!important;
  font-size:1.3rem!important;
}

.hub-head p{
  margin:3px 0 0;
  color:var(--muted);
  font-size:.92rem;
}

.location-preview{
  background:#0d1421;
  border:1px dashed rgba(148,163,184,.35);
  border-radius:18px;
  padding:14px;
  margin-top:14px;
  color:#cbd5e1;
  word-break:break-word;
  font-size:.9rem;
}

.location-preview b{
  color:#fff;
}

.stat-box{
  border-radius:22px;
  padding:18px;
}

.label-caps{
  text-transform:uppercase;
  font-size:.72rem;
  color:var(--muted);
  letter-spacing:1.35px;
  font-weight:800;
  margin-bottom:8px;
}

.stat-val{
  font-family:'JetBrains Mono',monospace;
  font-size:1.2rem;
  font-weight:800;
  color:#fff;
}

.contact-title{
  font-size:2rem;
  font-weight:900;
  color:#fff;
  letter-spacing:-.04em;
  margin:18px 0 14px;
}

.clean-note{
  color:var(--muted);
  font-size:.95rem;
  line-height:1.6;
}

.small-info{
  color:#a3adbf;
  font-size:.86rem;
  margin-top:8px;
}

div[data-testid="stDataFrame"]{
  border-radius:20px;
  overflow:hidden;
  border:1px solid rgba(148,163,184,.18);
}

@media(max-width:900px){
  .ns-title h1{font-size:2rem!important;}
  .ns-title h2{font-size:1.65rem!important;}
}
</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# DATA HELPERS
# =========================================================
@st.cache_resource
def load_model():
    try:
        with open(MODEL_FILE, "rb") as file:
            return pickle.load(file)
    except Exception:
        return None


def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []
    return []


def save_contacts(contacts):
    with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=4)


def clean_phone(number):
    return (
        str(number)
        .replace("+", "")
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .strip()
    )


def save_log(report, risk, confidence, location_link):
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["timestamp", "report", "risk", "confidence", "location_link"])

        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                report,
                risk,
                confidence,
                location_link,
            ]
        )


def delete_recent_log():
    if not os.path.exists(LOG_FILE):
        return False

    df = pd.read_csv(LOG_FILE)

    if df.empty:
        return False

    df = df.iloc[:-1]
    df.to_csv(LOG_FILE, index=False)
    return True


def get_prediction_details(model, text):
    danger_keywords = [
        "help", "sos", "save", "danger", "following", "chasing", "threat",
        "grab", "unsafe", "stalk", "follow", "attack", "harass", "emergency",
        "bachao", "peecha", "dar"
    ]

    lowered = text.lower()

    if not model:
        return ("danger", 90) if any(k in lowered for k in danger_keywords) else ("safe", 65)

    prediction = model.predict([text])[0]
    confidence = 75

    try:
        if hasattr(model.named_steps["classifier"], "predict_proba"):
            probabilities = model.predict_proba([text])[0]
            confidence = round(max(probabilities) * 100, 2)
    except Exception:
        pass

    if any(k in lowered for k in danger_keywords):
        prediction = "danger"
        confidence = max(confidence, 90)

    return prediction, confidence


def whatsapp_link(number, message):
    return f"https://wa.me/{clean_phone(number)}?text={urllib.parse.quote(message)}"


def tel_link(number):
    return f"tel:{clean_phone(number)}"


def build_default_message():
    report = st.session_state.get(
        "active_report",
        "Emergency alert triggered from NariSuraksha AI."
    )
    location = st.session_state.get("location_link", "")

    location_text = location if location else "Location is not available yet. Please use the manual location field."

    return f"""🚨 EMERGENCY ALERT

I may be in an unsafe situation.

Report: {report}

My location:
{location_text}

Please call me immediately or contact emergency services.

Sent via NariSuraksha AI."""


def render_quick_numbers():
    components.html(
        """
        <html>
        <head>
        <style>
        body{
          margin:0;
          font-family:'Plus Jakarta Sans', Arial, sans-serif;
          background:transparent;
          color:white;
        }
        .box{
          background:linear-gradient(180deg,rgba(17,24,39,.96),rgba(8,12,20,.96));
          border:1px solid rgba(148,163,184,.18);
          border-radius:28px;
          padding:24px;
          box-shadow:0 24px 80px rgba(0,0,0,.32);
        }
        .head{
          display:flex;
          align-items:center;
          gap:14px;
          margin-bottom:18px;
        }
        .icon{
          min-width:48px;
          height:48px;
          border-radius:17px;
          display:flex;
          align-items:center;
          justify-content:center;
          background:linear-gradient(135deg,#ff5c00,#ff2e63);
          box-shadow:0 14px 34px rgba(255,92,0,.28);
          font-size:22px;
        }
        h3{
          margin:0;
          font-size:22px;
          letter-spacing:-.04em;
        }
        p{
          margin:4px 0 0;
          color:#a3adbf;
          font-size:14px;
        }
        .grid{
          display:grid;
          grid-template-columns:1fr;
          gap:12px;
          margin-top:12px;
        }
        a{
          display:flex;
          align-items:center;
          justify-content:space-between;
          gap:12px;
          text-decoration:none;
          color:#fff;
          background:linear-gradient(135deg,#1b2330,#111827);
          border:1px solid rgba(148,163,184,.18);
          padding:16px 18px;
          border-radius:18px;
          font-weight:850;
          box-shadow:0 12px 28px rgba(0,0,0,.22);
        }
        a:hover{
          border-color:rgba(255,92,0,.82);
        }
        small{
          color:#cbd5e1;
          font-weight:850;
          font-size:13px;
        }
        </style>
        </head>
        <body>
          <div class="box">
            <div class="head">
              <div class="icon">☎️</div>
              <div>
                <h3>Emergency One-Tap Numbers</h3>
                <p>Quick access to essential emergency support lines.</p>
              </div>
            </div>

            <div class="grid">
              <a href="tel:112">
                <span>🚨 Police Emergency</span>
                <small>112</small>
              </a>
              <a href="tel:181">
                <span>👩 Women Helpline</span>
                <small>181</small>
              </a>
              <a href="tel:1930">
                <span>💻 Cyber Crime Helpline</span>
                <small>1930</small>
              </a>
            </div>
          </div>
        </body>
        </html>
        """,
        height=315,
    )


def render_contact_card(contact, message):
    name = html.escape(contact.get("name", "Contact"))
    number = clean_phone(contact.get("number", ""))
    wa = html.escape(whatsapp_link(number, message), quote=True)
    call = html.escape(tel_link(number), quote=True)

    components.html(
        f"""
        <html>
        <head>
        <style>
        body{{
          margin:0;
          font-family:'Plus Jakarta Sans', Arial, sans-serif;
          background:transparent;
          color:white;
        }}
        .card{{
          background:linear-gradient(135deg,#1a2230,#111722);
          border:1px solid rgba(148,163,184,.18);
          border-radius:22px;
          padding:18px;
          margin:0;
          box-shadow:0 18px 50px rgba(0,0,0,.24);
        }}
        .name{{
          font-size:18px;
          font-weight:900;
          color:#fff;
          margin-bottom:13px;
          letter-spacing:-.02em;
        }}
        .actions{{
          display:grid;
          grid-template-columns:1fr 1fr;
          gap:12px;
        }}
        a{{
          display:flex;
          justify-content:center;
          align-items:center;
          gap:8px;
          text-decoration:none;
          color:#fff;
          padding:14px 16px;
          border-radius:15px;
          font-weight:900;
          min-height:24px;
        }}
        .wa{{background:linear-gradient(135deg,#16a34a,#22c55e);}}
        .call{{background:linear-gradient(135deg,#ff5c00,#ff2e63);}}
        </style>
        </head>
        <body>
          <div class="card">
            <div class="name">{name}</div>
            <div class="actions">
              <a class="wa" href="{wa}" target="_blank">💬 WhatsApp</a>
              <a class="call" href="{call}">📞 Call</a>
            </div>
          </div>
        </body>
        </html>
        """,
        height=135,
    )


def location_box():
    st.markdown(
        """
        <div class="hub-card">
          <div class="hub-head">
            <div class="hub-icon">📍</div>
            <div>
              <h3>Location Access</h3>
              <p>Use live GPS or enter a manual landmark to create a shareable map link.</p>
            </div>
          </div>
        """,
        unsafe_allow_html=True,
    )

    if get_geolocation:
        st.caption("Click the button below and allow location permission in your browser.")
        if st.button("📍 Allow / Refresh Location", key="location_btn"):
            loc = get_geolocation()

            try:
                lat = loc["coords"]["latitude"]
                lon = loc["coords"]["longitude"]
                st.session_state.location_link = f"https://www.google.com/maps?q={lat},{lon}"
                st.session_state.location_status = "Location captured successfully."
                st.session_state.alert_message = build_default_message()
                st.rerun()
            except Exception:
                st.session_state.location_status = (
                    "Location permission was denied or not available. Please enter a manual landmark."
                )
    else:
        st.warning(
            "Auto location is not available because streamlit-js-eval is not installed. "
            "Run: pip install streamlit-js-eval"
        )

    manual_location = st.text_input(
        "Manual Location / Landmark",
        placeholder="Example: Near GEC Vaishali main gate",
        key="manual_location",
    )

    if manual_location.strip():
        st.session_state.location_link = (
            "https://www.google.com/maps/search/?api=1&query="
            + urllib.parse.quote(manual_location.strip())
        )
        st.session_state.alert_message = build_default_message()

    if st.session_state.get("location_status"):
        st.info(st.session_state.location_status)

    if st.session_state.get("location_link"):
        safe_link = html.escape(st.session_state.location_link)
        st.markdown(
            f"""
            <div class="location-preview">
              <b>Map Link Ready:</b><br>{safe_link}
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def fake_call_ui():
    st.markdown(
        """
        <div class='ns-title'>
          <h2>Professional Fake Call</h2>
          <p>Launch a realistic incoming-call screen for quick exit situations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 1])

    with c1:
        caller_name = st.text_input(
            "Caller Name",
            value=st.session_state.get("fake_caller", "Mom"),
        )

    with c2:
        caller_type = st.selectbox(
            "Call Type",
            ["WhatsApp Audio", "Normal Phone Call", "Video Call"],
        )

    if st.button("Start Fake Call Screen"):
        st.session_state.fake_call_active = True
        st.session_state.fake_caller = caller_name
        st.session_state.fake_type = caller_type

    if st.session_state.get("fake_call_active"):
        caller = html.escape(st.session_state.get("fake_caller", "Mom"))
        call_type = html.escape(st.session_state.get("fake_type", "WhatsApp Audio"))

        components.html(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }}
            body {{
                background: transparent;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 710px;
                color: white;
            }}
            .phone {{
                width: 370px;
                height: 690px;
                background: #050505;
                border-radius: 52px;
                padding: 12px;
                position: relative;
                box-shadow: 0 45px 120px rgba(0,0,0,.7), inset 0 0 0 1px rgba(255,255,255,.12);
            }}
            .screen {{
                height: 100%;
                border-radius: 42px;
                overflow: hidden;
                position: relative;
                background:
                    linear-gradient(rgba(3,7,18,.55), rgba(3,7,18,.96)),
                    radial-gradient(circle at 50% 18%, rgba(255,92,0,.55), transparent 28%),
                    radial-gradient(circle at 20% 80%, rgba(37,99,235,.35), transparent 28%),
                    linear-gradient(145deg, #1f2937, #020617 75%);
                padding: 42px 28px 30px;
                text-align: center;
            }}
            .notch {{
                width: 120px;
                height: 30px;
                background: #050505;
                border-radius: 0 0 20px 20px;
                position: absolute;
                top: 12px;
                left: 50%;
                transform: translateX(-50%);
                z-index: 3;
            }}
            .top-row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 13px;
                font-weight: 700;
                opacity: .9;
            }}
            .status {{
                margin-top: 34px;
                font-size: 15px;
                color: #dbeafe;
                letter-spacing: .3px;
            }}
            .avatar-ring {{
                width: 138px;
                height: 138px;
                border-radius: 50%;
                margin: 72px auto 24px;
                background: conic-gradient(from 90deg, #ff5c00, #ff2e63, #8b5cf6, #60a5fa, #ff5c00);
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 70px rgba(255,92,0,.38);
                animation: pulse 1.8s infinite ease-in-out;
            }}
            @keyframes pulse {{
                0%,100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.04); }}
            }}
            .avatar {{
                width: 118px;
                height: 118px;
                border-radius: 50%;
                background: linear-gradient(145deg,#2b3344,#111827);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 54px;
            }}
            .name {{
                font-size: 40px;
                font-weight: 800;
                letter-spacing: -1.5px;
                margin-bottom: 8px;
            }}
            .subtitle {{
                font-size: 16px;
                color: #cbd5e1;
            }}
            .wave {{
                display: flex;
                gap: 5px;
                justify-content: center;
                align-items: end;
                height: 32px;
                margin: 30px 0 76px;
            }}
            .wave span {{
                width: 5px;
                border-radius: 999px;
                background: #e5e7eb;
                animation: wave 1s infinite ease-in-out;
            }}
            .wave span:nth-child(1) {{ height: 14px; animation-delay: .05s; }}
            .wave span:nth-child(2) {{ height: 25px; animation-delay: .12s; }}
            .wave span:nth-child(3) {{ height: 18px; animation-delay: .18s; }}
            .wave span:nth-child(4) {{ height: 28px; animation-delay: .24s; }}
            .wave span:nth-child(5) {{ height: 16px; animation-delay: .30s; }}
            @keyframes wave {{
                50% {{ transform: scaleY(.38); opacity: .45; }}
            }}
            .actions {{
                display: flex;
                justify-content: space-between;
                padding: 0 28px;
            }}
            .circle {{
                width: 76px;
                height: 76px;
                border-radius: 50%;
                display: flex;
                justify-content: center;
                align-items: center;
                font-size: 32px;
                box-shadow: 0 20px 45px rgba(0,0,0,.42);
            }}
            .decline {{ background: #ef4444; }}
            .accept {{ background: #22c55e; }}
            .labels {{
                display: flex;
                justify-content: space-between;
                padding: 12px 33px 0;
                font-size: 13px;
                font-weight: 700;
                color: #e2e8f0;
            }}
            .bottom-bar {{
                width: 120px;
                height: 5px;
                border-radius: 999px;
                background: rgba(255,255,255,.72);
                position: absolute;
                left: 50%;
                bottom: 14px;
                transform: translateX(-50%);
            }}
            </style>
            </head>
            <body>
                <div class="phone">
                    <div class="notch"></div>
                    <div class="screen">
                        <div class="top-row">
                            <span>9:41</span>
                            <span>●●●  5G  🔋</span>
                        </div>
                        <div class="status">Incoming {call_type}</div>
                        <div class="avatar-ring">
                            <div class="avatar">👤</div>
                        </div>
                        <div class="name">{caller}</div>
                        <div class="subtitle">is calling...</div>
                        <div class="wave">
                            <span></span><span></span><span></span><span></span><span></span>
                        </div>
                        <div class="actions">
                            <div><div class="circle decline">✕</div></div>
                            <div><div class="circle accept">☎</div></div>
                        </div>
                        <div class="labels">
                            <span>Decline</span>
                            <span>Accept</span>
                        </div>
                        <div class="bottom-bar"></div>
                    </div>
                </div>
            </body>
            </html>
            """,
            height=740,
        )

        if st.button("Close Fake Call"):
            st.session_state.fake_call_active = False
            st.rerun()


# =========================================================
# SESSION STATE
# =========================================================
if "contacts" not in st.session_state:
    st.session_state.contacts = load_contacts()

if "location_link" not in st.session_state:
    st.session_state.location_link = ""

if "alert_message" not in st.session_state:
    st.session_state.alert_message = build_default_message()

model = load_model()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## NariSuraksha 🛡️")
    st.caption("Personal Safety Console")
    st.divider()

    if st.button("🚨 Trigger Rapid SOS"):
        st.session_state.last_prediction = "danger"
        st.session_state.last_confidence = 95
        st.session_state.active_report = "Emergency alert triggered from NariSuraksha AI."
        st.session_state.alert_message = build_default_message()
        save_log(
            st.session_state.active_report,
            "danger",
            95,
            st.session_state.get("location_link", ""),
        )
        st.success("SOS triggered and incident record saved.")

    st.divider()
    st.markdown("### Trusted Contacts")

    c_name = st.text_input("Contact Name")
    c_num = st.text_input("Phone Number with Country Code", placeholder="Example: 919876543210")

    if st.button("Save Contact"):
        if c_name.strip() and c_num.strip():
            st.session_state.contacts.append(
                {
                    "name": c_name.strip(),
                    "number": clean_phone(c_num),
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
            save_contacts(st.session_state.contacts)
            st.success("Contact saved successfully.")
            st.rerun()
        else:
            st.warning("Please enter both contact name and phone number.")

    if st.session_state.contacts:
        st.markdown("#### Saved Priority Contacts")

        for i, contact in enumerate(st.session_state.contacts):
            st.write(f"✅ {contact.get('name', 'Contact')} — {contact.get('number', '')}")

            if st.button(f"Delete {contact.get('name', 'Contact')}", key=f"delete_contact_{i}"):
                st.session_state.contacts.pop(i)
                save_contacts(st.session_state.contacts)
                st.success("Priority contact deleted.")
                st.rerun()

# =========================================================
# TOP STATS
# =========================================================
st.markdown(
    """
    <div class='ns-title'>
      <h1>NariSuraksha Safety Console</h1>
      <p>Analyze risk, prepare emergency messages, contact trusted people, and maintain incident records.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(
        "<div class='stat-box'><p class='label-caps'>System</p><div class='stat-val'>Online</div></div>",
        unsafe_allow_html=True,
    )

with s2:
    st.markdown(
        f"<div class='stat-box'><p class='label-caps'>Model</p><div class='stat-val'>{'AI Ready' if model else 'Keyword Mode'}</div></div>",
        unsafe_allow_html=True,
    )

with s3:
    st.markdown(
        f"<div class='stat-box'><p class='label-caps'>Contacts</p><div class='stat-val'>{len(st.session_state.contacts)}</div></div>",
        unsafe_allow_html=True,
    )

with s4:
    st.markdown(
        "<div class='stat-box'><p class='label-caps'>Records</p><div class='stat-val'>CSV Ready</div></div>",
        unsafe_allow_html=True,
    )

st.divider()

tabs = st.tabs(["Analyze", "Emergency Hub", "Fake Call", "Incident Records"])

# =========================================================
# ANALYZE TAB
# =========================================================
with tabs[0]:
    left, right = st.columns([2, 1])

    with left:
        st.markdown("### Incident Reporting")
        user_report = st.text_area(
            "Describe your situation",
            height=160,
            placeholder="Example: Someone is following me near the bus stop...",
        )

        if st.button("Evaluate Threat"):
            if user_report.strip():
                pred, conf = get_prediction_details(model, user_report)
                st.session_state.last_prediction = pred
                st.session_state.last_confidence = conf
                st.session_state.active_report = user_report.strip()
                st.session_state.alert_message = build_default_message()
                save_log(user_report.strip(), pred, conf, st.session_state.get("location_link", ""))
                st.success("Threat evaluated and incident record saved.")
            else:
                st.warning("Please describe your situation first.")

    with right:
        risk = st.session_state.get("last_prediction", "not checked")
        conf = st.session_state.get("last_confidence", 0)
        color = "#ff3b30" if risk == "danger" else "#22c55e"

        st.markdown(
            f"""
            <div class="glass-card" style="border-left:6px solid {color};">
                <p class="label-caps">Assessed Risk</p>
                <h2 style="color:{color}!important;">{str(risk).upper()}</h2>
                <p class="clean-note">Confidence: {conf}%</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =========================================================
# EMERGENCY HUB TAB
# =========================================================
with tabs[1]:
    st.markdown(
        """
        <div class='ns-title'>
          <h2>Emergency Hub</h2>
          <p>Capture your location, edit the emergency alert, contact trusted people, and save emergency records from one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1], gap="large")

    with left:
        location_box()
        render_quick_numbers()

    with right:
        st.markdown(
            """
            <div class="hub-card">
              <div class="hub-head">
                <div class="hub-icon">💬</div>
                <div>
                  <h3>Editable WhatsApp Alert</h3>
                  <p>Edit the message, confirm your location link, then send it to priority contacts.</p>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.get("location_link") and "Location is not available yet" in st.session_state.alert_message:
            st.session_state.alert_message = build_default_message()

        editable_msg = st.text_area(
            "Edit message before sending",
            key="alert_message",
            height=270,
        )

        st.markdown("<div class='contact-title'>Priority Contacts</div>", unsafe_allow_html=True)

        if st.session_state.contacts:
            for contact in st.session_state.contacts:
                render_contact_card(contact, editable_msg)

            st.write("")
            if st.button("Save Current Emergency Record"):
                save_log(
                    st.session_state.get("active_report", "Manual emergency message prepared."),
                    st.session_state.get("last_prediction", "manual"),
                    st.session_state.get("last_confidence", 0),
                    st.session_state.get("location_link", ""),
                )
                st.success("Emergency record saved successfully.")
        else:
            st.warning("Please save at least one trusted contact from the sidebar.")

# =========================================================
# FAKE CALL TAB
# =========================================================
with tabs[2]:
    fake_call_ui()

# =========================================================
# INCIDENT RECORDS TAB
# =========================================================
with tabs[3]:
    st.markdown(
        """
        <div class='logs-panel'>
          <h2>Incident Records</h2>
          <p style='color:#98a4b8;'>
            All saved emergency records appear here. You can download the CSV file or delete the most recent record.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)

        if not df.empty:
            st.dataframe(df, use_container_width=True, height=360)

            csv_data = df.to_csv(index=False).encode("utf-8")

            c1, c2 = st.columns([1, 1])

            with c1:
                st.download_button(
                    label="⬇️ Download Incident Records CSV",
                    data=csv_data,
                    file_name="narisuraksha_incident_records.csv",
                    mime="text/csv",
                )

            with c2:
                if st.button("🗑️ Delete Recent Incident Record"):
                    deleted = delete_recent_log()
                    if deleted:
                        st.success("Most recent incident record deleted.")
                        st.rerun()
                    else:
                        st.warning("No record is available to delete.")
        else:
            st.info("The incident log file is empty.")
    else:
        st.info("No incident records have been saved yet.")

st.markdown(
    "<p style='text-align:center;color:#8B949E;margin-top:50px;font-size:.75rem;'>NariSuraksha AI © 2026 | Built for Safety Project</p>",
    unsafe_allow_html=True,
)
