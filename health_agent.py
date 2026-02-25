import streamlit as st
import math
from agno.agent import Agent
from agno.models.xai import xAI

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="APEX · AI Health Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --neon-cyan: #00f5ff;
    --neon-green: #39ff14;
    --neon-purple: #bf00ff;
    --neon-orange: #ff6b00;
    --bg-deep: #010409;
    --bg-card: rgba(13, 17, 28, 0.95);
    --bg-glass: rgba(255,255,255,0.03);
    --border-glow: rgba(0, 245, 255, 0.25);
    --text-primary: #e8eaf0;
    --text-muted: #6b7280;
}

/* ── Global Reset ── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main .block-container { padding: 1.5rem 2rem 3rem; max-width: 1400px; }
.stApp { background: var(--bg-deep); color: var(--text-primary); }
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(0,245,255,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(191,0,255,0.05) 0%, transparent 60%),
        repeating-linear-gradient(0deg, transparent, transparent 80px, rgba(0,245,255,0.015) 80px, rgba(0,245,255,0.015) 81px),
        repeating-linear-gradient(90deg, transparent, transparent 80px, rgba(0,245,255,0.015) 80px, rgba(0,245,255,0.015) 81px);
    pointer-events: none;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.viewerBadge_container__1QSob { display: none; }

/* ── Hero Banner ── */
.apex-hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    position: relative;
}
.apex-hero .tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    color: var(--neon-cyan);
    border: 1px solid rgba(0,245,255,0.35);
    padding: 0.25rem 0.9rem;
    border-radius: 100px;
    margin-bottom: 1rem;
    background: rgba(0,245,255,0.04);
}
.apex-hero h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 900;
    letter-spacing: 0.05em;
    background: linear-gradient(135deg, #ffffff 0%, var(--neon-cyan) 50%, var(--neon-purple) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem;
    line-height: 1.1;
}
.apex-hero p {
    color: var(--text-muted);
    font-size: 1rem;
    font-weight: 300;
    max-width: 550px; margin: 0 auto;
}
.apex-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    margin: 1.5rem 0;
    opacity: 0.4;
}

