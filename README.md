# ⚡ APEX · Indian Health Intelligence

<div align="center">

![APEX Banner](https://img.shields.io/badge/APEX-Indian%20Health%20Intelligence-FF9933?style=for-the-badge&logo=lightning&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-00BCD4?style=for-the-badge&logo=groq&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-FFD700?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-138808?style=for-the-badge)

### 🇮🇳 AI-powered Indian Diet & Fitness Planner — Built for Bharat

**[Apex Fitness Live +](https://apex-fitness-ai.streamlit.app)**

</div>

---

## 📌 Overview

**APEX** is a next-generation AI health planner built specifically for Indians. It generates personalized Indian diet plans and weekly fitness programs using your biometric profile, regional cuisine preference, and health conditions — all powered by **Groq's LLaMA 3.3 70B** model for blazing-fast responses.

Unlike generic Western fitness apps, APEX understands:
- 🍛 Real Indian foods — dal, sabzi, roti, idli, poha, rajma, paneer, makhana
- 🌿 Ayurvedic recovery — ashwagandha, haldi doodh, abhyanga, pranayama
- 🏋️ Surya Namaskar warm-ups and yoga cool-downs
- 🗺️ Regional cuisine — North, South, East, West Indian
- 🩺 Indian health conditions — diabetes, PCOS, thyroid, acidity, anemia

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧬 **Live Biometric Dashboard** | Real-time BMI (Asian cutoffs), BMR, TDEE, ideal weight, water intake |
| 🍛 **Indian Nutrition Protocol** | Meal-by-meal plan with exact grams, macros & Indian food alternatives |
| 💪 **7-Day Training Program** | Sets, reps, RPE, Surya Namaskar, yoga cool-down, progressive overload |
| 📊 **Macro Tracker** | Visual protein/carbs/fat split based on your goal |
| 💬 **AI Health Assistant** | Ask anything — festival fasting, ingredient swaps, Ayurvedic tips |
| 🌿 **Ayurvedic Recovery** | Daily haldi doodh, ashwagandha, pranayama recommendations |
| 🔒 **Secure API Handling** | API key stored in Streamlit secrets — never exposed |

---

## 🖼️ Screenshots

> Live at website: **[Check here!](https://apex-fitness-ai.streamlit.app)**

---

## 🛠️ Tech Stack

```
Frontend      →  Streamlit 1.40+
AI Engine     →  Groq API (LLaMA 3.3 70B Versatile)
API Client    →  OpenAI Python SDK (Groq-compatible)
Language      →  Python 3.10+
Deployment    →  Streamlit Community Cloud
Fonts         →  Syne · DM Sans · JetBrains Mono (Google Fonts)
```

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Groq API key

Create a file at `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```
> Get your free API key at [console.groq.com](https://console.groq.com)

### 4. Run the app
```bash
streamlit run health_agent.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **Create app**
3. Select your repo, branch, and `health_agent.py` as the main file
4. Click **Advanced settings → Secrets** and add:
```toml
GROQ_API_KEY = "gsk_your_key_here"
```
5. Click **Deploy** 🚀

---

## 📁 Project Structure

```
├── health_agent.py       # Main Streamlit app
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
└── .streamlit/
    └── secrets.toml      # API keys (DO NOT commit this file)
```

---

## 📦 Requirements

```
streamlit==1.40.2
openai>=1.0.0
```

---

## 🧠 How It Works

```
User fills biometric profile
        ↓
App calculates BMI, BMR, TDEE, macros in real-time
        ↓
User clicks "Generate My APEX Plan"
        ↓
Two parallel Groq API calls:
  → Nutrition Agent  →  Indian meal plan with exact portions
  → Fitness Agent    →  7-day training program with Ayurvedic tips
        ↓
Results displayed in tabbed interface
        ↓
User can ask follow-up questions via AI Health Assistant
```

---

## 🇮🇳 Why APEX for India?

Most fitness apps are built for Western users. APEX is different:

- Uses **Asian BMI cutoffs** (healthy = 18.5–23, not 25)
- Plans based on **real Indian staples** — not chicken & broccoli
- Considers **Indian health conditions** like PCOD, thyroid, acidity
- Integrates **Ayurvedic wisdom** — haldi, ashwagandha, abhyanga
- Supports **religious & lifestyle diets** — Jain, Sattvic, Eggetarian
- Regional cuisine options for **North, South, East & West India**

---

## ⚠️ Disclaimer

APEX is an **AI-powered informational tool only**. It is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified doctor, registered dietitian, or certified fitness trainer before making significant changes to your diet or exercise routine — especially if you have existing health conditions.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

- [Groq](https://groq.com) — Ultra-fast LLaMA inference
- [Streamlit](https://streamlit.io) — Rapid Python web app framework
- [Meta LLaMA](https://llama.meta.com) — Open-source LLM powering the AI
- [Google Fonts](https://fonts.google.com) — Syne, DM Sans, JetBrains Mono

---

<div align="center">

Made with ❤️ for India 🇮🇳

**[⚡APEX FITNESS PLANNER⚡](https://apex-fitness-ai.streamlit.app)**

</div>
