# 🩺 MedSafe AI — Intelligent Medicine Safety Assistant

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medisafe.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-Educational-green)

> **MedSafe AI** is an AI-powered medicine safety assistant that helps users identify drug interactions, analyse prescriptions via OCR, get symptom guidance, monitor side effects, and predict emergency risk — all in a clean dark-theme web interface.

---

## 🚀 Live Demo

**[https://medisafe.streamlit.app/](https://medisafe.streamlit.app/)**

---

## ✨ Features

| Tab | Feature |
|-----|---------|
| 💊 **Interaction Checker** | Enter multiple medicines and instantly get drug interaction warnings with severity levels and an AI-generated safety summary |
| 📋 **Prescription OCR** | Upload a prescription image — Tesseract OCR extracts raw text, Groq AI parses medicines, salts, and dosages into structured JSON |
| 🤒 **Symptom Solver** | Describe your symptoms and receive rule-based guidance enhanced with an AI educational explanation |
| ⚠️ **Side Effect Monitor** | Log medicines, doses, and experiences — AI analyses potential side-effect relationships with urgent-alert detection |
| 🚨 **Risk Predictor** | Input patient demographics, medicines, symptoms, and conditions to receive a transparent 0–100 risk score (LOW / MODERATE / HIGH / CRITICAL) |

---

## 🏗️ Project Structure

```
MedSafe/
├── main.py               # Streamlit UI — all 5 tabs, dark theme CSS, session state
├── med_db.py             # Medicine database — 22 drugs with interactions, side effects, dosages
├── symptom.py            # Rule-based symptom guidance engine
├── ocr_utils.py          # Tesseract OCR preprocessing and text extraction
├── risk_engine.py        # Emergency risk scoring engine with fuzzy medicine matching
├── requirements.txt      # Python dependencies
├── packages.txt          # System packages for Streamlit Cloud (Tesseract)
├── .streamlit/
│   └── config.toml       # Streamlit theme and server configuration
└── .gitignore
```

---

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io/)** — Web UI framework
- **[Groq API](https://console.groq.com/)** — LLM inference (LLaMA 3.3 70B) for AI summaries and prescription parsing
- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)** + **pytesseract** — Prescription image text extraction
- **[RapidFuzz](https://github.com/maxbachmann/RapidFuzz)** — Fuzzy medicine name matching (WRatio scorer, LRU-cached)
- **Pillow** — Image preprocessing (contrast, sharpness, grayscale)

---

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/gitpranaav/MedSafe.git
cd MedSafe
```

### 2. Create and activate a virtual environment
```bash
python -m venv medsafe_env

# Windows
.\medsafe_env\Scripts\Activate.ps1

# macOS / Linux
source medsafe_env/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Tesseract OCR
- **Windows:** Download from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and install to `C:\Program Files\Tesseract-OCR\`
- **macOS:** `brew install tesseract`
- **Linux:** `sudo apt install tesseract-ocr`

### 5. Set your Groq API key
Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free API key at [console.groq.com](https://console.groq.com/).

### 6. Run the app
```bash
streamlit run main.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploying to Streamlit Cloud

1. Fork / push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a **New app**
3. Select your repo, branch `main`, main file `main.py`
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
5. Click **Deploy**

> Tesseract is automatically installed on Streamlit Cloud via `packages.txt`.

---

## 🗃️ Medicine Database

The built-in database (`med_db.py`) covers 22 commonly prescribed medicines across categories:

| Category | Medicines |
|---|---|
| Statins | Atorvastatin, Rosuvastatin, Simvastatin |
| Antidiabetics | Metformin, Glipizide, Insulin |
| Antibiotics | Amoxicillin, Amoxicillin-Clavulanate, Cefuroxime, Azithromycin, Ciprofloxacin |
| Analgesics / NSAIDs | Ibuprofen, Paracetamol, Aspirin |
| Cardiovascular | Lisinopril, Amlodipine, Metoprolol, Warfarin, Clopidogrel, Amiodarone, Digoxin |
| GI | Omeprazole |

Each entry includes: standard adult/paediatric dosage, drug interactions with severity labels, side effects, contraindications, and drug category.

---

## ⚠️ Disclaimer

**MedSafe AI is for educational purposes only.**
It is NOT a substitute for professional medical advice, diagnosis, or treatment.
Always consult a qualified healthcare professional before making any medical decisions.

---

## 📄 License

This project is developed for educational use.