/* ── Cards ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
}
.metric-card .label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.metric-card .value {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--neon-cyan);
    line-height: 1;
}
.metric-card .unit { font-size: 0.85rem; color: var(--text-muted); margin-left: 0.3rem; }
.metric-card .sub { font-size: 0.78rem; color: var(--text-muted); margin-top: 0.3rem; }

/* ── Status Badges ── */
.badge {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    padding: 0.2rem 0.65rem;
    border-radius: 100px;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-green  { background: rgba(57,255,20,0.12);  color: var(--neon-green);  border: 1px solid rgba(57,255,20,0.35); }
.badge-cyan   { background: rgba(0,245,255,0.12); color: var(--neon-cyan);  border: 1px solid rgba(0,245,255,0.3); }
.badge-orange { background: rgba(255,107,0,0.12); color: var(--neon-orange); border: 1px solid rgba(255,107,0,0.35); }
.badge-purple { background: rgba(191,0,255,0.12); color: #d966ff;           border: 1px solid rgba(191,0,255,0.35); }

/* ── Section Headers ── */
.section-header {
    display: flex; align-items: center; gap: 0.75rem;
    margin: 2rem 0 1rem;
}
.section-header .icon {
    width: 36px; height: 36px; border-radius: 8px;
    background: rgba(0,245,255,0.1);
    border: 1px solid rgba(0,245,255,0.3);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.section-header h2 {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: var(--text-primary);
    text-transform: uppercase;
    margin: 0;
}

/* ── Plan Output Cards ── */
.plan-card {
    background: var(--bg-card);
    border: 1px solid var(--border-glow);
    border-radius: 14px;
    padding: 1.5rem 1.75rem;
    margin-bottom: 1.25rem;
    position: relative;
}
.plan-card.green  { border-color: rgba(57,255,20,0.25); }
.plan-card.green::before  { background: linear-gradient(90deg, transparent, var(--neon-green), transparent); }
.plan-card.purple { border-color: rgba(191,0,255,0.25); }
.plan-card.purple::before { background: linear-gradient(90deg, transparent, #bf00ff, transparent); }
.plan-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
}
.plan-card h3 {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 0 0 1rem;
}
.plan-card.green h3 { color: var(--neon-green); }
.plan-card.purple h3 { color: #d966ff; }

/* ── Progress Bar ── */
.prog-wrap { margin: 0.5rem 0; }
.prog-label { display: flex; justify-content: space-between; margin-bottom: 0.3rem; font-size: 0.78rem; color: var(--text-muted); }
.prog-bar { height: 6px; background: rgba(255,255,255,0.07); border-radius: 100px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 100px; transition: width 1s ease; }

/* ── Chat ── */
.chat-msg { padding: 0.85rem 1.1rem; border-radius: 10px; margin-bottom: 0.75rem; font-size: 0.9rem; line-height: 1.6; }
.chat-user { background: rgba(0,245,255,0.07); border-left: 3px solid var(--neon-cyan); }
.chat-ai   { background: rgba(191,0,255,0.07); border-left: 3px solid #bf00ff; }
.chat-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.15em; margin-bottom: 0.4rem; opacity: 0.6; text-transform: uppercase; }

/* ── Streamlit Overrides ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,245,255,0.2) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: rgba(0,245,255,0.55) !important;
    box-shadow: 0 0 0 2px rgba(0,245,255,0.12) !important;
}
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(191,0,255,0.15)) !important;
    border: 1px solid rgba(0,245,255,0.4) !important;
    color: var(--neon-cyan) !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    border-radius: 8px !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,245,255,0.28), rgba(191,0,255,0.28)) !important;
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.2) !important;
    transform: translateY(-1px) !important;
}
.stSidebar { background: rgba(8,10,18,0.98) !important; border-right: 1px solid rgba(0,245,255,0.1) !important; }
.stSidebar [data-testid="stSidebarContent"] { padding: 1.5rem 1.25rem; }
label, .stSelectbox label, .stNumberInput label, .stTextInput label { color: #9ca3af !important; font-size: 0.8rem !important; font-family: 'JetBrains Mono', monospace !important; letter-spacing: 0.08em !important; }
.stAlert { border-radius: 10px !important; border-width: 1px !important; }
.stExpander { background: var(--bg-card) !important; border: 1px solid var(--border-glow) !important; border-radius: 12px !important; }
div[data-testid="stExpander"] div[role="button"] p { font-family: 'Orbitron', sans-serif !important; font-size: 0.8rem !important; letter-spacing: 0.1em !important; }
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.03) !important; border-radius: 10px !important; padding: 4px !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 500 !important; color: var(--text-muted) !important; }
.stTabs [aria-selected="true"] { background: rgba(0,245,255,0.12) !important; color: var(--neon-cyan) !important; }
hr { border-color: rgba(0,245,255,0.12) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Utility Functions ─────────────────────────────────────────────────────────
def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str, str]:
    if height_cm <= 0:
        return 0.0, "N/A", "cyan"
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:
        return bmi, "Underweight", "orange"
    elif bmi < 25:
        return bmi, "Normal", "green"
    elif bmi < 30:
        return bmi, "Overweight", "orange"
    else:
        return bmi, "Obese", "purple"

def calculate_tdee(weight_kg, height_cm, age, sex, activity_level) -> tuple[float, float]:
    """Returns (BMR, TDEE)"""
    if sex == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    multipliers = {
        "Sedentary": 1.2, "Lightly Active": 1.375,
        "Moderately Active": 1.55, "Very Active": 1.725, "Extremely Active": 1.9
    }
    tdee = bmr * multipliers.get(activity_level, 1.55)
    return round(bmr), round(tdee)

def calculate_ideal_weight(height_cm: float, sex: str) -> float:
    """Devine formula"""
    if height_cm < 152.4:
        return 50 if sex == "Male" else 45.5
    extra_inches = (height_cm - 152.4) / 2.54
    if sex == "Male":
        return round(50 + 2.3 * extra_inches, 1)
    return round(45.5 + 2.3 * extra_inches, 1)

def macro_split(tdee: float, goal: str) -> dict:
    if goal == "Lose Weight":
        cals = tdee - 400
        protein_g = round(cals * 0.35 / 4)
        fat_g     = round(cals * 0.30 / 9)
        carb_g    = round(cals * 0.35 / 4)
    elif goal == "Gain Muscle":
        cals = tdee + 350
        protein_g = round(cals * 0.30 / 4)
        fat_g     = round(cals * 0.25 / 9)
        carb_g    = round(cals * 0.45 / 4)
    elif goal == "Strength Training":
        cals = tdee + 200
        protein_g = round(cals * 0.32 / 4)
        fat_g     = round(cals * 0.28 / 9)
        carb_g    = round(cals * 0.40 / 4)
    else:
        cals = tdee
        protein_g = round(cals * 0.25 / 4)
        fat_g     = round(cals * 0.30 / 9)
        carb_g    = round(cals * 0.45 / 4)
    return {"calories": round(cals), "protein": protein_g, "fat": fat_g, "carbs": carb_g}

def progress_bar_html(label: str, value: int, max_val: int, color: str) -> str:
    pct = min(100, round(value / max_val * 100))
    return f"""
    <div class="prog-wrap">
        <div class="prog-label"><span>{label}</span><span>{value}g / {max_val}g</span></div>
        <div class="prog-bar"><div class="prog-fill" style="width:{pct}%;background:{color};"></div></div>
    </div>"""

def get_badge_html(text: str, color: str) -> str:
    return f'<span class="badge badge-{color}">{text}</span>'


# ─── Session State Init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "dietary_plan": None,
        "fitness_plan": None,
        "qa_pairs": [],
        "plans_generated": False,
        "macros": None,
        "tdee": None,
        "bmi": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.5rem;">
        <div style="font-family:'Orbitron',sans-serif;font-size:1.1rem;font-weight:900;
                    background:linear-gradient(135deg,#00f5ff,#bf00ff);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    letter-spacing:0.2em;">⚡ APEX</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;
                    color:#4b5563;letter-spacing:0.3em;margin-top:0.2rem;">
            AI HEALTH INTELLIGENCE v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;letter-spacing:0.2em;color:#6b7280;text-transform:uppercase;margin-bottom:0.5rem;">🔑 Authentication</div>', unsafe_allow_html=True)
    grok_api_key = st.text_input(
        "Grok API Key",
        type="password",
        placeholder="xai-••••••••••••••••",
        help="Get your key at console.x.ai"
    )
    if not grok_api_key:
        st.markdown("""
        <div style="background:rgba(255,107,0,0.08);border:1px solid rgba(255,107,0,0.3);
                    border-radius:8px;padding:0.75rem;margin:0.5rem 0;
                    font-size:0.78rem;color:#ff6b00;">
            ⚠️ API key required to activate AI systems
        </div>
        """, unsafe_allow_html=True)
        st.markdown("[→ Get Grok API Key](https://console.x.ai)", unsafe_allow_html=False)
    else:
        st.markdown('<div style="background:rgba(57,255,20,0.08);border:1px solid rgba(57,255,20,0.25);border-radius:8px;padding:0.65rem;font-size:0.78rem;color:#39ff14;margin:0.5rem 0;">✓ Systems Online</div>', unsafe_allow_html=True)

    st.divider()
    st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;letter-spacing:0.2em;color:#6b7280;text-transform:uppercase;margin-bottom:0.75rem;">⚙️ AI Model Config</div>', unsafe_allow_html=True)
    model_choice = st.selectbox("Model", ["grok-3-mini", "grok-3", "grok-2-1212"], help="Grok model to use")
    temperature  = st.slider("Creativity", 0.0, 1.0, 0.7, 0.05, help="Higher = more creative plans")

    st.divider()
    if st.session_state.plans_generated:
        st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;letter-spacing:0.2em;color:#6b7280;text-transform:uppercase;margin-bottom:0.75rem;">📊 Session Stats</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="badge badge-cyan">PLAN ACTIVE</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.78rem;color:#6b7280;margin-top:0.5rem;">{len(st.session_state.qa_pairs)} Q&A exchanges logged</div>', unsafe_allow_html=True)
        if st.button("🔄 RESET SESSION"):
            for k in ["dietary_plan","fitness_plan","qa_pairs","plans_generated","macros","tdee","bmi"]:
                st.session_state[k] = None if k not in ["qa_pairs"] else []
            st.session_state.plans_generated = False
            st.rerun()


# ─── Hero Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="apex-hero">
    <div class="tag">POWERED BY GROK AI · NEXT-GEN HEALTH INTELLIGENCE</div>
    <h1>APEX HEALTH PLANNER</h1>
    <p>Precision-engineered dietary and fitness protocols calibrated to your unique biometric profile</p>
</div>
<div class="apex-divider"></div>
""", unsafe_allow_html=True)

if not grok_api_key:
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;color:#4b5563;
                font-family:'DM Sans',sans-serif;font-size:0.9rem;">
        Enter your Grok API key in the sidebar to activate the AI systems.
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─── Initialize Model ──────────────────────────────────────────────────────────
try:
    grok_model = xAI(id=model_choice, api_key=grok_api_key)
except Exception as e:
    st.error(f"Failed to initialize Grok model: {e}")
    st.stop()


# ─── PROFILE INPUT SECTION ────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="icon">👤</div>
    <h2>Biometric Profile</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    age    = st.number_input("AGE", min_value=10, max_value=100, value=28, step=1)
    height = st.number_input("HEIGHT (cm)", min_value=100.0, max_value=250.0, value=175.0, step=0.5)
    sex    = st.selectbox("BIOLOGICAL SEX", ["Male", "Female", "Other"])

with col2:
    weight   = st.number_input("WEIGHT (kg)", min_value=20.0, max_value=300.0, value=75.0, step=0.5)
    activity = st.selectbox("ACTIVITY LEVEL", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
    dietary_pref = st.selectbox("DIETARY PREFERENCE", ["No Restriction", "Vegetarian", "Vegan", "Keto", "Paleo", "Mediterranean", "Gluten Free", "Low Carb", "Dairy Free"])

with col3:
    fitness_goal = st.selectbox("FITNESS GOAL", ["Lose Weight", "Gain Muscle", "Endurance", "Stay Fit", "Strength Training", "Athletic Performance"])
    health_conditions = st.multiselect("HEALTH CONDITIONS", ["None", "Diabetes", "Hypertension", "High Cholesterol", "PCOS", "Thyroid Issues", "Joint Pain"], default=["None"])
    supplements = st.multiselect("CURRENT SUPPLEMENTS", ["None", "Protein Powder", "Creatine", "Omega-3", "Vitamins D/B12", "Pre-workout"], default=["None"])


# ─── Live Biometric Dashboard ─────────────────────────────────────────────────
bmi, bmi_category, bmi_color = calculate_bmi(weight, height)
bmr, tdee = calculate_tdee(weight, height, age, sex, activity)
ideal_wt  = calculate_ideal_weight(height, sex)
macros    = macro_split(tdee, fitness_goal)
wt_diff   = round(weight - ideal_wt, 1)
wt_status = f"+{wt_diff} kg above ideal" if wt_diff > 0 else f"{abs(wt_diff)} kg below ideal" if wt_diff < 0 else "At ideal weight"

st.markdown("""
<div class="section-header">
    <div class="icon">📊</div>
    <h2>Live Biometric Analysis</h2>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Body Mass Index</div>
        <div class="value">{bmi:.1f}<span class="unit">BMI</span></div>
        <div class="sub">{get_badge_html(bmi_category, bmi_color)}</div>
    </div>""", unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Basal Metabolic Rate</div>
        <div class="value">{bmr:,}<span class="unit">kcal</span></div>
        <div class="sub" style="color:#6b7280">Resting energy expenditure</div>
    </div>""", unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Daily Energy Target</div>
        <div class="value">{macros['calories']:,}<span class="unit">kcal</span></div>
        <div class="sub">{get_badge_html(fitness_goal.upper(), 'cyan')}</div>
    </div>""", unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Ideal Body Weight</div>
        <div class="value">{ideal_wt}<span class="unit">kg</span></div>
        <div class="sub" style="color:#6b7280">{wt_status}</div>
    </div>""", unsafe_allow_html=True)

with m5:
    water_l = round(weight * 0.033, 1)
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">Daily Water Intake</div>
        <div class="value">{water_l}<span class="unit">L</span></div>
        <div class="sub" style="color:#6b7280">{round(water_l * 4)} glasses of 250ml</div>
    </div>""", unsafe_allow_html=True)


# ─── Macro Breakdown ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="icon">🧬</div>
    <h2>Macro Nutrient Protocol</h2>
</div>
""", unsafe_allow_html=True)

mcc1, mcc2 = st.columns([3, 1])
with mcc1:
    st.markdown(f"""
    <div class="plan-card green">
        <h3>🎯 Target Macro Distribution · {macros['calories']:,} kcal/day</h3>
        {progress_bar_html('Protein', macros['protein'], 250, '#39ff14')}
        {progress_bar_html('Carbohydrates', macros['carbs'], 350, '#00f5ff')}
        {progress_bar_html('Fats', macros['fat'], 120, '#bf00ff')}
    </div>""", unsafe_allow_html=True)

with mcc2:
    prot_pct = round(macros['protein'] * 4 / macros['calories'] * 100)
    carb_pct = round(macros['carbs'] * 4 / macros['calories'] * 100)
    fat_pct  = round(macros['fat'] * 9 / macros['calories'] * 100)
    st.markdown(f"""
    <div class="metric-card" style="height:100%;">
        <div class="label">Split Ratio</div>
        <div style="margin-top:0.75rem;display:flex;flex-direction:column;gap:0.5rem;">
            <div style="display:flex;justify-content:space-between;font-size:0.82rem;">
                <span style="color:#39ff14">● Protein</span><span style="font-family:'JetBrains Mono',monospace;color:#e8eaf0">{prot_pct}%</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.82rem;">
                <span style="color:#00f5ff">● Carbs</span><span style="font-family:'JetBrains Mono',monospace;color:#e8eaf0">{carb_pct}%</span>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.82rem;">
                <span style="color:#bf00ff">● Fats</span><span style="font-family:'JetBrains Mono',monospace;color:#e8eaf0">{fat_pct}%</span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='apex-divider'></div>", unsafe_allow_html=True)


# ─── Generate Plans ────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
    <div class="icon">⚡</div>
    <h2>AI Plan Generation</h2>
</div>
""", unsafe_allow_html=True)

gen_col1, gen_col2, gen_col3 = st.columns([1, 2, 1])
with gen_col2:
    generate_clicked = st.button("⚡ GENERATE MY APEX PLAN", use_container_width=True)

if generate_clicked:
    conditions_str   = ", ".join([c for c in health_conditions if c != "None"]) or "None"
    supplements_str  = ", ".join([s for s in supplements if s != "None"]) or "None"
    user_profile = f"""
BIOMETRIC PROFILE:
- Age: {age} years | Sex: {sex}
- Weight: {weight} kg | Height: {height} cm
- BMI: {bmi:.1f} ({bmi_category})
- BMR: {bmr} kcal/day | TDEE: {tdee} kcal/day
- Ideal Weight: {ideal_wt} kg

GOALS & PREFERENCES:
- Primary Goal: {fitness_goal}
- Activity Level: {activity}
- Dietary Preference: {dietary_pref}
- Health Conditions: {conditions_str}
- Current Supplements: {supplements_str}

MACRO TARGETS:
- Daily Calories: {macros['calories']} kcal
- Protein: {macros['protein']}g | Carbs: {macros['carbs']}g | Fats: {macros['fat']}g
"""

    with st.spinner("🧠 APEX AI analyzing your biometric data..."):
        try:
            dietary_agent = Agent(
                name="APEX Nutrition Scientist",
                role="Elite sports nutritionist and dietitian",
                model=grok_model,
                instructions=[
                    f"You are an elite nutrition scientist. Create a highly detailed, personalized meal plan.",
                    f"The user's dietary preference is: {dietary_pref}. Strictly respect this.",
                    "Format the meal plan clearly with: Pre-Workout, Breakfast, Mid-Morning Snack, Lunch, Afternoon Snack, Post-Workout, Dinner, Evening Snack (if needed).",
                    f"Target macros: {macros['calories']} kcal, {macros['protein']}g protein, {macros['carbs']}g carbs, {macros['fat']}g fat.",
                    "For each meal, list: food items with portions (grams), estimated macros, and preparation notes.",
                    "Include: hydration protocol, meal timing recommendations, and supplement timing if applicable.",
                    f"Account for health conditions: {conditions_str}. Avoid contraindicated foods.",
                    "Be specific, scientific, and actionable. No vague advice.",
                ]
            )

            fitness_agent = Agent(
                name="APEX Performance Coach",
                role="Elite strength and conditioning coach",
                model=grok_model,
                instructions=[
                    "You are an elite performance coach. Create a science-backed weekly training program.",
                    f"Goal: {fitness_goal} | Activity Level: {activity}.",
                    "Provide a 7-day plan: include rest days, active recovery, and training sessions.",
                    "For each workout: warm-up (5-10 min), main exercises with sets/reps/rest/RPE, cool-down.",
                    "Include: progressive overload strategy, deload week guidance, and injury prevention notes.",
                    f"Adapt for health conditions: {conditions_str}. Avoid contraindicated movements.",
                    "Add performance metrics to track (e.g., 1RM estimates, VO2 max indicators).",
                    "Be specific with form cues and technique notes for key lifts.",
                ]
            )

            with st.spinner("🍽️ Generating nutrition protocol..."):
                dietary_response = dietary_agent.run(user_profile)

            with st.spinner("💪 Generating training program..."):
                fitness_response = fitness_agent.run(user_profile)

            st.session_state.dietary_plan  = dietary_response.content
            st.session_state.fitness_plan  = fitness_response.content
            st.session_state.plans_generated = True
            st.session_state.macros = macros
            st.session_state.qa_pairs = []

            st.success("✅ APEX plan generated successfully!")
            st.rerun()

        except Exception as e:
            st.error(f"❌ Generation error: {e}")


# ─── Display Plans ─────────────────────────────────────────────────────────────
if st.session_state.plans_generated:
    st.markdown("<div class='apex-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="icon">📋</div>
        <h2>Your APEX Protocol</h2>
    </div>
    """, unsafe_allow_html=True)

    plan_tab1, plan_tab2, plan_tab3 = st.tabs([
        "🍽️  NUTRITION PROTOCOL",
        "💪  TRAINING PROGRAM",
        "💬  AI HEALTH ASSISTANT"
    ])

    with plan_tab1:
        st.markdown(f"""
        <div class="plan-card green">
            <h3>🧬 Personalized Nutrition Protocol</h3>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1rem;">
                {get_badge_html(dietary_pref, 'green')}
                {get_badge_html(f"{macros['calories']} KCAL", 'cyan')}
                {get_badge_html(fitness_goal.upper(), 'purple')}
            </div>
        </div>""", unsafe_allow_html=True)

        # Macro reminder
        r1, r2, r3 = st.columns(3)
        with r1:
            st.metric("Daily Protein", f"{macros['protein']}g", help="Target protein intake")
        with r2:
            st.metric("Daily Carbs", f"{macros['carbs']}g", help="Target carbohydrate intake")
        with r3:
            st.metric("Daily Fats", f"{macros['fat']}g", help="Target fat intake")

        with st.expander("📋 View Full Nutrition Protocol", expanded=True):
            st.markdown(st.session_state.dietary_plan)

        st.markdown("""
        <div class="plan-card" style="border-color:rgba(57,255,20,0.2);margin-top:1rem;">
            <h3 style="color:#39ff14;">⚠️ General Nutrition Guidelines</h3>
            <div style="font-size:0.85rem;color:#9ca3af;line-height:1.8;">
            • Drink water consistently — aim for your daily water target spread evenly throughout the day<br>
            • Eat within 30–60 min of waking to kick-start metabolism<br>
            • Consume protein with every meal to maintain muscle synthesis<br>
            • Avoid processed sugars and trans fats regardless of goal<br>
            • Track adherence for at least 4 weeks before judging results<br>
            • Consult a licensed dietitian before making major dietary changes
            </div>
        </div>""", unsafe_allow_html=True)

    with plan_tab2:
        st.markdown(f"""
        <div class="plan-card purple">
            <h3>⚡ Performance Training Program</h3>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1rem;">
                {get_badge_html(fitness_goal.upper(), 'purple')}
                {get_badge_html(activity.upper(), 'cyan')}
                {get_badge_html('7-DAY PROGRAM', 'green')}
            </div>
        </div>""", unsafe_allow_html=True)

        with st.expander("🏋️ View Full Training Program", expanded=True):
            st.markdown(st.session_state.fitness_plan)

        st.markdown("""
        <div class="plan-card" style="border-color:rgba(191,0,255,0.2);margin-top:1rem;">
            <h3 style="color:#d966ff;">💡 Performance Optimization Tips</h3>
            <div style="font-size:0.85rem;color:#9ca3af;line-height:1.8;">
            • Track your lifts and progressively overload every 1–2 weeks<br>
            • Prioritize sleep (7–9 hours) — this is when muscle grows and recovers<br>
            • Deload every 4–6 weeks to prevent overtraining and injury<br>
            • Warm up dynamically before every session; static stretch post-workout<br>
            • Focus on compound movements for maximum hormonal response<br>
            • Consult a certified trainer before attempting new advanced exercises
            </div>
        </div>""", unsafe_allow_html=True)

    with plan_tab3:
        st.markdown("""
        <div class="plan-card" style="border-color:rgba(0,245,255,0.2);margin-bottom:1.25rem;">
            <h3 style="color:#00f5ff;">🤖 APEX AI Health Assistant</h3>
            <div style="font-size:0.84rem;color:#9ca3af;">
            Ask anything about your nutrition protocol, training program, recovery, supplements, or health goals.
            The AI has full context of your biometric profile and generated plans.
            </div>
        </div>""", unsafe_allow_html=True)

        with st.form("qa_form", clear_on_submit=True):
            q_col1, q_col2 = st.columns([5, 1])
            with q_col1:
                question = st.text_input("", placeholder="e.g. Can I substitute chicken with tofu? What's the best pre-workout meal?")
            with q_col2:
                submitted = st.form_submit_button("→ ASK", use_container_width=True)

        if submitted and question:
            context = (
                f"User biometric profile:\n{user_profile if 'user_profile' in dir() else 'Profile data from session'}\n\n"
                f"Dietary Plan:\n{st.session_state.dietary_plan}\n\n"
                f"Fitness Plan:\n{st.session_state.fitness_plan}\n\n"
                f"User Question: {question}"
            )
            with st.spinner("🧠 Processing your query..."):
                try:
                    qa_agent = Agent(
                        model=grok_model,
                        instructions=[
                            "You are APEX — an elite AI health and fitness advisor.",
                            "Answer questions about the user's personalized dietary and fitness plans.",
                            "Be specific, evidence-based, and actionable. Reference the user's plan when relevant.",
                            "Keep answers concise but thorough. Use bullet points for clarity when appropriate.",
                        ],
                        markdown=True
                    )
                    response = qa_agent.run(context)
                    answer = response.content if hasattr(response, 'content') else "Unable to generate response."
                    st.session_state.qa_pairs.append((question, answer))
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        # Q&A History
        if st.session_state.qa_pairs:
            st.markdown(f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;letter-spacing:0.2em;color:#6b7280;text-transform:uppercase;margin-bottom:0.75rem;">{len(st.session_state.qa_pairs)} Exchanges Logged</div>', unsafe_allow_html=True)
            for i, (q, a) in enumerate(reversed(st.session_state.qa_pairs)):
                idx = len(st.session_state.qa_pairs) - i
                st.markdown(f"""
                <div class="chat-msg chat-user">
                    <div class="chat-label">USER · Query #{idx}</div>
                    {q}
                </div>
                <div class="chat-msg chat-ai">
                    <div class="chat-label">⚡ APEX AI · Response</div>
                    {a}
                </div>""", unsafe_allow_html=True)


# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div class='apex-divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:1rem 0 0.5rem;font-family:'JetBrains Mono',monospace;
            font-size:0.58rem;letter-spacing:0.25em;color:#374151;">
    APEX · AI HEALTH INTELLIGENCE · POWERED BY GROK AI &nbsp;|&nbsp;
    FOR INFORMATIONAL PURPOSES ONLY · NOT MEDICAL ADVICE · CONSULT A HEALTHCARE PROFESSIONAL
</div>
""", unsafe_allow_html=True)
