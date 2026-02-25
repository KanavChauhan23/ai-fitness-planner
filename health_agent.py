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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --saffron: #FF9933;
    --saffron-dim: rgba(255,153,51,0.15);
    --green-india: #138808;
    --green-neon: #00e676;
    --gold: #FFD700;
    --teal: #00BCD4;
    --bg-base: #050810;
    --bg-card: rgba(10,15,30,0.97);
    --border-saffron: rgba(255,153,51,0.3);
    --border-teal: rgba(0,188,212,0.25);
    --text-bright: #F0F4FF;
    --text-mid: #8892A4;
    --text-dim: #3D4A5C;
}

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main .block-container { padding: 1.25rem 2rem 4rem; max-width: 1380px; }
.stApp { background: var(--bg-base); color: var(--text-bright); }
.stApp::before {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse 70% 45% at 10% 0%, rgba(255,153,51,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 55% 40% at 90% 100%, rgba(0,188,212,0.06) 0%, transparent 55%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(255,215,0,0.03) 0%, transparent 60%);
}
#MainMenu, footer, header { visibility: hidden; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(255,153,51,0.3); border-radius: 4px; }

/* Sidebar */
section[data-testid="stSidebar"] { background: rgba(5,8,20,0.99) !important; border-right: 1px solid rgba(255,153,51,0.12) !important; }

/* Hero */
.hero-wrap { padding: 2rem 1rem 1rem; text-align: center; }
.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 0.5rem;
    font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.35em;
    color: var(--saffron); border: 1px solid var(--border-saffron);
    padding: 0.22rem 0.85rem; border-radius: 100px; background: var(--saffron-dim);
    margin-bottom: 1rem; text-transform: uppercase;
}
.hero-title {
    font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: clamp(2.2rem, 5vw, 3.8rem); line-height: 1.05; letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 0%, var(--saffron) 40%, var(--gold) 70%, var(--teal) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.6rem;
}
.hero-sub { color: var(--text-mid); font-size: 0.92rem; font-weight: 300; max-width: 520px; margin: 0 auto 1.5rem; line-height: 1.6; }
.tricolor-line { height: 3px; border-radius: 100px; margin: 0 auto 1.5rem; width: 120px; background: linear-gradient(90deg, #FF9933 33%, #ffffff 33% 66%, #138808 66%); }

/* Section header */
.sec-head { display: flex; align-items: center; gap: 0.7rem; margin: 2rem 0 1.1rem; padding-bottom: 0.6rem; border-bottom: 1px solid rgba(255,153,51,0.1); }
.sec-head-icon { width: 34px; height: 34px; border-radius: 9px; background: linear-gradient(135deg, rgba(255,153,51,0.18), rgba(0,188,212,0.12)); border: 1px solid var(--border-saffron); display: flex; align-items: center; justify-content: center; font-size: 0.95rem; flex-shrink: 0; }
.sec-head-title { font-family: 'Syne', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.18em; color: var(--text-bright); text-transform: uppercase; }
.sec-head-line { flex: 1; height: 1px; background: linear-gradient(90deg, rgba(255,153,51,0.2), transparent); }

/* Input cards */
.input-group { background: var(--bg-card); border: 1px solid rgba(255,153,51,0.12); border-radius: 14px; padding: 1.5rem; position: relative; overflow: hidden; }
.input-group::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--saffron), var(--gold), var(--teal)); opacity: 0.6; }

/* Metric cards */
.m-card { background: var(--bg-card); border-radius: 14px; padding: 1.1rem 1.2rem; position: relative; overflow: hidden; border: 1px solid rgba(255,153,51,0.12); }
.m-card:hover { border-color: rgba(255,153,51,0.35); }
.m-card-glow { position: absolute; top: -30px; right: -30px; width: 80px; height: 80px; border-radius: 50%; opacity: 0.12; filter: blur(20px); }
.m-card-label { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; letter-spacing: 0.22em; color: var(--text-mid); text-transform: uppercase; margin-bottom: 0.5rem; }
.m-card-value { font-family: 'Syne', sans-serif; font-size: 1.85rem; font-weight: 800; line-height: 1; display: flex; align-items: baseline; gap: 0.3rem; }
.m-card-unit { font-size: 0.78rem; color: var(--text-mid); font-family: 'DM Sans', sans-serif; font-weight: 400; }
.m-card-sub { font-size: 0.75rem; color: var(--text-mid); margin-top: 0.4rem; }

