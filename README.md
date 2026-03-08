# MedSafe AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://medisafe.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

MedSafe AI is a medicine safety assistant built with Python and Streamlit. It combines a local drug interaction database, OCR-based prescription reading, rule-based symptom guidance, and an AI layer (powered by Groq) to help users understand their medications more safely.

The project was built as an educational tool — it is not intended for clinical use.

**Live app:** [https://medisafe.streamlit.app/](https://medisafe.streamlit.app/)

---

## What it does

The app is split into five tabs, each covering a different aspect of medicine safety:

- **Interaction Checker** — Enter a list of medicines and the app cross-references them against a database of known drug interactions, flagging high and moderate severity pairs. An AI summary is generated to explain the most important concern in plain language.

- **Prescription OCR** — Upload a photo or scan of a prescription. Tesseract OCR pulls the raw text out of the image, and the AI then parses it into a structured list of medicines, salts, and dosages. Identified medicines are automatically matched against the database.

- **Symptom Solver** — Describe what you are feeling and the app returns relevant guidance based on keyword matching across common symptom categories. An AI-enhanced explanation is added to give more context around the advice.

- **Side Effect Monitor** — Input the medicines you are taking, your doses, and what you have been experiencing. The app profiles each medicine from the database and generates an AI analysis of which side effects may relate to which drug, along with advice on when to see a doctor.

- **Risk Predictor** — Enter patient age, gender, current medicines, symptoms, and medical conditions. The engine calculates a risk score from 0 to 100 across eight weighted categories (age, polypharmacy, dangerous combinations, symptom severity, etc.) and returns a colour-coded level — LOW, MODERATE, HIGH, or CRITICAL.

---

## Project structure

```
MedSafe/
├── main.py               # Streamlit app — UI, tabs, session state, CSS
├── med_db.py             # Medicine database (22 drugs)
├── symptom.py            # Symptom keyword matching engine
├── ocr_utils.py          # Image preprocessing and Tesseract OCR
├── risk_engine.py        # Risk scoring engine and fuzzy medicine lookup
├── requirements.txt      # Python dependencies
├── packages.txt          # System packages for Streamlit Cloud
├── .streamlit/
│   └── config.toml       # Theme and server settings
└── .gitignore
```

---

## Tech stack

- [Streamlit](https://streamlit.io/) for the web interface
- [Groq API](https://console.groq.com/) with LLaMA 3.3 70B for AI summaries and prescription parsing
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) via pytesseract for image text extraction
- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) for fuzzy medicine name matching, with LRU caching
- Pillow for image preprocessing

---

## Running locally

**1. Clone the repo**
```bash
git clone https://github.com/gitpranaav/MedSafe.git
cd MedSafe
```

**2. Create a virtual environment**
```bash
python -m venv medsafe_env

# Windows
.\medsafe_env\Scripts\Activate.ps1

# macOS / Linux
source medsafe_env/bin/activate
```

**3. Install Python dependencies**
```bash
pip install -r requirements.txt
```

**4. Install Tesseract OCR**
- Windows: download the installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and install to `C:\Program Files\Tesseract-OCR\`
- macOS: `brew install tesseract`
- Linux: `sudo apt install tesseract-ocr`

**5. Add your Groq API key**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_key_here
```
A free key can be obtained at [console.groq.com](https://console.groq.com/).

**6. Start the app**
```bash
streamlit run main.py
```

---

## Deploying to Streamlit Cloud

1. Push the repo to GitHub (the `.env` and `medsafe_env/` folder are excluded by `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app pointing to `main.py` on the `main` branch
3. Under Advanced settings, add your secret:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
4. Deploy — Tesseract will be installed automatically from `packages.txt`

---

## Medicine database

The database in `med_db.py` covers 22 commonly prescribed medicines. Each entry stores the standard adult and paediatric dose, known drug interactions with severity labels, common side effects, contraindications, and drug category.

| Category | Medicines |
|---|---|
| Statins | Atorvastatin, Rosuvastatin, Simvastatin |
| Antidiabetics | Metformin, Glipizide, Insulin |
| Antibiotics | Amoxicillin, Amoxicillin-Clavulanate, Cefuroxime, Azithromycin, Ciprofloxacin |
| Analgesics / NSAIDs | Ibuprofen, Paracetamol, Aspirin |
| Cardiovascular | Lisinopril, Amlodipine, Metoprolol, Warfarin, Clopidogrel, Amiodarone, Digoxin |
| GI | Omeprazole |

---

## Disclaimer

MedSafe AI is built for educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional before making decisions about your medications.
