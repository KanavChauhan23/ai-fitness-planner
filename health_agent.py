import streamlit as st
from openai import OpenAI

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
    --border-glow: rgba(0, 245, 255, 0.25);
    --text-primary: #e8eaf0;
    --text-muted: #6b7280;
}

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

#MainMenu, footer, header { visibility: hidden; }

.apex-hero { text-align: center; padding: 2.5rem 1rem 1.5rem; }
.apex-hero .tag {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem; letter-spacing: 0.3em; color: var(--neon-cyan);
    border: 1px solid rgba(0,245,255,0.35); padding: 0.25rem 0.9rem;
    border-radius: 100px; margin-bottom: 1rem; background: rgba(0,245,255,0.04);
}
.apex-hero h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 900; letter-spacing: 0.05em;
    background: linear-gradient(135deg, #ffffff 0%, var(--neon-cyan) 50%, var(--neon-purple) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem; line-height: 1.1;
}
.apex-hero p { color: var(--text-muted); font-size: 1rem; font-weight: 300; max-width: 550px; margin: 0 auto; }
.apex-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
    margin: 1.5rem 0; opacity: 0.4;
}

.metric-card {
    background: var(--bg-card); border: 1px solid var(--border-glow);
    border-radius: 12px; padding: 1.25rem 1.5rem; position: relative; overflow: hidden;
}
.metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
}
.metric-card .label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.62rem;
    letter-spacing: 0.2em; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.4rem;
}
.metric-card .value {
    font-family: 'Orbitron', sans-serif; font-size: 1.8rem;
    font-weight: 700; color: var(--neon-cyan); line-height: 1;
}
.metric-card .unit { font-size: 0.85rem; color: var(--text-muted); margin-left: 0.3rem; }
.metric-card .sub { font-size: 0.78rem; color: var(--text-muted); margin-top: 0.3rem; }