/* Chips/badges */
.chip { display: inline-flex; align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; padding: 0.18rem 0.6rem; border-radius: 100px; font-weight: 500; letter-spacing: 0.06em; white-space: nowrap; }
.chip-saffron { background: rgba(255,153,51,0.12); color: #FF9933; border: 1px solid rgba(255,153,51,0.3); }
.chip-green   { background: rgba(0,230,118,0.1);  color: #00e676; border: 1px solid rgba(0,230,118,0.3); }
.chip-teal    { background: rgba(0,188,212,0.1);  color: #00BCD4; border: 1px solid rgba(0,188,212,0.25); }
.chip-gold    { background: rgba(255,215,0,0.1);  color: #FFD700; border: 1px solid rgba(255,215,0,0.3); }
.chip-red     { background: rgba(255,82,82,0.1);  color: #ff5252; border: 1px solid rgba(255,82,82,0.3); }

/* Macro bars */
.macro-bar-wrap { margin: 0.55rem 0; }
.macro-bar-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem; }
.macro-bar-name { font-size: 0.78rem; color: var(--text-bright); font-weight: 500; }
.macro-bar-val { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--text-mid); }
.macro-bar-track { height: 5px; background: rgba(255,255,255,0.06); border-radius: 100px; overflow: hidden; }
.macro-bar-fill { height: 100%; border-radius: 100px; }

/* Plan blocks */
.plan-block { background: var(--bg-card); border-radius: 16px; padding: 1.5rem 1.75rem; margin-bottom: 1.25rem; position: relative; overflow: hidden; border: 1px solid rgba(255,153,51,0.15); }
.plan-block::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.plan-block.orange::before { background: linear-gradient(90deg, transparent, #FF9933, #FFD700, transparent); }
.plan-block.teal-b::before { background: linear-gradient(90deg, transparent, #00BCD4, transparent); }
.plan-block-title { font-family: 'Syne', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; margin-bottom: 0.9rem; }
.plan-block.orange .plan-block-title { color: #FF9933; }
.plan-block.teal-b .plan-block-title { color: #00BCD4; }

/* Chat */
.chat-bubble { padding: 0.9rem 1.1rem; border-radius: 12px; margin-bottom: 0.8rem; line-height: 1.65; font-size: 0.88rem; }
.chat-user { background: rgba(255,153,51,0.07); border-left: 3px solid #FF9933; }
.chat-ai   { background: rgba(0,188,212,0.06);  border-left: 3px solid #00BCD4; }
.chat-lbl  { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; letter-spacing: 0.15em; opacity: 0.55; margin-bottom: 0.4rem; text-transform: uppercase; }

/* Sidebar */
.sb-logo { text-align: center; padding: 1.5rem 1rem 1rem; border-bottom: 1px solid rgba(255,153,51,0.1); margin-bottom: 1.25rem; }
.sb-logo-name { font-family: 'Syne', sans-serif; font-size: 1.15rem; font-weight: 800; letter-spacing: 0.15em; background: linear-gradient(135deg, #FF9933, #FFD700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.sb-logo-sub { font-family: 'JetBrains Mono', monospace; font-size: 0.52rem; letter-spacing: 0.3em; color: var(--text-dim); margin-top: 0.2rem; }
.sb-stat { padding: 0.7rem 1rem; background: rgba(255,153,51,0.05); border: 1px solid rgba(255,153,51,0.1); border-radius: 10px; margin-bottom: 0.55rem; display: flex; align-items: center; justify-content: space-between; }
.sb-stat-label { font-size: 0.75rem; color: var(--text-mid); }
.sb-stat-val   { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #FF9933; font-weight: 600; }
.sb-tip { background: rgba(0,188,212,0.05); border: 1px solid rgba(0,188,212,0.15); border-radius: 10px; padding: 0.75rem 0.9rem; margin-bottom: 0.55rem; font-size: 0.77rem; color: var(--text-mid); line-height: 1.5; }
.sb-tip strong { color: #00BCD4; display: block; font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 0.2rem; font-family: 'JetBrains Mono', monospace; }
.sb-section-label { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; letter-spacing: 0.25em; color: var(--text-dim); text-transform: uppercase; margin: 1.1rem 0 0.6rem; padding: 0 1rem; }

/* Streamlit overrides */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,153,51,0.2) !important;
    border-radius: 10px !important; color: #F0F4FF !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 0.95rem !important;
    padding: 0.6rem 0.9rem !important;
}
.stTextInput > div > div > input:focus { border-color: rgba(255,153,51,0.55) !important; box-shadow: 0 0 0 3px rgba(255,153,51,0.1) !important; }
.stSelectbox > div > div, .stMultiSelect > div > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,153,51,0.2) !important; border-radius: 10px !important; color: #F0F4FF !important; }
.stButton > button {
    background: linear-gradient(135deg, rgba(255,153,51,0.18), rgba(255,215,0,0.12)) !important;
    border: 1px solid rgba(255,153,51,0.45) !important; color: #FF9933 !important;
    font-family: 'Syne', sans-serif !important; font-size: 0.78rem !important; font-weight: 700 !important;
    letter-spacing: 0.15em !important; border-radius: 10px !important; padding: 0.65rem 1.2rem !important;
    transition: all 0.25s ease !important; width: 100% !important;
}
.stButton > button:hover { background: linear-gradient(135deg, rgba(255,153,51,0.32), rgba(255,215,0,0.22)) !important; box-shadow: 0 0 24px rgba(255,153,51,0.25) !important; transform: translateY(-1px) !important; }
label, .stSelectbox label, .stTextInput label, .stMultiSelect label { color: #8892A4 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.025) !important; border-radius: 12px !important; padding: 4px !important; gap: 3px !important; }
.stTabs [data-baseweb="tab"] { border-radius: 9px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 500 !important; color: #8892A4 !important; padding: 0.5rem 1.1rem !important; }
.stTabs [aria-selected="true"] { background: rgba(255,153,51,0.14) !important; color: #FF9933 !important; }
.stMetric { background: rgba(255,153,51,0.04); border: 1px solid rgba(255,153,51,0.1); border-radius: 10px; padding: 0.75rem 1rem !important; }
[data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; color: #FF9933 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: #8892A4 !important; }
.stExpander { background: var(--bg-card) !important; border: 1px solid rgba(255,153,51,0.15) !important; border-radius: 12px !important; }
div[data-testid="stExpander"] div[role="button"] p { font-family: 'Syne', sans-serif !important; font-size: 0.82rem !important; font-weight: 700 !important; }
[data-baseweb="tag"] { background: rgba(255,153,51,0.15) !important; border-color: rgba(255,153,51,0.3) !important; }
hr { border-color: rgba(255,153,51,0.1) !important; }
div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def calculate_bmi(weight_kg, height_cm):
    if height_cm <= 0: return 0.0, "N/A", "saffron"
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:   return round(bmi,1), "Underweight", "teal"
    elif bmi < 23:   return round(bmi,1), "Healthy ✓", "green"
    elif bmi < 27.5: return round(bmi,1), "Overweight", "saffron"
    else:            return round(bmi,1), "Obese", "red"

def calculate_tdee(weight_kg, height_cm, age, sex, activity):
    bmr = (10*weight_kg + 6.25*height_cm - 5*age + 5) if sex == "Male" else (10*weight_kg + 6.25*height_cm - 5*age - 161)
    m = {"Sedentary (Desk job)": 1.2, "Lightly Active (Walk 1-3 days)": 1.375,
         "Moderately Active (Exercise 3-5 days)": 1.55, "Very Active (Hard exercise 6-7 days)": 1.725,
         "Athlete / Physical Labour": 1.9}
    return round(bmr), round(bmr * m.get(activity, 1.55))

def ideal_weight(height_cm, sex):
    if height_cm < 152.4: return 50 if sex == "Male" else 45.5
    extra = (height_cm - 152.4) / 2.54
    return round(50 + 2.3*extra, 1) if sex == "Male" else round(45.5 + 2.3*extra, 1)

def macro_split(tdee, goal):
    if goal == "Weight Loss":            cals, p, f, c = tdee-400, 0.35, 0.30, 0.35
    elif goal == "Muscle Gain":          cals, p, f, c = tdee+350, 0.30, 0.25, 0.45
    elif goal == "Strength Training":    cals, p, f, c = tdee+200, 0.32, 0.28, 0.40
    elif goal == "Athletic Performance": cals, p, f, c = tdee+300, 0.28, 0.25, 0.47
    else:                                cals, p, f, c = tdee,     0.25, 0.30, 0.45
    return {"cals": round(cals), "protein": round(cals*p/4), "fat": round(cals*f/9), "carbs": round(cals*c/4)}

def macrobar(label, val, max_v, color):
    pct = min(100, round(val/max_v*100))
    return f"""<div class="macro-bar-wrap">
    <div class="macro-bar-top"><span class="macro-bar-name">{label}</span><span class="macro-bar-val">{val}g</span></div>
    <div class="macro-bar-track"><div class="macro-bar-fill" style="width:{pct}%;background:{color};"></div></div>
    </div>"""

def chip(text, kind="saffron"):
    return f'<span class="chip chip-{kind}">{text}</span>'

def safe_float(val, default):
    try: return float(str(val).strip())
    except: return default

def ask_groq(client, system_msg, user_msg):
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"system","content":system_msg},{"role":"user","content":user_msg}],
        max_tokens=2500, temperature=0.7
    )
    return resp.choices[0].message.content


# ─── Session State ─────────────────────────────────────────────────────────────
for k, v in {"diet_plan":None,"fit_plan":None,"qa":[],"generated":False}.items():
    if k not in st.session_state: st.session_state[k] = v

groq_key = st.secrets.get("GROQ_API_KEY", "")


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div style="font-size:1.8rem;margin-bottom:0.3rem;">🏋️</div>
        <div class="sb-logo-name">⚡ APEX</div>
        <div class="sb-logo-sub">INDIAN HEALTH INTELLIGENCE</div>
        <div style="height:3px;border-radius:100px;background:linear-gradient(90deg,#FF9933,#fff,#138808);margin:0.75rem auto 0;width:80px;"></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label">System Status</div>', unsafe_allow_html=True)
    if groq_key:
        st.markdown('<div class="sb-stat"><span class="sb-stat-label">🟢 AI Engine</span><span class="sb-stat-val">ONLINE</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-stat"><span class="sb-stat-label">⚡ Model</span><span class="sb-stat-val">LLaMA 3.3 70B</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-stat"><span class="sb-stat-label">🇮🇳 Diet Mode</span><span class="sb-stat-val">INDIAN</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sb-stat" style="border-color:rgba(255,82,82,0.3)"><span class="sb-stat-label">🔴 AI Engine</span><span class="sb-stat-val" style="color:#ff5252">OFFLINE</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-section-label">Daily Wellness Tips</div>', unsafe_allow_html=True)
    for title, tip in [
        ("💧 Hydration", "Start with warm water + lemon + jeera. Aim for 8–10 glasses daily."),
        ("🌅 Morning Ritual", "10 rounds of Surya Namaskar burns ~100 kcal and boosts metabolism."),
        ("🍛 Meal Timing", "Largest meal at lunch (1–2 PM). Keep dinner light before 8 PM."),
        ("🌿 Ayurveda", "Haldi + kali mirch daily reduces inflammation. Ashwagandha builds strength."),
        ("😴 Recovery", "7–9 hrs sleep regulates cortisol, ghrelin and muscle repair hormones."),
    ]:
        st.markdown(f'<div class="sb-tip"><strong>{title}</strong>{tip}</div>', unsafe_allow_html=True)

    if st.session_state.generated:
        st.markdown('<div class="sb-section-label">Session</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sb-stat"><span class="sb-stat-label">📋 Plan</span><span class="sb-stat-val">ACTIVE</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sb-stat"><span class="sb-stat-label">💬 Q&A</span><span class="sb-stat-val">{len(st.session_state.qa)} chats</span></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 NEW SESSION"):
            for k in ["diet_plan","fit_plan","qa","generated"]:
                st.session_state[k] = None if k != "qa" else []
            st.session_state.generated = False
            st.rerun()


# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">🇮🇳 MADE FOR INDIA · POWERED BY GROQ AI</div>
    <h1 class="hero-title">APEX HEALTH PLANNER</h1>
    <p class="hero-sub">AI-crafted Indian diet & fitness plans calibrated to your unique body and goals</p>
    <div class="tricolor-line"></div>
</div>
""", unsafe_allow_html=True)

if not groq_key:
    st.error("⚠️ GROQ_API_KEY missing. Go to Streamlit Cloud → App Settings → Secrets and add: GROQ_API_KEY = \"gsk_...\"")
    st.stop()

client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")


# ─── Profile Inputs ────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-head-icon">👤</div><div class="sec-head-title">Your Biometric Profile</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="input-group">', unsafe_allow_html=True)
    age_in    = st.text_input("Age (years)", value="25", placeholder="e.g. 25")
    height_in = st.text_input("Height (cm)", value="170", placeholder="e.g. 170")
    sex       = st.selectbox("Biological Sex", ["Male", "Female", "Other"])
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="input-group">', unsafe_allow_html=True)
    weight_in = st.text_input("Weight (kg)", value="70", placeholder="e.g. 70")
    activity  = st.selectbox("Activity Level", [
        "Sedentary (Desk job)", "Lightly Active (Walk 1-3 days)",
        "Moderately Active (Exercise 3-5 days)", "Very Active (Hard exercise 6-7 days)",
        "Athlete / Physical Labour"
    ])
    diet_pref = st.selectbox("Diet Type", [
        "Non-Vegetarian", "Vegetarian", "Vegan", "Eggetarian",
        "Jain (No root vegetables)", "Sattvic", "Low Carb Indian", "Diabetic-friendly Indian"
    ])
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="input-group">', unsafe_allow_html=True)
    goal       = st.selectbox("Fitness Goal", [
        "Weight Loss", "Muscle Gain", "Stay Fit & Healthy",
        "Strength Training", "Endurance & Stamina", "Athletic Performance"
    ])
    conditions = st.multiselect("Health Conditions", [
        "None", "Diabetes (Type 2)", "Hypertension", "High Cholesterol",
        "PCOD/PCOS", "Thyroid", "Acidity / IBS", "Anemia", "Joint Pain / Arthritis"
    ], default=["None"])
    region     = st.selectbox("Regional Cuisine", [
        "North Indian", "South Indian", "East Indian (Bengali/Odia)",
        "West Indian (Gujarati/Marathi)", "Mixed / Pan India"
    ])
    st.markdown('</div>', unsafe_allow_html=True)

age    = int(safe_float(age_in, 25))
height = safe_float(height_in, 170)
weight = safe_float(weight_in, 70)


# ─── Biometric Dashboard ───────────────────────────────────────────────────────
bmi, bmi_cat, bmi_chip = calculate_bmi(weight, height)
bmr, tdee  = calculate_tdee(weight, height, age, sex, activity)
ideal_wt   = ideal_weight(height, sex)
macros     = macro_split(tdee, goal)
water_l    = round(weight * 0.033, 1)
wt_diff    = round(weight - ideal_wt, 1)
wt_label   = f"+{wt_diff} kg above" if wt_diff > 0 else f"{abs(wt_diff)} kg below" if wt_diff < 0 else "At ideal ✓"

st.markdown('<div class="sec-head"><div class="sec-head-icon">📊</div><div class="sec-head-title">Live Biometric Analysis</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)

color_map = {"saffron":"#FF9933","teal":"#00BCD4","gold":"#FFD700","green":"#00e676","red":"#ff5252"}
cards_data = [
    ("BMI · Asian Standard", bmi, "BMI", bmi_cat, bmi_chip),
    ("Basal Metabolic Rate", f"{bmr:,}", "kcal", "Resting burn", "teal"),
    ("Daily Calorie Target", f"{macros['cals']:,}", "kcal", goal[:15], "saffron"),
    ("Ideal Body Weight", ideal_wt, "kg", wt_label, "gold"),
    ("Daily Water", water_l, "litres", f"{round(water_l*4)} glasses", "teal"),
    ("Daily Protein", macros['protein'], "grams", "Muscle synthesis", "green"),
]
for col, (label, val, unit, sub, col_name) in zip(st.columns(6), cards_data):
    c = color_map.get(col_name, "#FF9933")
    with col:
        st.markdown(f"""<div class="m-card">
            <div class="m-card-glow" style="background:{c};"></div>
            <div class="m-card-label">{label}</div>
            <div class="m-card-value" style="color:{c};">{val}<span class="m-card-unit">{unit}</span></div>
            <div class="m-card-sub">{chip(sub, col_name)}</div>
        </div>""", unsafe_allow_html=True)


# ─── Macros ────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-head-icon">🧬</div><div class="sec-head-title">Macro Nutrition Targets</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)

ma1, ma2 = st.columns([3,1])
with ma1:
    st.markdown(f"""<div class="plan-block orange">
        <div class="plan-block-title">🎯 Daily Macro Targets · {macros['cals']:,} kcal</div>
        {macrobar('Protein', macros['protein'], 250, '#FF9933')}
        {macrobar('Carbohydrates', macros['carbs'], 350, '#00BCD4')}
        {macrobar('Fats', macros['fat'], 120, '#FFD700')}
    </div>""", unsafe_allow_html=True)

with ma2:
    prot_pct = round(macros['protein']*4/macros['cals']*100)
    carb_pct = round(macros['carbs']*4/macros['cals']*100)
    fat_pct  = round(macros['fat']*9/macros['cals']*100)
    st.markdown(f"""<div class="m-card" style="height:100%;">
        <div class="m-card-label">Split Ratio</div>
        <div style="margin-top:0.9rem;display:flex;flex-direction:column;gap:0.65rem;">
            <div style="display:flex;justify-content:space-between;"><span style="font-size:0.8rem;color:#FF9933">● Protein</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#F0F4FF;">{prot_pct}%</span></div>
            <div style="display:flex;justify-content:space-between;"><span style="font-size:0.8rem;color:#00BCD4">● Carbs</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#F0F4FF;">{carb_pct}%</span></div>
            <div style="display:flex;justify-content:space-between;"><span style="font-size:0.8rem;color:#FFD700">● Fats</span><span style="font-family:'JetBrains Mono',monospace;font-size:0.75rem;color:#F0F4FF;">{fat_pct}%</span></div>
        </div>
        <div style="margin-top:1rem;padding-top:0.75rem;border-top:1px solid rgba(255,153,51,0.1);font-size:0.72rem;color:#8892A4;">Based on {goal}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─── Generate ─────────────────────────────────────────────────────────────────
st.markdown('<div class="sec-head"><div class="sec-head-icon">⚡</div><div class="sec-head-title">Generate Your AI Plan</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)

_, gc, _ = st.columns([1,2,1])
with gc:
    gen = st.button("⚡ GENERATE MY APEX PLAN")

if gen:
    cond_str = ", ".join([c for c in conditions if c != "None"]) or "None"
    profile  = f"""Age:{age}|Sex:{sex}|Weight:{weight}kg|Height:{height}cm|BMI:{bmi}({bmi_cat})|BMR:{bmr}|TDEE:{tdee}|IdealWT:{ideal_wt}kg
Goal:{goal}|Activity:{activity}|Diet:{diet_pref}|Region:{region}|Conditions:{cond_str}
Macros:{macros['cals']}kcal|P:{macros['protein']}g|C:{macros['carbs']}g|F:{macros['fat']}g"""

    try:
        with st.spinner("🍛 Crafting your Indian nutrition plan..."):
            diet_plan = ask_groq(client,
                f"""You are India's top sports nutritionist. Create a complete Indian meal plan.
Diet: {diet_pref} | Region: {region} | Conditions: {cond_str} | Goal: {goal}
Targets: {macros['cals']} kcal | Protein:{macros['protein']}g | Carbs:{macros['carbs']}g | Fat:{macros['fat']}g

Format exactly as:
🌅 EARLY MORNING (6-7 AM): warm water with lemon/jeera, soaked almonds, tulsi chai etc.
🍳 BREAKFAST (8-9 AM): specific Indian dish with grams and macros
🥗 MID-MORNING (11 AM): light Indian snack
🍛 LUNCH (1-2 PM): dal + sabzi + roti/rice + salad with exact grams
☕ EVENING SNACK (4-5 PM): roasted chana/makhana/sprouts/chaas etc.
🏋️ PRE/POST WORKOUT: what to eat and when
🌙 DINNER (7-8 PM): light Indian meal with portions
💊 HYDRATION & SUPPLEMENTS: desi alternatives (haldi doodh, jeera water, etc.)

Use real Indian foods: dal, sabzi, roti, rice, idli, dosa, poha, upma, rajma, chole, paneer, sprouts, makhana, chaas, lassi, etc.
Give exact grams for each item. Respect {diet_pref} strictly. Adapt for {cond_str}.""",
                profile)

        with st.spinner("💪 Building your training program..."):
            fit_plan = ask_groq(client,
                f"""You are an elite Indian fitness coach. Create a 7-day training program.
Goal:{goal}|Activity:{activity}|Age:{age}|Weight:{weight}kg|Conditions:{cond_str}

For each day provide:
Day name + workout type (or rest/active recovery)
Warm-up: include Surya Namaskar where relevant
Main workout: exercise name, sets × reps, rest time, RPE (1-10)
Cool-down: yoga asanas (Shavasana, Balasana, etc.)
Recovery tip: haldi doodh, ashwagandha, abhyanga, pranayama etc.

Also include: 4-week progressive overload plan, home/bodyweight alternatives for gym exercises.
Adapt all exercises for conditions: {cond_str}.""",
                profile)

        st.session_state.diet_plan = diet_plan
        st.session_state.fit_plan  = fit_plan
        st.session_state.generated = True
        st.session_state.qa        = []
        st.success("✅ Your APEX Indian Health Plan is ready!")
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")


# ─── Show Plans ────────────────────────────────────────────────────────────────
if st.session_state.generated:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><div class="sec-head-icon">📋</div><div class="sec-head-title">Your APEX Protocol</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["🍛  INDIAN DIET PLAN", "💪  TRAINING PROGRAM", "💬  AI HEALTH ASSISTANT"])

    with t1:
        st.markdown(f"""<div class="plan-block orange">
            <div class="plan-block-title">🍛 Personalized Indian Nutrition Protocol</div>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">{chip(diet_pref,'saffron')} {chip(region,'gold')} {chip(f"{macros['cals']} KCAL",'teal')} {chip(goal.upper(),'green')}</div>
        </div>""", unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        r1.metric("Daily Protein", f"{macros['protein']}g")
        r2.metric("Daily Carbs",   f"{macros['carbs']}g")
        r3.metric("Daily Fats",    f"{macros['fat']}g")
        with st.expander("🍛 View Full Indian Diet Plan", expanded=True):
            st.markdown(st.session_state.diet_plan)
        st.markdown("""<div class="plan-block orange" style="margin-top:1rem;">
            <div class="plan-block-title">🌿 Indian Nutrition Wisdom</div>
            <div style="font-size:0.85rem;color:#8892A4;line-height:1.85;">
            🫙 Use cold-pressed oils — mustard, coconut, groundnut instead of refined oil<br>
            🌾 Choose whole grains — multigrain atta, hand-pounded rice, millets (ragi, jowar, bajra)<br>
            🥛 Homemade curd/chaas daily — probiotics for gut health and digestion<br>
            🌿 Haldi + kali mirch (turmeric + black pepper) in every meal — powerful anti-inflammatory<br>
            🕗 Eat with your circadian rhythm — largest meal at lunch, lightest before 8 PM
            </div></div>""", unsafe_allow_html=True)

    with t2:
        st.markdown(f"""<div class="plan-block teal-b">
            <div class="plan-block-title">⚡ 7-Day Training Program</div>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">{chip(goal.upper(),'teal')} {chip('7-DAY PLAN','green')} {chip(activity.split('(')[0].strip().upper(),'saffron')}</div>
        </div>""", unsafe_allow_html=True)
        with st.expander("🏋️ View Full Training Program", expanded=True):
            st.markdown(st.session_state.fit_plan)
        st.markdown("""<div class="plan-block teal-b" style="margin-top:1rem;">
            <div class="plan-block-title">🌿 Ayurvedic Recovery Protocol</div>
            <div style="font-size:0.85rem;color:#8892A4;line-height:1.85;">
            🥛 Haldi doodh (golden milk) post-workout — curcumin reduces muscle inflammation fast<br>
            🌿 Ashwagandha (300–500mg with warm milk) — reduces cortisol, boosts testosterone naturally<br>
            💆 Abhyanga (sesame oil self-massage) on rest days — reduces DOMS and improves circulation<br>
            🧘 Anulom-Vilom pranayama (10 min daily) — improves VO2 max and mental focus<br>
            😴 Sleep before 10:30 PM — aligns with natural melatonin cycle for optimal recovery
            </div></div>""", unsafe_allow_html=True)

    with t3:
        st.markdown("""<div class="plan-block orange" style="margin-bottom:1.25rem;">
            <div class="plan-block-title">🤖 APEX AI Health Assistant</div>
            <div style="font-size:0.84rem;color:#8892A4;line-height:1.6;">
            Ask anything about your Indian diet plan, workout, Ayurvedic alternatives, ingredient swaps, 
            festival eating, travel meals, or goal-specific advice. APEX knows your complete profile.
            </div></div>""", unsafe_allow_html=True)

        with st.form("qa_form", clear_on_submit=True):
            qc1, qc2 = st.columns([5,1])
            with qc1:
                q = st.text_input("", placeholder="e.g. What to eat during Navratri fast? Can I have biryani on cheat day?", label_visibility="collapsed")
            with qc2:
                ask_btn = st.form_submit_button("ASK →", use_container_width=True)

        if ask_btn and q:
            with st.spinner("🧠 Thinking..."):
                try:
                    ctx = f"Diet:\n{st.session_state.diet_plan}\n\nFitness:\n{st.session_state.fit_plan}"
                    ans = ask_groq(client,
                        "You are APEX — India's top AI health advisor. Give specific, practical advice using Indian food and fitness context. Suggest desi alternatives, Ayurvedic tips, and reference the user's exact plan.",
                        f"{ctx}\n\nQuestion: {q}")
                    st.session_state.qa.append((q, ans))
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        for i, (question, answer) in enumerate(reversed(st.session_state.qa)):
            n = len(st.session_state.qa) - i
            st.markdown(f"""
            <div class="chat-bubble chat-user"><div class="chat-lbl">You · #{n}</div>{question}</div>
            <div class="chat-bubble chat-ai"><div class="chat-lbl">⚡ APEX AI</div>{answer}</div>
            """, unsafe_allow_html=True)


# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2rem 0 0.5rem;">
    <div style="height:3px;border-radius:100px;background:linear-gradient(90deg,transparent,#FF9933,#fff,#138808,transparent);margin:0 auto 1rem;width:200px;opacity:0.5;"></div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;letter-spacing:0.3em;color:#3D4A5C;">
        APEX · MADE FOR INDIA 🇮🇳 · GROQ + LLaMA 3.3 70B &nbsp;|&nbsp; NOT MEDICAL ADVICE · CONSULT A QUALIFIED DOCTOR
    </div>
</div>
""", unsafe_allow_html=True)
