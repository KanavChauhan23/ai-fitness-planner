import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="APEX · Indian Health Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --saffron:  #FF9933;
    --gold:     #FFD700;
    --teal:     #00BCD4;
    --green-neon: #00e676;
    --bg-base:  #050810;
    --bg-card:  rgba(10,15,30,0.97);
    --text-bright: #F0F4FF;
    --text-mid: #8892A4;
    --text-dim: #3D4A5C;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main .block-container { padding: 1rem 2rem 4rem; max-width: 1400px; }
.stApp { background: var(--bg-base); color: var(--text-bright); }
.stApp::before {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 70% 45% at 10% 0%, rgba(255,153,51,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 55% 40% at 90% 100%, rgba(0,188,212,0.06) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(255,215,0,0.025) 0%, transparent 60%);
}
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(255,153,51,0.35); border-radius: 4px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(4,6,18,0.99) !important;
    border-right: 1px solid rgba(255,153,51,0.13) !important;
}

/* ── Hero ── */
.hero-wrap { padding: 1.8rem 1rem 0.8rem; text-align: center; }
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; letter-spacing: 0.38em;
    color: var(--saffron); border: 1px solid rgba(255,153,51,0.35);
    padding: 0.22rem 0.9rem; border-radius: 100px; background: rgba(255,153,51,0.08);
    margin-bottom: 0.9rem; text-transform: uppercase;
}
.hero-title {
    font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: clamp(2rem, 4.5vw, 3.6rem); line-height: 1.05; letter-spacing: -0.02em;
    background: linear-gradient(120deg, #ffffff 0%, #FF9933 38%, #FFD700 65%, #00BCD4 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.55rem;
}
.hero-sub { color: var(--text-mid); font-size: 0.9rem; font-weight: 300; max-width: 500px; margin: 0 auto 1.2rem; line-height: 1.65; }
.tricolor-line { height: 3px; border-radius: 100px; margin: 0 auto 1.5rem; width: 110px; background: linear-gradient(90deg, #FF9933 33.3%, #ffffff 33.3% 66.6%, #138808 66.6%); }

/* ── Section header ── */
.sec-head { display: flex; align-items: center; gap: 0.7rem; margin: 1.8rem 0 1rem; padding-bottom: 0.55rem; border-bottom: 1px solid rgba(255,153,51,0.1); }
.sec-icon { width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg,rgba(255,153,51,0.2),rgba(0,188,212,0.1)); border: 1px solid rgba(255,153,51,0.3); display:flex; align-items:center; justify-content:center; font-size:0.9rem; flex-shrink:0; }
.sec-title { font-family:'Syne',sans-serif; font-size:0.76rem; font-weight:700; letter-spacing:0.2em; color:var(--text-bright); text-transform:uppercase; }
.sec-line { flex:1; height:1px; background:linear-gradient(90deg,rgba(255,153,51,0.18),transparent); }

/* ── Profile input section wrapper ── */
.profile-wrap {
    background: var(--bg-card);
    border: 1px solid rgba(255,153,51,0.15);
    border-radius: 16px;
    padding: 1.5rem 1.75rem 1.25rem;
    position: relative; overflow: hidden;
}
.profile-wrap::before {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, #FF9933, #FFD700, #00BCD4);
    opacity: 0.7;
}

/* ── Metric cards ── */
.mc {
    background: var(--bg-card);
    border: 1px solid rgba(255,153,51,0.13);
    border-radius: 13px; padding: 1rem 1rem 0.9rem;
    position: relative; overflow: hidden; height: 100%;
    transition: border-color 0.2s;
}
.mc:hover { border-color: rgba(255,153,51,0.38); }
.mc::after {
    content:''; position:absolute; top:0; left:0; right:0; height:2px;
    background: var(--mc-accent, #FF9933); opacity: 0.5;
}
.mc-glow {
    position:absolute; top:-24px; right:-24px; width:70px; height:70px;
    border-radius:50%; opacity:0.1; filter:blur(18px);
    background: var(--mc-accent, #FF9933);
}
.mc-label {
    font-family:'JetBrains Mono',monospace; font-size:0.55rem; letter-spacing:0.2em;
    color:var(--text-mid); text-transform:uppercase; margin-bottom:0.45rem; line-height:1.3;
}
.mc-val {
    font-family:'Syne',sans-serif; font-size:1.55rem; font-weight:800; line-height:1;
    color: var(--mc-accent, #FF9933);
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
}
.mc-unit { font-size:0.72rem; color:var(--text-mid); font-family:'DM Sans',sans-serif; margin-left:0.2rem; }
.mc-sub { font-size:0.7rem; margin-top:0.4rem; }

/* ── Chips ── */
.chip { display:inline-flex; align-items:center; font-family:'JetBrains Mono',monospace; font-size:0.58rem; padding:0.15rem 0.55rem; border-radius:100px; font-weight:500; letter-spacing:0.05em; white-space:nowrap; }
.chip-s { background:rgba(255,153,51,0.12); color:#FF9933; border:1px solid rgba(255,153,51,0.3); }
.chip-g { background:rgba(0,230,118,0.1);  color:#00e676; border:1px solid rgba(0,230,118,0.3); }
.chip-t { background:rgba(0,188,212,0.1);  color:#00BCD4; border:1px solid rgba(0,188,212,0.25); }
.chip-o { background:rgba(255,215,0,0.1);  color:#FFD700; border:1px solid rgba(255,215,0,0.3); }
.chip-r { background:rgba(255,82,82,0.1);  color:#ff5252; border:1px solid rgba(255,82,82,0.3); }

/* ── Macro bars ── */
.mbar { margin:0.5rem 0; }
.mbar-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:0.28rem; }
.mbar-name { font-size:0.78rem; color:var(--text-bright); font-weight:500; }
.mbar-val { font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:var(--text-mid); }
.mbar-track { height:5px; background:rgba(255,255,255,0.055); border-radius:100px; overflow:hidden; }
.mbar-fill { height:100%; border-radius:100px; }

/* ── Plan blocks ── */
.pblock { background:var(--bg-card); border-radius:15px; padding:1.4rem 1.65rem; margin-bottom:1.2rem; position:relative; overflow:hidden; border:1px solid rgba(255,153,51,0.15); }
.pblock::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; }
.pblock.ora::before { background:linear-gradient(90deg,transparent,#FF9933,#FFD700,transparent); }
.pblock.tea::before { background:linear-gradient(90deg,transparent,#00BCD4,transparent); }
.pblock-title { font-family:'Syne',sans-serif; font-size:0.75rem; font-weight:700; letter-spacing:0.16em; text-transform:uppercase; margin-bottom:0.85rem; }
.pblock.ora .pblock-title { color:#FF9933; }
.pblock.tea .pblock-title { color:#00BCD4; }

/* ── Chat ── */
.cbubble { padding:0.85rem 1.1rem; border-radius:11px; margin-bottom:0.75rem; line-height:1.65; font-size:0.87rem; }
.cu { background:rgba(255,153,51,0.07); border-left:3px solid #FF9933; }
.ca { background:rgba(0,188,212,0.06); border-left:3px solid #00BCD4; }
.clbl { font-family:'JetBrains Mono',monospace; font-size:0.57rem; letter-spacing:0.14em; opacity:0.5; margin-bottom:0.35rem; text-transform:uppercase; }

/* ── Sidebar components ── */
.sb-logo { text-align:center; padding:1.4rem 1rem 1rem; border-bottom:1px solid rgba(255,153,51,0.1); margin-bottom:1.1rem; }
.sb-logo-name { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800; letter-spacing:0.15em; background:linear-gradient(135deg,#FF9933,#FFD700); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.sb-logo-sub  { font-family:'JetBrains Mono',monospace; font-size:0.5rem; letter-spacing:0.3em; color:var(--text-dim); margin-top:0.2rem; }
.sb-row { padding:0.65rem 1rem; background:rgba(255,153,51,0.05); border:1px solid rgba(255,153,51,0.1); border-radius:9px; margin-bottom:0.5rem; display:flex; align-items:center; justify-content:space-between; }
.sb-row-label { font-size:0.73rem; color:var(--text-mid); }
.sb-row-val   { font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:#FF9933; font-weight:600; }
.sb-tip { background:rgba(0,188,212,0.04); border:1px solid rgba(0,188,212,0.14); border-radius:9px; padding:0.7rem 0.85rem; margin-bottom:0.5rem; font-size:0.75rem; color:var(--text-mid); line-height:1.55; }
.sb-tip strong { color:#00BCD4; display:block; font-size:0.62rem; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:0.18rem; font-family:'JetBrains Mono',monospace; }
.sb-sec { font-family:'JetBrains Mono',monospace; font-size:0.56rem; letter-spacing:0.26em; color:var(--text-dim); text-transform:uppercase; margin:1rem 0 0.55rem; padding:0 1rem; }

/* ══════════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES
══════════════════════════════════════════ */

/* All text inputs — CRITICAL color fix */
.stTextInput input {
    background: rgba(15,20,40,0.9) !important;
    border: 1px solid rgba(255,153,51,0.28) !important;
    border-radius: 10px !important;
    color: #F0F4FF !important;
    caret-color: #FF9933 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 0.9rem !important;
}
.stTextInput input::placeholder { color: rgba(136,146,164,0.5) !important; }
.stTextInput input:focus {
    border-color: rgba(255,153,51,0.6) !important;
    box-shadow: 0 0 0 3px rgba(255,153,51,0.1) !important;
    outline: none !important;
    color: #FFFFFF !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(15,20,40,0.9) !important;
    border: 1px solid rgba(255,153,51,0.28) !important;
    border-radius: 10px !important;
    color: #F0F4FF !important;
}
/* Multiselect */
.stMultiSelect > div > div {
    background: rgba(15,20,40,0.9) !important;
    border: 1px solid rgba(255,153,51,0.28) !important;
    border-radius: 10px !important;
    color: #F0F4FF !important;
}
/* Dropdown option text */
[data-baseweb="select"] [data-testid="stSelectbox"] span,
[data-baseweb="select"] div { color: #F0F4FF !important; }

/* All labels */
label, .stSelectbox label, .stTextInput label, .stMultiSelect label {
    color: #8892A4 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.64rem !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    margin-bottom: 0.3rem !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(255,153,51,0.18), rgba(255,215,0,0.1)) !important;
    border: 1px solid rgba(255,153,51,0.5) !important;
    color: #FF9933 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.76rem !important; font-weight: 700 !important;
    letter-spacing: 0.16em !important; border-radius: 10px !important;
    padding: 0.65rem 1.2rem !important; width: 100% !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(255,153,51,0.3), rgba(255,215,0,0.2)) !important;
    box-shadow: 0 0 22px rgba(255,153,51,0.28) !important;
    transform: translateY(-1px) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.025) !important; border-radius: 11px !important; padding: 4px !important; gap: 3px !important; }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 500 !important; color: #8892A4 !important; padding: 0.48rem 1rem !important; }
.stTabs [aria-selected="true"] { background: rgba(255,153,51,0.14) !important; color: #FF9933 !important; }

/* Metric widgets */
.stMetric { background: rgba(255,153,51,0.04) !important; border: 1px solid rgba(255,153,51,0.1) !important; border-radius: 10px !important; padding: 0.7rem 0.9rem !important; }
[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; color: #FF9933 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { font-family: 'JetBrains Mono', monospace !important; font-size: 0.62rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: #8892A4 !important; }

/* Expander */
.stExpander { background: var(--bg-card) !important; border: 1px solid rgba(255,153,51,0.15) !important; border-radius: 12px !important; }
div[data-testid="stExpander"] div[role="button"] p { font-family: 'Syne', sans-serif !important; font-size: 0.8rem !important; font-weight: 700 !important; }

/* Multiselect tags — force dark background, no white */
[data-baseweb="tag"] {
    background: rgba(255,153,51,0.14) !important;
    border: 1px solid rgba(255,153,51,0.35) !important;
    border-radius: 6px !important;
}
[data-baseweb="tag"] span { color: #FF9933 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.68rem !important; }
[data-baseweb="tag"] button svg { fill: #FF9933 !important; }

/* Multiselect container inner background */
[data-baseweb="select"] > div { background: rgba(15,20,40,0.9) !important; }
.stMultiSelect [data-baseweb="select"] > div { background: rgba(15,20,40,0.9) !important; }
[data-testid="stMultiSelect"] div { background-color: transparent !important; }
[data-baseweb="select"] [data-baseweb="tag"] { background: rgba(255,153,51,0.14) !important; }

/* Form submit button (ASK →) — must override separately */
button[kind="formSubmit"], button[data-testid="baseButton-secondary"] {
    background: linear-gradient(135deg, rgba(255,153,51,0.22), rgba(255,215,0,0.14)) !important;
    border: 1px solid rgba(255,153,51,0.55) !important;
    color: #FF9933 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.76rem !important; font-weight: 700 !important;
    letter-spacing: 0.14em !important; border-radius: 10px !important;
}
button[kind="formSubmit"]:hover {
    background: linear-gradient(135deg, rgba(255,153,51,0.35), rgba(255,215,0,0.25)) !important;
    box-shadow: 0 0 18px rgba(255,153,51,0.3) !important;
    color: #FFFFFF !important;
}
/* Force ALL buttons in forms to show orange text */
div[data-testid="stForm"] button { color: #FF9933 !important; background: rgba(255,153,51,0.12) !important; border: 1px solid rgba(255,153,51,0.45) !important; }

hr { border-color: rgba(255,153,51,0.1) !important; }
div[data-testid="stForm"] { border: none !important; padding: 0 !important; }

/* Number/text input inside form */
.stForm .stTextInput input { color: #FFFFFF !important; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def bmi_calc(w, h):
    if h <= 0: return 0.0, "N/A", "chip-s"
    b = w / ((h/100)**2)
    if b < 18.5:   return round(b,1), "Underweight", "chip-t"
    elif b < 23:   return round(b,1), "Healthy ✓",   "chip-g"
    elif b < 27.5: return round(b,1), "Overweight",   "chip-s"
    else:          return round(b,1), "Obese",        "chip-r"

def tdee_calc(w, h, age, sex, act):
    bmr = (10*w + 6.25*h - 5*age + 5) if sex=="Male" else (10*w + 6.25*h - 5*age - 161)
    m = {"Sedentary (Desk job)":1.2, "Lightly Active (Walk 1-3 days)":1.375,
         "Moderately Active (Exercise 3-5 days)":1.55, "Very Active (Hard exercise 6-7 days)":1.725,
         "Athlete / Physical Labour":1.9}
    return round(bmr), round(bmr * m.get(act, 1.55))

def ideal_wt(h, sex):
    if h < 152.4: return 50 if sex=="Male" else 45.5
    ex = (h - 152.4) / 2.54
    return round(50+2.3*ex, 1) if sex=="Male" else round(45.5+2.3*ex, 1)

def macros(tdee, goal):
    if goal=="Weight Loss":            c,p,f,ch = tdee-400, .35,.30,.35
    elif goal=="Muscle Gain":          c,p,f,ch = tdee+350, .30,.25,.45
    elif goal=="Strength Training":    c,p,f,ch = tdee+200, .32,.28,.40
    elif goal=="Athletic Performance": c,p,f,ch = tdee+300, .28,.25,.47
    else:                              c,p,f,ch = tdee,     .25,.30,.45
    return {"cals":round(c), "pro":round(c*p/4), "fat":round(c*f/9), "carb":round(c*ch/4)}

def mbar_html(label, val, mx, color):
    pct = min(100, round(val/mx*100))
    return f"""<div class="mbar">
    <div class="mbar-top"><span class="mbar-name">{label}</span><span class="mbar-val">{val}g</span></div>
    <div class="mbar-track"><div class="mbar-fill" style="width:{pct}%;background:{color}"></div></div></div>"""

def chip_html(text, cls="chip-s"):
    return f'<span class="chip {cls}">{text}</span>'

def mc_html(label, val, unit, sub_html, accent):
    return f"""<div class="mc" style="--mc-accent:{accent}">
    <div class="mc-glow"></div>
    <div class="mc-label">{label}</div>
    <div class="mc-val">{val}<span class="mc-unit">{unit}</span></div>
    <div class="mc-sub">{sub_html}</div></div>"""

def safe_f(v, d):
    try: return float(str(v).strip())
    except: return d

def ask(client, sys, usr):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system","content":sys},{"role":"user","content":usr}],
        max_tokens=2500, temperature=0.72
    )
    return r.choices[0].message.content


# ─── Session ──────────────────────────────────────────────────────────────────
for k,v in {"dp":None,"fp":None,"qa":[],"done":False}.items():
    if k not in st.session_state: st.session_state[k] = v

groq_key = st.secrets.get("GROQ_API_KEY","")


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div class="sb-logo">
        <div style="font-size:1.7rem;margin-bottom:0.25rem;">🏋️</div>
        <div class="sb-logo-name">⚡ APEX</div>
        <div class="sb-logo-sub">INDIAN HEALTH INTELLIGENCE</div>
        <div style="height:3px;width:75px;margin:0.65rem auto 0;border-radius:100px;
             background:linear-gradient(90deg,#FF9933,#fff,#138808);"></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">System Status</div>', unsafe_allow_html=True)
    if groq_key:
        for lbl, val in [("🟢 AI Engine","ONLINE"),("⚡ Model","LLaMA 3.3 70B"),("🇮🇳 Mode","INDIAN DIET")]:
            st.markdown(f'<div class="sb-row"><span class="sb-row-label">{lbl}</span><span class="sb-row-val">{val}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sb-row" style="border-color:rgba(255,82,82,0.3)"><span class="sb-row-label">🔴 AI Engine</span><span class="sb-row-val" style="color:#ff5252">OFFLINE</span></div>', unsafe_allow_html=True)
        st.markdown("[→ Setup Groq API Key](https://console.groq.com)")

    st.markdown('<div class="sb-sec">Daily Wellness Tips</div>', unsafe_allow_html=True)
    for t, tip in [
        ("💧 Hydration","Start with warm jeera water + lemon. Aim 8–10 glasses daily."),
        ("🌅 Morning Ritual","10 rounds Surya Namaskar burns ~100 kcal & boosts metabolism."),
        ("🍛 Meal Rhythm","Largest meal at lunch (1–2 PM). Keep dinner light before 8 PM."),
        ("🌿 Ayurveda","Haldi + kali mirch daily = natural anti-inflammatory powerhouse."),
        ("😴 Recovery","7–9 hrs sleep regulates cortisol & muscle repair hormones."),
    ]:
        st.markdown(f'<div class="sb-tip"><strong>{t}</strong>{tip}</div>', unsafe_allow_html=True)

    if st.session_state.done:
        st.markdown('<div class="sb-sec">Session</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sb-row"><span class="sb-row-label">📋 Plan Status</span><span class="sb-row-val">ACTIVE</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sb-row"><span class="sb-row-label">💬 Q&A Chats</span><span class="sb-row-val">{len(st.session_state.qa)}</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 NEW SESSION"):
            for k in ["dp","fp","qa","done"]:
                st.session_state[k] = None if k!="qa" else []
            st.session_state.done = False
            st.rerun()


# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""<div class="hero-wrap">
    <div class="hero-eyebrow">🇮🇳 MADE FOR INDIA · POWERED BY GROQ AI</div>
    <h1 class="hero-title">APEX HEALTH PLANNER</h1>
    <p class="hero-sub">AI-crafted Indian diet & fitness plans calibrated to your unique body and goals</p>
    <div class="tricolor-line"></div>
</div>""", unsafe_allow_html=True)

if not groq_key:
    st.error("⚠️ GROQ_API_KEY missing — Streamlit Cloud → App Settings → Secrets → add: GROQ_API_KEY = \"gsk_...\"")
    st.stop()

client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")


# ─── Profile Inputs (NO wrapper divs — they cause the empty box bug) ────────
st.markdown('<div class="sec-head"><div class="sec-icon">👤</div><div class="sec-title">Your Biometric Profile</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

# Styled column background via CSS targeting
st.markdown("""<style>
/* Wrap all 3 profile columns in a subtle card look */
div[data-testid="column"]:nth-child(-n+3) > div:first-child {
    background: rgba(10,15,30,0.95);
    border: 1px solid rgba(255,153,51,0.13);
    border-radius: 14px; padding: 1.25rem 1.25rem 1rem;
    position: relative;
}
</style>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    age_in    = st.text_input("Age (years)",  value="25", placeholder="e.g. 25")
    height_in = st.text_input("Height (cm)",  value="170", placeholder="e.g. 170")
    sex       = st.selectbox("Biological Sex", ["Male","Female","Other"])
with c2:
    weight_in = st.text_input("Weight (kg)",  value="70", placeholder="e.g. 70")
    activity  = st.selectbox("Activity Level", [
        "Sedentary (Desk job)","Lightly Active (Walk 1-3 days)",
        "Moderately Active (Exercise 3-5 days)","Very Active (Hard exercise 6-7 days)","Athlete / Physical Labour"])
    diet_pref = st.selectbox("Diet Type", [
        "Non-Vegetarian","Vegetarian","Vegan","Eggetarian",
        "Jain (No root vegetables)","Sattvic","Low Carb Indian","Diabetic-friendly Indian"])
with c3:
    goal      = st.selectbox("Fitness Goal", [
        "Weight Loss","Muscle Gain","Stay Fit & Healthy","Strength Training","Endurance & Stamina","Athletic Performance"])
    conditions= st.multiselect("Health Conditions", [
        "None","Diabetes (Type 2)","Hypertension","High Cholesterol",
        "PCOD/PCOS","Thyroid","Acidity / IBS","Anemia","Joint Pain"], default=["None"])
    region    = st.selectbox("Regional Cuisine", [
        "North Indian","South Indian","East Indian (Bengali/Odia)","West Indian (Gujarati/Marathi)","Mixed / Pan India"])

age    = max(10, int(safe_f(age_in, 25)))
height = max(100, safe_f(height_in, 170))
weight = max(20,  safe_f(weight_in, 70))


# ─── Biometrics Dashboard ─────────────────────────────────────────────────────
bmi_v, bmi_cat, bmi_cls = bmi_calc(weight, height)
bmr_v, tdee_v = tdee_calc(weight, height, age, sex, activity)
idwt  = ideal_wt(height, sex)
mac   = macros(tdee_v, goal)
water = round(weight*0.033, 1)
diff  = round(weight - idwt, 1)
wlbl  = f"+{diff} kg over" if diff>0 else f"{abs(diff)} kg under" if diff<0 else "At ideal ✓"

st.markdown('<div class="sec-head"><div class="sec-icon">📊</div><div class="sec-title">Live Biometric Analysis</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

cols = st.columns(6)
card_data = [
    ("BMI · Asian\nStandard",    bmi_v,          "BMI",    f'<span class="chip {bmi_cls}">{bmi_cat}</span>',          "#FF9933"),
    ("Basal\nMetabolic Rate",    f"{bmr_v:,}",   "kcal",   f'<span class="chip chip-t">Resting burn</span>',          "#00BCD4"),
    ("Daily Calorie\nTarget",    f"{mac['cals']:,}","kcal", f'<span class="chip chip-s">{goal[:14]}</span>',           "#FF9933"),
    ("Ideal Body\nWeight",       idwt,            "kg",     f'<span class="chip chip-o">{wlbl}</span>',               "#FFD700"),
    ("Daily Water\nIntake",      water,           "L",      f'<span class="chip chip-t">{round(water*4)} glasses</span>',  "#00BCD4"),
    ("Daily Protein\nTarget",    mac["pro"],      "g",      f'<span class="chip chip-g">Muscle synthesis</span>',     "#00e676"),
]
for col, (label, val, unit, sub, accent) in zip(cols, card_data):
    with col:
        st.markdown(mc_html(label, val, unit, sub, accent), unsafe_allow_html=True)


# ─── Macros ────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-icon">🧬</div><div class="sec-title">Macro Nutrition Targets</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

ma1, ma2 = st.columns([3,1])
with ma1:
    p_pct = round(mac["pro"]*4/mac["cals"]*100)
    c_pct = round(mac["carb"]*4/mac["cals"]*100)
    f_pct = round(mac["fat"]*9/mac["cals"]*100)
    st.markdown(f"""<div class="pblock ora">
    <div class="pblock-title">🎯 Daily Macro Targets · {mac['cals']:,} kcal/day</div>
    {mbar_html("Protein",      mac["pro"],  250, "#FF9933")}
    {mbar_html("Carbohydrates",mac["carb"], 380, "#00BCD4")}
    {mbar_html("Fats",         mac["fat"],  130, "#FFD700")}
    </div>""", unsafe_allow_html=True)

with ma2:
    st.markdown(f"""<div class="mc" style="--mc-accent:#FF9933;height:100%">
    <div class="mc-glow"></div>
    <div class="mc-label">Macro Split</div>
    <div style="margin-top:0.9rem;display:flex;flex-direction:column;gap:0.7rem;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:0.8rem;color:#FF9933">● Protein</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#F0F4FF">{p_pct}%</span></div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:0.8rem;color:#00BCD4">● Carbs</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#F0F4FF">{c_pct}%</span></div>
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:0.8rem;color:#FFD700">● Fats</span>
            <span style="font-family:'JetBrains Mono',monospace;font-size:0.78rem;color:#F0F4FF">{f_pct}%</span></div>
    </div>
    <div style="margin-top:1rem;padding-top:0.7rem;border-top:1px solid rgba(255,153,51,0.1);
         font-size:0.7rem;color:#6b7589">For: {goal}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── Generate ─────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-icon">⚡</div><div class="sec-title">Generate Your AI Plan</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

_, gc, _ = st.columns([1,2,1])
with gc:
    gen = st.button("⚡ GENERATE MY APEX PLAN")

if gen:
    cond = ", ".join([c for c in conditions if c!="None"]) or "None"
    prof = f"""Age:{age}|Sex:{sex}|Weight:{weight}kg|Height:{height}cm|BMI:{bmi_v}({bmi_cat})|BMR:{bmr_v}|TDEE:{tdee_v}|IdealWT:{idwt}kg
Goal:{goal}|Activity:{activity}|Diet:{diet_pref}|Region:{region}|Conditions:{cond}
Macros:{mac['cals']}kcal|P:{mac['pro']}g|C:{mac['carb']}g|F:{mac['fat']}g"""

    try:
        with st.spinner("🍛 Crafting your Indian nutrition plan..."):
            dp = ask(client,
                f"""You are India's top sports nutritionist. Create a detailed Indian meal plan.
Diet:{diet_pref}|Region:{region}|Conditions:{cond}|Goal:{goal}
Targets:{mac['cals']}kcal|P:{mac['pro']}g|C:{mac['carb']}g|F:{mac['fat']}g

Format:
🌅 EARLY MORNING (6-7 AM)
🍳 BREAKFAST (8-9 AM)
🥗 MID-MORNING SNACK (11 AM)
🍛 LUNCH (1-2 PM)
☕ EVENING SNACK (4-5 PM)
🏋️ PRE/POST WORKOUT NUTRITION
🌙 DINNER (7-8 PM)
💧 HYDRATION & SUPPLEMENTS (desi alternatives)

For each meal: exact Indian foods with grams + estimated macros + prep notes.
Use: dal, sabzi, roti, rice, idli, dosa, poha, upma, rajma, chole, paneer, sprouts, makhana, chaas, lassi, etc.
Strictly respect {diet_pref}. Adapt for conditions: {cond}.""", prof)

        with st.spinner("💪 Building your training program..."):
            fp = ask(client,
                f"""You are India's top fitness coach. Build a 7-day training program.
Goal:{goal}|Activity:{activity}|Age:{age}|Weight:{weight}kg|Conditions:{cond}

For EACH day include:
Day + workout type OR Rest/Active Recovery
Warm-up (include Surya Namaskar variants)
Main workout: exercise | sets×reps | rest | RPE
Cool-down: yoga asanas (with Sanskrit names)
Daily Ayurvedic recovery tip

End with: 4-week progressive overload plan + home/bodyweight alternatives.
Adapt for conditions: {cond}.""", prof)

        st.session_state.dp   = dp
        st.session_state.fp   = fp
        st.session_state.done = True
        st.session_state.qa   = []
        st.success("✅ Your APEX Indian Health Plan is ready!")
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")


# ─── Show Plans ────────────────────────────────────────────────────────────────
if st.session_state.done:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-icon">📋</div><div class="sec-title">Your APEX Protocol</div><div class="sec-line"></div></div>', unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["🍛  INDIAN DIET PLAN", "💪  TRAINING PROGRAM", "💬  AI HEALTH ASSISTANT"])

    with t1:
        st.markdown(f"""<div class="pblock ora">
        <div class="pblock-title">🍛 Personalized Indian Nutrition Protocol</div>
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
            {chip_html(diet_pref,'chip-s')} {chip_html(region,'chip-o')}
            {chip_html(f"{mac['cals']} KCAL",'chip-t')} {chip_html(goal.upper(),'chip-g')}
        </div></div>""", unsafe_allow_html=True)
        r1,r2,r3 = st.columns(3)
        r1.metric("Daily Protein", f"{mac['pro']}g")
        r2.metric("Daily Carbs",   f"{mac['carb']}g")
        r3.metric("Daily Fats",    f"{mac['fat']}g")
        with st.expander("🍛 View Full Indian Diet Plan", expanded=True):
            st.markdown(st.session_state.dp)
        st.markdown("""<div class="pblock ora" style="margin-top:1rem;">
        <div class="pblock-title">🌿 Indian Nutrition Wisdom</div>
        <div style="font-size:0.84rem;color:#8892A4;line-height:1.9;">
        🫙 Use cold-pressed oils — mustard, coconut or groundnut instead of refined oil<br>
        🌾 Choose whole grains — multigrain atta, hand-pounded rice, millets (ragi, jowar, bajra)<br>
        🥛 Daily homemade curd or chaas — best probiotic for gut health &amp; digestion<br>
        🌿 Haldi + kali mirch in every meal — powerful anti-inflammatory combination<br>
        🕗 Follow circadian eating — largest meal at lunch, lightest dinner before 8 PM
        </div></div>""", unsafe_allow_html=True)

    with t2:
        st.markdown(f"""<div class="pblock tea">
        <div class="pblock-title">⚡ 7-Day Performance Program</div>
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
            {chip_html(goal.upper(),'chip-t')} {chip_html('7-DAY PLAN','chip-g')} {chip_html(activity.split('(')[0].strip().upper(),'chip-s')}
        </div></div>""", unsafe_allow_html=True)
        with st.expander("🏋️ View Full Training Program", expanded=True):
            st.markdown(st.session_state.fp)
        st.markdown("""<div class="pblock tea" style="margin-top:1rem;">
        <div class="pblock-title">🌿 Ayurvedic Recovery Protocol</div>
        <div style="font-size:0.84rem;color:#8892A4;line-height:1.9;">
        🥛 Haldi doodh (golden milk) post-workout — curcumin reduces muscle inflammation<br>
        🌿 Ashwagandha 300–500mg with warm milk — lowers cortisol, boosts natural testosterone<br>
        💆 Abhyanga (sesame oil self-massage) on rest days — reduces DOMS &amp; improves circulation<br>
        🧘 Anulom-Vilom pranayama 10 min daily — improves VO₂ max and mental clarity<br>
        😴 Sleep before 10:30 PM — aligns with natural melatonin for optimal recovery
        </div></div>""", unsafe_allow_html=True)

    with t3:
        st.markdown("""<div class="pblock ora" style="margin-bottom:1.1rem;">
        <div class="pblock-title">🤖 APEX AI Health Assistant</div>
        <div style="font-size:0.83rem;color:#8892A4;line-height:1.65;">
            Ask anything about your Indian diet, workout, Ayurvedic alternatives, ingredient swaps,
            festival eating, travel meals, or goal advice. APEX knows your complete profile.
        </div></div>""", unsafe_allow_html=True)

        with st.form("qa_form", clear_on_submit=True):
            qc1, qc2 = st.columns([5,1])
            with qc1:
                q = st.text_input(
                    "",
                    placeholder="e.g. Can I have biryani on cheat day? What to eat during Navratri fast?",
                    label_visibility="collapsed"
                )
            with qc2:
                ask_btn = st.form_submit_button("ASK →", use_container_width=True)

        if ask_btn and q:
            with st.spinner("🧠 Thinking..."):
                try:
                    ctx = f"Diet Plan:\n{st.session_state.dp}\n\nFitness Plan:\n{st.session_state.fp}"
                    ans = ask(client,
                        "You are APEX — India's top AI health advisor. Give specific practical advice using Indian foods and fitness context. Suggest desi alternatives and Ayurvedic tips where relevant. Reference the user's exact plan.",
                        f"{ctx}\n\nUser Question: {q}")
                    st.session_state.qa.append((q, ans))
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.qa:
            for i, (question, answer) in enumerate(reversed(st.session_state.qa)):
                n = len(st.session_state.qa) - i
                st.markdown(f"""
                <div class="cbubble cu"><div class="clbl">You · #{n}</div>{question}</div>
                <div class="cbubble ca"><div class="clbl">⚡ APEX AI</div>{answer}</div>
                """, unsafe_allow_html=True)


# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 0.5rem;">
    <div style="height:3px;width:180px;margin:0 auto 1rem;border-radius:100px;opacity:0.45;
         background:linear-gradient(90deg,transparent,#FF9933,#fff,#138808,transparent);"></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.52rem;letter-spacing:0.3em;color:#3D4A5C;">
        APEX · MADE FOR INDIA 🇮🇳 · GROQ + LLaMA 3.3 70B &nbsp;|&nbsp; FOR INFORMATIONAL USE ONLY · NOT MEDICAL ADVICE
    </div>
</div>
""", unsafe_allow_html=True)