.badge { display: inline-block; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; padding: 0.2rem 0.65rem; border-radius: 100px; font-weight: 600; letter-spacing: 0.05em; }
.badge-green  { background: rgba(57,255,20,0.12);  color: #39ff14; border: 1px solid rgba(57,255,20,0.35); }
.badge-cyan   { background: rgba(0,245,255,0.12);  color: #00f5ff; border: 1px solid rgba(0,245,255,0.3); }
.badge-orange { background: rgba(255,107,0,0.12);  color: #ff6b00; border: 1px solid rgba(255,107,0,0.35); }
.badge-purple { background: rgba(191,0,255,0.12);  color: #d966ff; border: 1px solid rgba(191,0,255,0.35); }

.section-header { display: flex; align-items: center; gap: 0.75rem; margin: 2rem 0 1rem; }
.section-header .icon {
    width: 36px; height: 36px; border-radius: 8px;
    background: rgba(0,245,255,0.1); border: 1px solid rgba(0,245,255,0.3);
    display: flex; align-items: center; justify-content: center; font-size: 1rem;
}
.section-header h2 {
    font-family: 'Orbitron', sans-serif; font-size: 0.95rem; font-weight: 700;
    letter-spacing: 0.12em; color: var(--text-primary); text-transform: uppercase; margin: 0;
}

.plan-card {
    background: var(--bg-card); border: 1px solid var(--border-glow);
    border-radius: 14px; padding: 1.5rem 1.75rem; margin-bottom: 1.25rem; position: relative;
}
.plan-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; }
.plan-card.green  { border-color: rgba(57,255,20,0.25); }
.plan-card.green::before  { background: linear-gradient(90deg, transparent, #39ff14, transparent); }
.plan-card.purple { border-color: rgba(191,0,255,0.25); }
.plan-card.purple::before { background: linear-gradient(90deg, transparent, #bf00ff, transparent); }
.plan-card h3 { font-family: 'Orbitron', sans-serif; font-size: 0.8rem; letter-spacing: 0.15em; text-transform: uppercase; margin: 0 0 1rem; }
.plan-card.green h3  { color: #39ff14; }
.plan-card.purple h3 { color: #d966ff; }

.prog-wrap { margin: 0.5rem 0; }
.prog-label { display: flex; justify-content: space-between; margin-bottom: 0.3rem; font-size: 0.78rem; color: var(--text-muted); }
.prog-bar { height: 6px; background: rgba(255,255,255,0.07); border-radius: 100px; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 100px; }

.chat-msg { padding: 0.85rem 1.1rem; border-radius: 10px; margin-bottom: 0.75rem; font-size: 0.9rem; line-height: 1.6; }
.chat-user { background: rgba(0,245,255,0.07); border-left: 3px solid #00f5ff; }
.chat-ai   { background: rgba(191,0,255,0.07); border-left: 3px solid #bf00ff; }
.chat-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.15em; margin-bottom: 0.4rem; opacity: 0.6; text-transform: uppercase; }

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,245,255,0.2) !important;
    border-radius: 8px !important; color: var(--text-primary) !important;
}
.stTextInput > div > div > input:focus { border-color: rgba(0,245,255,0.55) !important; box-shadow: 0 0 0 2px rgba(0,245,255,0.12) !important; }
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, rgba(0,245,255,0.15), rgba(191,0,255,0.15)) !important;
    border: 1px solid rgba(0,245,255,0.4) !important; color: #00f5ff !important;
    font-family: 'Orbitron', sans-serif !important; font-size: 0.75rem !important;
    font-weight: 700 !important; letter-spacing: 0.15em !important;
    border-radius: 8px !important; padding: 0.65rem 1rem !important; transition: all 0.3s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,245,255,0.28), rgba(191,0,255,0.28)) !important;
    border-color: #00f5ff !important; box-shadow: 0 0 20px rgba(0,245,255,0.2) !important;
}
.stSidebar { background: rgba(8,10,18,0.98) !important; border-right: 1px solid rgba(0,245,255,0.1) !important; }
label, .stSelectbox label, .stNumberInput label, .stTextInput label {
    color: #9ca3af !important; font-size: 0.8rem !important;
    font-family: 'JetBrains Mono', monospace !important; letter-spacing: 0.08em !important;
}
.stTabs [data-baseweb="tab-list"] { background: rgba(255,255,255,0.03) !important; border-radius: 10px !important; padding: 4px !important; }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important; color: var(--text-muted) !important; }
.stTabs [aria-selected="true"] { background: rgba(0,245,255,0.12) !important; color: #00f5ff !important; }
hr { border-color: rgba(0,245,255,0.12) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ──────────────────────────────────────────────────────────
def calculate_bmi(weight_kg, height_cm):
    if height_cm <= 0:
        return 0.0, "N/A", "cyan"
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5:   return round(bmi, 1), "Underweight", "orange"
    elif bmi < 25:   return round(bmi, 1), "Normal", "green"
    elif bmi < 30:   return round(bmi, 1), "Overweight", "orange"
    else:            return round(bmi, 1), "Obese", "purple"

def calculate_tdee(weight_kg, height_cm, age, sex, activity_level):
    if sex == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    multipliers = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725, "Extremely Active": 1.9}
    tdee = bmr * multipliers.get(activity_level, 1.55)
    return round(bmr), round(tdee)

def calculate_ideal_weight(height_cm, sex):
    if height_cm < 152.4: return 50 if sex == "Male" else 45.5
    extra_inches = (height_cm - 152.4) / 2.54
    return round(50 + 2.3 * extra_inches, 1) if sex == "Male" else round(45.5 + 2.3 * extra_inches, 1)

def macro_split(tdee, goal):
    if goal == "Lose Weight":
        cals = tdee - 400; p, f, c = 0.35, 0.30, 0.35
    elif goal == "Gain Muscle":
        cals = tdee + 350; p, f, c = 0.30, 0.25, 0.45
    elif goal == "Strength Training":
        cals = tdee + 200; p, f, c = 0.32, 0.28, 0.40
    else:
        cals = tdee; p, f, c = 0.25, 0.30, 0.45
    return {"calories": round(cals), "protein": round(cals*p/4), "fat": round(cals*f/9), "carbs": round(cals*c/4)}

def prog_bar(label, value, max_val, color):
    pct = min(100, round(value / max_val * 100))
    return f"""<div class="prog-wrap">
        <div class="prog-label"><span>{label}</span><span>{value}g</span></div>
        <div class="prog-bar"><div class="prog-fill" style="width:{pct}%;background:{color};"></div></div>
    </div>"""

def badge(text, color):
    return f'<span class="badge badge-{color}">{text}</span>'

def ask_grok(client, model, system_prompt, user_message):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        max_tokens=2048,
        temperature=0.7
    )
    return response.choices[0].message.content


# ─── Session State ─────────────────────────────────────────────────────────────
for k, v in {"dietary_plan": None, "fitness_plan": None, "qa_pairs": [], "plans_generated": False}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.5rem;">
        <div style="font-family:'Orbitron',sans-serif;font-size:1.2rem;font-weight:900;
                    background:linear-gradient(135deg,#00f5ff,#bf00ff);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    letter-spacing:0.2em;">⚡ APEX</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;color:#4b5563;letter-spacing:0.3em;margin-top:0.2rem;">
            AI HEALTH INTELLIGENCE v2.0</div>
    </div>""", unsafe_allow_html=True)

    # API key loaded from Streamlit secrets
    grok_api_key = st.secrets.get("GROK_API_KEY", "")
    if grok_api_key:
        st.markdown('<div style="background:rgba(57,255,20,0.08);border:1px solid rgba(57,255,20,0.25);border-radius:8px;padding:0.65rem;font-size:0.78rem;color:#39ff14;margin:0.5rem 0;">✓ Systems Online</div>', unsafe_allow_html=True)
    else:
        st.markdown("""<div style="background:rgba(255,107,0,0.08);border:1px solid rgba(255,107,0,0.3);
            border-radius:8px;padding:0.75rem;font-size:0.78rem;color:#ff6b00;margin:0.5rem 0;">
            ⚠️ GROK_API_KEY not found in Streamlit secrets</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.65rem;letter-spacing:0.2em;color:#6b7280;text-transform:uppercase;margin-bottom:0.75rem;">⚙️ Model Config</div>', unsafe_allow_html=True)
    model_choice = st.selectbox("Model", ["grok-3-mini", "grok-3", "grok-2-1212"])

    st.divider()
    if st.session_state.plans_generated:
        st.markdown(f'<div class="badge badge-cyan">PLAN ACTIVE</div><div style="font-size:0.78rem;color:#6b7280;margin-top:0.5rem;">{len(st.session_state.qa_pairs)} Q&A exchanges</div>', unsafe_allow_html=True)
        if st.button("🔄 RESET SESSION"):
            st.session_state.dietary_plan = None
            st.session_state.fitness_plan = None
            st.session_state.qa_pairs = []
            st.session_state.plans_generated = False
            st.rerun()


# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="apex-hero">
    <div class="tag">POWERED BY GROK AI · NEXT-GEN HEALTH INTELLIGENCE</div>
    <h1>APEX HEALTH PLANNER</h1>
    <p>Precision-engineered dietary and fitness protocols calibrated to your unique biometric profile</p>
</div>
<div class="apex-divider"></div>
""", unsafe_allow_html=True)

if not grok_api_key:
    st.error("⚠️ GROK_API_KEY not found. Please add it to your Streamlit Cloud secrets: Settings → Secrets → add `GROK_API_KEY = 'xai-...'`")
    st.stop()

# Init Grok client
client = OpenAI(api_key=grok_api_key, base_url="https://api.x.ai/v1")


# ─── Profile Input ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><div class="icon">👤</div><h2>Biometric Profile</h2></div>', unsafe_allow_html=True)

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


# ─── Live Biometric Dashboard ──────────────────────────────────────────────────
bmi, bmi_cat, bmi_col = calculate_bmi(weight, height)
bmr, tdee = calculate_tdee(weight, height, age, sex, activity)
ideal_wt  = calculate_ideal_weight(height, sex)
macros    = macro_split(tdee, fitness_goal)
wt_diff   = round(weight - ideal_wt, 1)
wt_status = f"+{wt_diff}kg above ideal" if wt_diff > 0 else f"{abs(wt_diff)}kg below ideal" if wt_diff < 0 else "At ideal weight"
water_l   = round(weight * 0.033, 1)

st.markdown('<div class="section-header"><div class="icon">📊</div><h2>Live Biometric Analysis</h2></div>', unsafe_allow_html=True)
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f'<div class="metric-card"><div class="label">Body Mass Index</div><div class="value">{bmi}<span class="unit">BMI</span></div><div class="sub">{badge(bmi_cat, bmi_col)}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="label">Basal Metabolic Rate</div><div class="value">{bmr:,}<span class="unit">kcal</span></div><div class="sub" style="color:#6b7280">Resting expenditure</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><div class="label">Daily Energy Target</div><div class="value">{macros["calories"]:,}<span class="unit">kcal</span></div><div class="sub">{badge(fitness_goal.upper(), "cyan")}</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="label">Ideal Body Weight</div><div class="value">{ideal_wt}<span class="unit">kg</span></div><div class="sub" style="color:#6b7280">{wt_status}</div></div>', unsafe_allow_html=True)
with m5:
    st.markdown(f'<div class="metric-card"><div class="label">Daily Water Intake</div><div class="value">{water_l}<span class="unit">L</span></div><div class="sub" style="color:#6b7280">{round(water_l*4)} glasses/day</div></div>', unsafe_allow_html=True)


# ─── Macro Breakdown ───────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><div class="icon">🧬</div><h2>Macro Nutrient Protocol</h2></div>', unsafe_allow_html=True)
mc1, mc2 = st.columns([3, 1])
with mc1:
    st.markdown(f"""<div class="plan-card green">
        <h3>🎯 Target Macros · {macros['calories']:,} kcal/day</h3>
        {prog_bar('Protein', macros['protein'], 250, '#39ff14')}
        {prog_bar('Carbohydrates', macros['carbs'], 350, '#00f5ff')}
        {prog_bar('Fats', macros['fat'], 120, '#bf00ff')}
    </div>""", unsafe_allow_html=True)
with mc2:
    prot_pct = round(macros['protein'] * 4 / macros['calories'] * 100)
    carb_pct = round(macros['carbs']   * 4 / macros['calories'] * 100)
    fat_pct  = round(macros['fat']     * 9 / macros['calories'] * 100)
    st.markdown(f"""<div class="metric-card">
        <div class="label">Split Ratio</div>
        <div style="margin-top:0.75rem;display:flex;flex-direction:column;gap:0.5rem;">
            <div style="display:flex;justify-content:space-between;font-size:0.82rem;"><span style="color:#39ff14">● Protein</span><span style="font-family:'JetBrains Mono',monospace">{prot_pct}%</span></div>
            <div style="display:flex;justify-content:space-between;font-size:0.82rem;"><span style="color:#00f5ff">● Carbs</span><span style="font-family:'JetBrains Mono',monospace">{carb_pct}%</span></div>
            <div style="display:flex;justify-content:space-between;font-size:0.82rem;"><span style="color:#bf00ff">● Fats</span><span style="font-family:'JetBrains Mono',monospace">{fat_pct}%</span></div>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div class='apex-divider'></div>", unsafe_allow_html=True)


# ─── Generate Plans ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header"><div class="icon">⚡</div><h2>AI Plan Generation</h2></div>', unsafe_allow_html=True)
_, gen_col, _ = st.columns([1, 2, 1])
with gen_col:
    generate_clicked = st.button("⚡ GENERATE MY APEX PLAN", use_container_width=True)

if generate_clicked:
    conditions_str  = ", ".join([c for c in health_conditions if c != "None"]) or "None"
    supplements_str = ", ".join([s for s in supplements if s != "None"]) or "None"

    user_profile = f"""
BIOMETRIC PROFILE:
- Age: {age} | Sex: {sex} | Weight: {weight}kg | Height: {height}cm
- BMI: {bmi} ({bmi_cat}) | BMR: {bmr} kcal | TDEE: {tdee} kcal | Ideal Weight: {ideal_wt}kg

GOALS & PREFERENCES:
- Primary Goal: {fitness_goal} | Activity: {activity}
- Diet: {dietary_pref} | Health Conditions: {conditions_str} | Supplements: {supplements_str}

MACRO TARGETS:
- Calories: {macros['calories']} kcal | Protein: {macros['protein']}g | Carbs: {macros['carbs']}g | Fats: {macros['fat']}g
"""

    try:
        with st.spinner("🍽️ Generating nutrition protocol..."):
            dietary_plan = ask_grok(
                client, model_choice,
                f"""You are an elite sports nutritionist. Create a highly detailed personalized meal plan.
Respect dietary preference: {dietary_pref}. Account for health conditions: {conditions_str}.
Format: Pre-Workout, Breakfast, Mid-Morning Snack, Lunch, Afternoon Snack, Post-Workout, Dinner.
For each meal list: food items with portions (grams), estimated macros, and prep notes.
Target: {macros['calories']} kcal, {macros['protein']}g protein, {macros['carbs']}g carbs, {macros['fat']}g fat.
Include hydration protocol and supplement timing. Be specific and scientific.""",
                user_profile
            )

        with st.spinner("💪 Generating training program..."):
            fitness_plan = ask_grok(
                client, model_choice,
                f"""You are an elite strength and conditioning coach. Create a science-backed 7-day training program.
Goal: {fitness_goal} | Activity Level: {activity} | Conditions: {conditions_str}.
Include: rest days, warm-up, main exercises with sets/reps/rest/RPE, cool-down.
Add progressive overload strategy, deload guidance, form cues for key lifts.
Be specific and actionable.""",
                user_profile
            )

        st.session_state.dietary_plan    = dietary_plan
        st.session_state.fitness_plan    = fitness_plan
        st.session_state.plans_generated = True
        st.session_state.qa_pairs        = []
        st.success("✅ APEX plan generated successfully!")
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error: {e}")


# ─── Display Plans ─────────────────────────────────────────────────────────────
if st.session_state.plans_generated:
    st.markdown("<div class='apex-divider'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="icon">📋</div><h2>Your APEX Protocol</h2></div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🍽️  NUTRITION PROTOCOL", "💪  TRAINING PROGRAM", "💬  AI HEALTH ASSISTANT"])

    with tab1:
        st.markdown(f"""<div class="plan-card green">
            <h3>🧬 Personalized Nutrition Protocol</h3>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
                {badge(dietary_pref, 'green')} {badge(f"{macros['calories']} KCAL", 'cyan')} {badge(fitness_goal.upper(), 'purple')}
            </div></div>""", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Daily Protein", f"{macros['protein']}g")
        c2.metric("Daily Carbs",   f"{macros['carbs']}g")
        c3.metric("Daily Fats",    f"{macros['fat']}g")
        with st.expander("📋 Full Nutrition Protocol", expanded=True):
            st.markdown(st.session_state.dietary_plan)
        st.markdown("""<div class="plan-card green" style="margin-top:1rem;">
            <h3>⚠️ Nutrition Guidelines</h3>
            <div style="font-size:0.85rem;color:#9ca3af;line-height:1.8;">
            • Spread water intake evenly throughout the day<br>
            • Eat within 30–60 min of waking to kick-start metabolism<br>
            • Include protein in every meal for muscle synthesis<br>
            • Avoid processed sugars and trans fats<br>
            • Consult a licensed dietitian before major changes
            </div></div>""", unsafe_allow_html=True)

    with tab2:
        st.markdown(f"""<div class="plan-card purple">
            <h3>⚡ Performance Training Program</h3>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
                {badge(fitness_goal.upper(), 'purple')} {badge(activity.upper(), 'cyan')} {badge('7-DAY PROGRAM', 'green')}
            </div></div>""", unsafe_allow_html=True)
        with st.expander("🏋️ Full Training Program", expanded=True):
            st.markdown(st.session_state.fitness_plan)
        st.markdown("""<div class="plan-card purple" style="margin-top:1rem;">
            <h3>💡 Performance Tips</h3>
            <div style="font-size:0.85rem;color:#9ca3af;line-height:1.8;">
            • Progressively overload every 1–2 weeks<br>
            • Prioritize 7–9 hours sleep for recovery<br>
            • Deload every 4–6 weeks to prevent overtraining<br>
            • Dynamic warm-up before; static stretch after<br>
            • Consult a certified trainer before advanced exercises
            </div></div>""", unsafe_allow_html=True)

    with tab3:
        st.markdown("""<div class="plan-card" style="border-color:rgba(0,245,255,0.2);margin-bottom:1.25rem;">
            <h3 style="color:#00f5ff;">🤖 APEX AI Health Assistant</h3>
            <div style="font-size:0.84rem;color:#9ca3af;">
            Ask anything about your nutrition, training, recovery, or supplements.
            The AI has full context of your biometric profile and generated plans.
            </div></div>""", unsafe_allow_html=True)

        with st.form("qa_form", clear_on_submit=True):
            q1, q2 = st.columns([5, 1])
            with q1:
                question = st.text_input("", placeholder="e.g. Can I swap chicken with tofu? Best pre-workout meal?", label_visibility="collapsed")
            with q2:
                submitted = st.form_submit_button("→ ASK", use_container_width=True)

        if submitted and question:
            with st.spinner("🧠 Processing..."):
                try:
                    context = f"User profile + plans:\n\nDietary Plan:\n{st.session_state.dietary_plan}\n\nFitness Plan:\n{st.session_state.fitness_plan}"
                    answer  = ask_grok(
                        client, model_choice,
                        "You are APEX — an elite AI health and fitness advisor. Answer questions about the user's personalized plans. Be specific, evidence-based, and concise.",
                        f"{context}\n\nUser Question: {question}"
                    )
                    st.session_state.qa_pairs.append((question, answer))
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        for i, (q, a) in enumerate(reversed(st.session_state.qa_pairs)):
            idx = len(st.session_state.qa_pairs) - i
            st.markdown(f"""
            <div class="chat-msg chat-user"><div class="chat-label">USER · #{idx}</div>{q}</div>
            <div class="chat-msg chat-ai"><div class="chat-label">⚡ APEX AI</div>{a}</div>
            """, unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div class='apex-divider'></div>", unsafe_allow_html=True)
st.markdown("""<div style="text-align:center;padding:1rem 0 0.5rem;font-family:'JetBrains Mono',monospace;
    font-size:0.58rem;letter-spacing:0.25em;color:#374151;">
    APEX · AI HEALTH INTELLIGENCE · POWERED BY GROK AI &nbsp;|&nbsp;
    FOR INFORMATIONAL PURPOSES ONLY · NOT MEDICAL ADVICE
</div>""", unsafe_allow_html=True)
