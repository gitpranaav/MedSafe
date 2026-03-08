# main.py — MedSafe AI  |  Streamlit Application Entry Point
# Run with:  streamlit run main.py
#
# MedSafe AI is an educational medicine safety assistant.
# It is NOT a substitute for professional medical advice.

from __future__ import annotations

import json
import re
import time
import logging
import streamlit as st
from PIL import Image
import pytesseract
from datetime import datetime
from functools import lru_cache
from rapidfuzz import fuzz

logging.basicConfig(
    filename="medsafe.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
_logger = logging.getLogger("medsafe")

from med_db import MED_DB
from symptom import symptom_advice
from ocr_utils import extract_text_from_image
from risk_engine import calculate_risk_score, find_medicine

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# ── Tesseract path (Windows) ──────────────────────────────────────────────────
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ── Groq API key: Streamlit Cloud secrets → .env fallback ──────────────────────
def _get_groq_key() -> str:
    try:
        return st.secrets["GROQ_API_KEY"]  # Streamlit Cloud
    except Exception:
        return os.environ.get("GROQ_API_KEY", "")

# ── Groq client ───────────────────────────────────────────────────────────────
_groq_client = Groq(api_key=_get_groq_key())
_GROQ_MODEL = "llama-3.3-70b-versatile"


# ══════════════════════════════════════════════════════════════════════════════
#  Page config — must be the very first Streamlit call
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="MedSafe AI – Intelligent Medicine Safety Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ══════════════════════════════════════════════════════════════════════════════
#  Custom CSS
# ══════════════════════════════════════════════════════════════════════════════

def _inject_css() -> None:
    st.markdown(
        """
        <style>
        /* ── Global / Body ─────────────────────────────────── */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0d1117;
            color: #e6edf3;
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }

        /* ── App header banner ──────────────────────────────── */
        .ms-header {
            background: linear-gradient(135deg, #161b22 0%, #1a2332 100%);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 22px 32px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 18px;
        }
        .ms-header-icon { font-size: 2.6rem; line-height: 1; }
        .ms-header-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: #e6edf3;
            margin: 0;
            letter-spacing: -0.5px;
        }
        .ms-header-sub {
            font-size: 0.82rem;
            color: #8b949e;
            margin: 2px 0 0;
        }

        /* ── Tab bar ────────────────────────────────────────── */
        [data-testid="stTabs"] > div:first-child {
            background: #161b22;
            border-radius: 10px 10px 0 0;
            border-bottom: 2px solid #21262d;
            padding: 0 8px;
            gap: 2px;
        }
        button[data-baseweb="tab"] {
            font-size: 0.82rem !important;
            font-weight: 600 !important;
            color: #8b949e !important;
            padding: 10px 18px !important;
            border-radius: 8px 8px 0 0 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #58a6ff !important;
            border-bottom: 2px solid #58a6ff !important;
            background: #0d1117 !important;
        }
        button[data-baseweb="tab"]:hover {
            color: #c9d1d9 !important;
            background: #1f2937 !important;
        }

        /* ── Section card ───────────────────────────────────── */
        .ms-card {
            background: #161b22;
            border: 1px solid #21262d;
            border-radius: 10px;
            padding: 24px 28px;
            margin-bottom: 18px;
        }
        .ms-card-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #c9d1d9;
            margin: 0 0 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* ── Section header (tab-level) ─────────────────────── */
        .ms-tab-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 6px;
        }
        .ms-tab-title {
            font-size: 1.45rem;
            font-weight: 700;
            color: #e6edf3;
            margin: 0;
        }
        .ms-tab-badge {
            background: #1f2937;
            border: 1px solid #30363d;
            border-radius: 20px;
            padding: 2px 10px;
            font-size: 0.72rem;
            color: #8b949e;
        }
        .ms-divider {
            border: none;
            border-top: 1px solid #21262d;
            margin: 18px 0;
        }

        /* ── Medicine chip ──────────────────────────────────── */
        .ms-chip-found {
            display: inline-block;
            background: #1a3a2a;
            border: 1px solid #238636;
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 0.82rem;
            color: #3fb950;
            margin: 3px 4px 3px 0;
            font-weight: 600;
        }
        .ms-chip-notfound {
            display: inline-block;
            background: #3a1a1a;
            border: 1px solid #da3633;
            border-radius: 20px;
            padding: 4px 14px;
            font-size: 0.82rem;
            color: #f85149;
            margin: 3px 4px 3px 0;
            font-weight: 600;
        }

        /* ── Interaction warning card ───────────────────────── */
        .ms-interaction {
            background: #2a1a0e;
            border-left: 4px solid #d29922;
            border-radius: 0 8px 8px 0;
            padding: 12px 16px;
            margin: 8px 0;
            font-size: 0.88rem;
            color: #e3b341;
            line-height: 1.55;
        }
        .ms-interaction-critical {
            background: #280d0d;
            border-left: 4px solid #da3633;
            border-radius: 0 8px 8px 0;
            padding: 12px 16px;
            margin: 8px 0;
            font-size: 0.88rem;
            color: #f78166;
            line-height: 1.55;
        }

        /* ── Risk score gauge ───────────────────────────────── */
        .ms-risk-gauge {
            text-align: center;
            padding: 28px 20px;
            border-radius: 12px;
            margin-bottom: 12px;
        }
        .ms-risk-number {
            font-size: 3.8rem;
            font-weight: 800;
            line-height: 1;
        }
        .ms-risk-label {
            font-size: 1.1rem;
            font-weight: 700;
            margin-top: 6px;
        }
        .ms-risk-critical { background: #280d0d; color: #f85149; border: 2px solid #da3633; }
        .ms-risk-high     { background: #2a1800; color: #d29922; border: 2px solid #9e6a03; }
        .ms-risk-moderate { background: #1e2210; color: #b5a31e; border: 2px solid #9e8a03; }
        .ms-risk-low      { background: #0d1f14; color: #3fb950; border: 2px solid #238636; }

        /* ── AI advice box ──────────────────────────────────── */
        .ms-ai-box {
            background: #111827;
            border: 1px solid #1d4ed8;
            border-left: 4px solid #3b82f6;
            border-radius: 0 8px 8px 0;
            padding: 16px 20px;
            margin: 10px 0;
            font-size: 0.9rem;
            color: #93c5fd;
            line-height: 1.7;
        }
        .ms-ai-box strong { color: #bfdbfe; }

        /* ── Metric box ─────────────────────────────────────── */
        .ms-metric {
            background: #161b22;
            border: 1px solid #21262d;
            border-radius: 10px;
            padding: 16px 20px;
            text-align: center;
        }
        .ms-metric-value {
            font-size: 1.9rem;
            font-weight: 800;
            color: #58a6ff;
        }
        .ms-metric-label {
            font-size: 0.78rem;
            color: #8b949e;
            margin-top: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* ── Info pill ──────────────────────────────────────── */
        .ms-info-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #0c2340;
            border: 1px solid #1f4080;
            border-radius: 20px;
            padding: 5px 14px;
            font-size: 0.8rem;
            color: #7eb3f5;
            margin: 4px 4px 4px 0;
        }

        /* ── Factor row ─────────────────────────────────────── */
        .ms-factor {
            background: #161b22;
            border: 1px solid #21262d;
            border-radius: 8px;
            padding: 10px 16px;
            margin: 5px 0;
            font-size: 0.85rem;
            color: #c9d1d9;
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }
        .ms-factor-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            flex-shrink: 0;
            margin-top: 4px;
        }
        .ms-factor-dot-red    { background: #f85149; }
        .ms-factor-dot-orange { background: #d29922; }
        .ms-factor-dot-yellow { background: #b5a31e; }
        .ms-factor-dot-blue   { background: #58a6ff; }

        /* ── Footer ─────────────────────────────────────────── */
        .ms-footer {
            text-align: center;
            color: #484f58;
            font-size: 0.75rem;
            padding: 18px 0 8px;
            border-top: 1px solid #21262d;
            margin-top: 32px;
        }

        /* ── Streamlit overrides ─────────────────────────────── */
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stSelectbox"] > div > div,
        [data-testid="stNumberInput"] input {
            background-color: #0d1117 !important;
            border: 1px solid #30363d !important;
            border-radius: 8px !important;
            color: #e6edf3 !important;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: #58a6ff !important;
            box-shadow: 0 0 0 3px rgba(88,166,255,0.15) !important;
        }
        .stButton > button {
            background: #238636 !important;
            color: #ffffff !important;
            border: 1px solid #2ea043 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 9px 22px !important;
            font-size: 0.88rem !important;
            transition: all 0.2s ease !important;
        }
        .stButton > button:hover {
            background: #2ea043 !important;
            border-color: #3fb950 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px rgba(46,160,67,0.3) !important;
        }
        .stButton > button:active { transform: translateY(0) !important; }

        /* secondary button variant */
        .ms-btn-secondary .stButton > button {
            background: #21262d !important;
            border-color: #30363d !important;
            color: #c9d1d9 !important;
        }
        .ms-btn-secondary .stButton > button:hover {
            background: #30363d !important;
            box-shadow: none !important;
        }

        div[data-testid="stFileUploader"] {
            background: #161b22 !important;
            border: 2px dashed #30363d !important;
            border-radius: 10px !important;
        }
        div[data-testid="stFileUploader"]:hover {
            border-color: #58a6ff !important;
        }

        [data-testid="stExpander"] {
            background: #161b22 !important;
            border: 1px solid #21262d !important;
            border-radius: 8px !important;
        }
        [data-testid="stExpanderToggleIcon"] { color: #58a6ff !important; }

        /* metric override */
        [data-testid="metric-container"] {
            background: #161b22;
            border: 1px solid #21262d;
            border-radius: 10px;
            padding: 14px 18px;
        }
        [data-testid="stMetricValue"] { color: #58a6ff !important; }
        [data-testid="stMetricLabel"] { color: #8b949e !important; }

        /* alert overrides */
        [data-testid="stAlert"] {
            border-radius: 8px !important;
        }

        /* progress bar */
        [data-testid="stProgressBar"] > div > div {
            border-radius: 6px !important;
        }

        /* hide default streamlit branding */
        #MainMenu, footer, header { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Session state initialisation
# ══════════════════════════════════════════════════════════════════════════════

def _init_session_state() -> None:
    defaults: dict = {
        # Tab 1 — Interaction Checker
        "ic_medicines_input": "",
        "ic_results": None,          # list[str] of interaction strings
        "ic_found": None,            # list[tuple[str, str]]
        "ic_not_found": None,        # list[str]
        "ic_ai_summary": "",
        # Tab 2 — Prescription OCR
        "ocr_raw_text": "",
        "ocr_parsed": None,          # dict from LLM
        "ocr_interactions": None,    # list[str]
        "ocr_filename": "",
        # Tab 3 — Symptom & Doubt Solver
        "sym_input": "",
        "sym_advice": "",
        "sym_ai": "",
        # Tab 4 — Side-Effect Monitor
        "se_age": 25,
        "se_gender": "Male",
        "se_medicines": "",
        "se_doses": "",
        "se_experience": "",
        "se_duration": "1–3 days",
        "se_results": None,          # dict with keys: profiles, ai_analysis, urgent
        # Tab 5 — Emergency Risk Predictor
        "er_age": 65,
        "er_gender": "Male",
        "er_medicines": "",
        "er_symptoms": "",
        "er_conditions": "",
        "er_result": None,           # dict from calculate_risk_score
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


# ══════════════════════════════════════════════════════════════════════════════
#  AI helpers  (Groq)
# ══════════════════════════════════════════════════════════════════════════════

# Simple in-process cache: keyed on (prompt, max_tokens) to avoid duplicate
# API calls when the same analysis is triggered multiple times in one session.
_ai_cache: dict[tuple, str] = {}


def _ollama_chat(prompt: str, max_tokens: int = 350, temperature: float = 0.35) -> str:
    cache_key = (prompt, max_tokens)
    if cache_key in _ai_cache:
        _logger.info("AI cache hit (max_tokens=%d, prompt_len=%d)", max_tokens, len(prompt))
        return _ai_cache[cache_key]
    t0 = time.perf_counter()
    try:
        response = _groq_client.chat.completions.create(
            model=_GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        result = response.choices[0].message.content.strip()
        elapsed = time.perf_counter() - t0
        _logger.info("Groq inference %.2fs (max_tokens=%d, prompt_len=%d)", elapsed, max_tokens, len(prompt))
        _ai_cache[cache_key] = result
        return result
    except Exception as exc:
        _logger.error("Groq API error: %s", exc)
        return f"⚠️ AI response unavailable — check your GROQ_API_KEY. Error: {exc}"


def _ai_interaction_summary(interactions: list[str]) -> str:
    prompt = (
        "You are a clinical pharmacist assistant (educational purposes only).\n"
        "Based on the drug interaction notes below, write a clear 2–3 sentence "
        "educational summary of the most important safety concern. "
        "Do NOT provide clinical diagnosis. Be factual and non-alarmist.\n\n"
        "Notes:\n" + "\n".join(f"- {i}" for i in interactions) + "\n\nSummary:"
    )
    return _ollama_chat(prompt, max_tokens=220, temperature=0.3)


def _ai_parse_prescription(ocr_text: str) -> dict:
    prompt = (
        "You are a medical data extraction assistant.\n"
        "Extract all medicine names and their active drug/salt components from "
        "the prescription text below.\n\n"
        "Respond with ONLY a raw JSON object — absolutely no markdown, no code fences, "
        "no explanation text before or after:\n"
        '{"medicines": [{"name": "...", "salt": "...", "dosage": "..."}]}\n\n'
        "Use null for missing fields. Return empty array if no medicines found.\n\n"
        f"Prescription text:\n{ocr_text}\n\nJSON:"
    )
    raw = _ollama_chat(prompt, max_tokens=700, temperature=0.1)

    # Strip markdown code fences Groq sometimes wraps the response in
    cleaned = re.sub(r"```(?:json)?\s*", "", raw).strip()
    cleaned = cleaned.replace("```", "").strip()

    start, end = cleaned.find("{"), cleaned.rfind("}") + 1
    if start != -1 and end > start:
        try:
            return json.loads(cleaned[start:end])
        except json.JSONDecodeError:
            pass

    # Fallback: scan OCR words directly against MED_DB with fuzzy matching
    medicines_found = []
    seen_keys: set[str] = set()
    words = re.findall(r"[A-Za-z]+", ocr_text)
    for word in words:
        if len(word) < 4:
            continue
        key = find_medicine(word)
        if key and key not in seen_keys:
            seen_keys.add(key)
            medicines_found.append({"name": MED_DB[key]["name"], "salt": None, "dosage": None})
    if medicines_found:
        return {"medicines": medicines_found, "_source": "fuzzy_fallback"}

    return {"medicines": [], "_parse_error": "Could not extract valid JSON from AI response."}


def _ai_symptom_explanation(symptom: str, rule_advice: str) -> str:
    prompt = (
        f'A patient describes: "{symptom}".\n\n'
        f"Basic guidance provided:\n{rule_advice}\n\n"
        "Write a friendly, educational explanation (3–4 sentences) covering:\n"
        "1. Why the suggested remedies work.\n"
        "2. One lifestyle or dietary consideration.\n"
        "3. When professional care becomes essential.\n\n"
        'End with: "Always consult a healthcare professional for personalised advice."\n\n'
        "Explanation:"
    )
    return _ollama_chat(prompt, max_tokens=400, temperature=0.4)


def _ai_side_effect_analysis(
    age: int, gender: str, medicines: list[str],
    doses: list[str], experience: str, duration: str,
) -> str:
    profiles: list[str] = []
    for i, med in enumerate(medicines):
        key = find_medicine(med)
        if key:
            se = MED_DB[key].get("side_effects", [])
            dose_info = doses[i] if i < len(doses) else "not specified"
            profiles.append(
                f"- {MED_DB[key]['name']} (dose: {dose_info} mg): {', '.join(se[:5])}"
            )
    profile_text = "\n".join(profiles) if profiles else "No medicines matched in database."
    prompt = (
        f"Educational pharmacist assistant.\n"
        f"Patient — Age: {age}, Gender: {gender}.\n"
        f'Reports: "{experience}" (duration: {duration}).\n\n'
        f"Side-effect profiles:\n{profile_text}\n\n"
        "Write an educational analysis (3–4 sentences):\n"
        "1. Which experience may relate to which medicine.\n"
        "2. A non-prescription management suggestion.\n"
        "3. Clear trigger for contacting a doctor.\n\n"
        "EDUCATIONAL ONLY — not a medical diagnosis.\n\nAnalysis:"
    )
    return _ollama_chat(prompt, max_tokens=450, temperature=0.35)


# ══════════════════════════════════════════════════════════════════════════════
#  Shared helpers
# ══════════════════════════════════════════════════════════════════════════════

def _parse_medicine_list(raw: str) -> list[str]:
    """Accept comma-separated or newline-separated medicine names."""
    if not raw.strip():
        return []
    if "," in raw:
        return [m.strip() for m in raw.split(",") if m.strip()]
    return [m.strip() for m in raw.splitlines() if m.strip()]


def _check_interactions(medicines: list[str]) -> tuple[list[tuple[str, str]], list[str], list[str]]:
    """
    Resolve medicines and detect interactions.
    Returns: found (list of (input, db_key)), not_found (list), interactions (list of str).
    """
    found: list[tuple[str, str]] = []
    not_found: list[str] = []
    for med in medicines:
        key = find_medicine(med)
        if key:
            if key not in [f[1] for f in found]:
                found.append((med, key))
        else:
            not_found.append(med)

    results: set[str] = set()
    keys_list = [f[1] for f in found]
    for source_key in keys_list:
        db_ints = MED_DB[source_key].get("interactions", {})
        for target_key in keys_list:
            if target_key == source_key:
                continue
            target_lower = MED_DB[target_key]["name"].lower()
            for int_name, severity in db_ints.items():
                s1 = fuzz.token_sort_ratio(int_name.lower(), target_key.lower())
                s2 = fuzz.token_sort_ratio(int_name.lower(), target_lower)
                if max(s1, s2) >= 70:
                    results.add(
                        f"**{MED_DB[source_key]['name']}** ↔ "
                        f"**{MED_DB[target_key]['name']}**: {severity}"
                    )
                    break
    return found, not_found, sorted(results)


def _render_interaction_cards(interactions: list[str]) -> None:
    for item in interactions:
        is_critical = "High" in item
        css_class = "ms-interaction-critical" if is_critical else "ms-interaction"
        st.markdown(f'<div class="{css_class}">⚠️ {item}</div>', unsafe_allow_html=True)


def _render_medicine_chips(found: list[tuple[str, str]], not_found: list[str]) -> None:
    html = ""
    for _, key in found:
        html += f'<span class="ms-chip-found">✓ {MED_DB[key]["name"]}</span>'
    for name in not_found:
        html += f'<span class="ms-chip-notfound">✗ {name}</span>'
    st.markdown(html, unsafe_allow_html=True)


def _render_ai_box(text: str) -> None:
    st.markdown(
        f'<div class="ms-ai-box">🤖 <strong>AI Enhanced Advice:</strong> {text}</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  App Header
# ══════════════════════════════════════════════════════════════════════════════

def _render_header() -> None:
    st.markdown(
        """
        <div class="ms-header">
            <div class="ms-header-icon">🩺</div>
            <div>
                <p class="ms-header-title">MedSafe AI – Intelligent Medicine Safety Assistant</p>
                <p class="ms-header-sub">
                    AI-powered medicine safety checker for educational use &nbsp;·&nbsp;
                    Powered by LLaMA 3 &nbsp;·&nbsp; Not a substitute for professional medical advice
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  Tab 1 — Medicine Interaction Checker
# ══════════════════════════════════════════════════════════════════════════════

def _tab_interaction_checker() -> None:
    st.markdown(
        '<div class="ms-tab-header">'
        '<span style="font-size:1.5rem">💊</span>'
        '<p class="ms-tab-title">Medicine Interaction Checker</p>'
        f'<span class="ms-tab-badge">{len(MED_DB)} medicines in database</span>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Enter the medicines you are taking to identify known drug–drug interactions "
        "and receive an AI-assisted safety summary."
    )
    st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

    # ── Input card ────────────────────────────────────────────────────────
    st.markdown('<div class="ms-card">', unsafe_allow_html=True)
    st.markdown('<p class="ms-card-title">🔍 Enter Medicines</p>', unsafe_allow_html=True)

    col_input, col_hint = st.columns([3, 1])
    with col_input:
        med_input = st.text_area(
            "Enter medicines (comma-separated or one per line):",
            value=st.session_state.ic_medicines_input,
            placeholder="e.g.  Warfarin, Aspirin, Atorvastatin, Metoprolol",
            height=110,
            key="ic_med_textarea",
            help="Accepts generic names, brand names, or common spelling variations.",
        )
    with col_hint:
        st.markdown(
            '<br>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="ms-info-pill">💡 Fuzzy matching enabled</div>'
            '<div class="ms-info-pill">🔒 Local analysis</div>'
            '<div class="ms-info-pill">🌐 AI summary via Groq</div>',
            unsafe_allow_html=True,
        )

    col_btn, col_clear = st.columns([1, 5])
    with col_btn:
        check_btn = st.button("🔍 Check Interactions", type="primary", key="ic_check_btn")
    with col_clear:
        with st.container():
            st.markdown('<div class="ms-btn-secondary">', unsafe_allow_html=True)
            if st.button("✕ Clear", key="ic_clear_btn"):
                st.session_state.ic_medicines_input = ""
                st.session_state.ic_results = None
                st.session_state.ic_found = None
                st.session_state.ic_not_found = None
                st.session_state.ic_ai_summary = ""
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close ms-card

    # ── Validation & processing ───────────────────────────────────────────
    if check_btn:
        medicines = _parse_medicine_list(med_input)
        if not medicines:
            st.error("⛔ Please enter at least one medicine name before checking.")
        elif len(medicines) < 2:
            st.warning(
                "⚠️ Please enter **at least 2 medicines** to detect interactions. "
                "Single-medicine details will still be shown."
            )
            found, not_found, _ = _check_interactions(medicines)
            st.session_state.ic_medicines_input = med_input
            st.session_state.ic_found = found
            st.session_state.ic_not_found = not_found
            st.session_state.ic_results = []
            st.session_state.ic_ai_summary = ""
        else:
            with st.spinner("🔬 Analysing interactions…"):
                found, not_found, interactions = _check_interactions(medicines)
            st.session_state.ic_medicines_input = med_input
            st.session_state.ic_found = found
            st.session_state.ic_not_found = not_found
            st.session_state.ic_results = interactions
            # AI summary only if interactions found
            if interactions:
                with st.spinner("🤖 Generating AI safety summary…"):
                    st.session_state.ic_ai_summary = _ai_interaction_summary(interactions)
            else:
                st.session_state.ic_ai_summary = ""

    # ── Results (persisted in session state) ──────────────────────────────
    if st.session_state.ic_found is not None:
        st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

        # Recognised / unrecognised chips
        st.markdown("**Medicines Recognised:**")
        _render_medicine_chips(st.session_state.ic_found, st.session_state.ic_not_found)

        if st.session_state.ic_not_found:
            st.warning(
                f"⚠️ Could not match: **{', '.join(st.session_state.ic_not_found)}**. "
                "Try the generic/active-ingredient name."
            )

        interactions = st.session_state.ic_results or []

        st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

        # Metrics row
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Medicines Matched", len(st.session_state.ic_found))
        col_m2.metric("Interactions Found", len(interactions))
        severity_high = sum(1 for i in interactions if "High" in i)
        col_m3.metric("High-Severity Alerts", severity_high)

        # Interaction cards
        if interactions:
            st.markdown(f"#### ⚠️ {len(interactions)} Interaction(s) Detected")
            _render_interaction_cards(interactions)

            if st.session_state.ic_ai_summary:
                st.markdown("<br>", unsafe_allow_html=True)
                _render_ai_box(st.session_state.ic_ai_summary)
        elif st.session_state.ic_results is not None:
            st.success(
                "✅ **No major interactions detected** between the identified medicines "
                "in our database.\n\n"
                "_Absence of a result does not guarantee safety — always consult your "
                "pharmacist or prescriber._"
            )

        # Medicine detail expanders
        if st.session_state.ic_found:
            st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)
            st.markdown("#### 📋 Detailed Medicine Profiles")
            for _, key in st.session_state.ic_found:
                data = MED_DB[key]
                with st.expander(f"💊 {data['name']}  ·  {data.get('category', 'N/A')}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        adult = data["standard_dose_mg"].get("adult")
                        ped = data["standard_dose_mg"].get("pediatric")
                        st.markdown(
                            f"**Standard Adult Dose:** "
                            f"{'–' if adult is None else str(adult) + ' mg'}"
                        )
                        st.markdown(
                            f"**Paediatric Dose:** "
                            f"{'–' if ped is None else str(ped) + ' mg'}"
                        )
                        se = data.get("side_effects", [])
                        if se:
                            st.markdown(f"**Common Side Effects:** {', '.join(se[:5])}")
                    with c2:
                        ci = data.get("contraindications", [])
                        if ci:
                            st.markdown(f"**Contraindications:** {', '.join(ci)}")
                        n_ints = len(data.get("interactions", {}))
                        st.markdown(f"**Documented Interactions:** {n_ints} in database")


# ══════════════════════════════════════════════════════════════════════════════
#  Tab 2 — Prescription OCR
# ══════════════════════════════════════════════════════════════════════════════

def _tab_prescription_ocr() -> None:
    st.markdown(
        '<div class="ms-tab-header">'
        '<span style="font-size:1.5rem">📋</span>'
        '<p class="ms-tab-title">Extract Medicines From Prescription Image</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Upload a prescription image. Tesseract OCR extracts raw text; "
        "Groq AI then identifies medicines, salts, and dosages as structured JSON."
    )
    st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

    col_upload, col_preview = st.columns([1, 1])

    with col_upload:
        st.markdown('<div class="ms-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="ms-card-title">📤 Upload Prescription Image</p>',
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader(
            "Upload prescription image",
            type=["png", "jpg", "jpeg", "bmp", "tiff"],
            key="ocr_upload",
            label_visibility="collapsed",
            help="Accepts JPG, PNG, JPEG, BMP, TIFF. Max 200 MB.",
        )
        st.caption("Drag and drop here · Limit 200 MB per file · JPG, PNG, JPEG")
        st.markdown("</div>", unsafe_allow_html=True)

        if uploaded:
            extract_btn = st.button(
                "📄 Extract & Analyse", type="primary", key="ocr_extract_btn"
            )
            if st.button("✕ Clear Results", key="ocr_clear_btn"):
                st.session_state.ocr_raw_text = ""
                st.session_state.ocr_parsed = None
                st.session_state.ocr_interactions = None
                st.session_state.ocr_filename = ""
                st.rerun()
        else:
            extract_btn = False

    with col_preview:
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption=f"📎 {uploaded.name}", use_container_width=True)
        else:
            st.markdown(
                '<div class="ms-card" style="min-height:200px">'
                '<p class="ms-card-title">📌 How it works</p>'
                '<ol style="color:#8b949e; font-size:0.85rem; line-height:2">'
                '<li>Upload a clear prescription image (JPG/PNG).</li>'
                '<li>Tesseract OCR extracts raw text from the image.</li>'
                '<li>LLaMA 3 parses the text into structured medicine data.</li>'
                '<li>Identified medicines are checked against the safety database.</li>'
                '<li>An interaction check runs automatically if ≥ 2 medicines are found.</li>'
                '</ol>'
                '</div>',
                unsafe_allow_html=True,
            )

    # ── Processing ────────────────────────────────────────────────────────
    if extract_btn and uploaded:
        image = Image.open(uploaded)
        with st.spinner("📄 Running OCR extraction…"):
            t_ocr = time.perf_counter()
            ocr_text = extract_text_from_image(image)
            _logger.info("OCR UI call completed in %.2fs for '%s'", time.perf_counter() - t_ocr, uploaded.name)

        if ocr_text.startswith("OCR Error"):
            st.error(f"⛔ {ocr_text}")
            st.info(
                "💡 **Tip:** Ensure Tesseract OCR is installed and the path in "
                "`ocr_utils.py` matches your installation directory."
            )
        else:
            st.session_state.ocr_raw_text = ocr_text
            st.session_state.ocr_filename = uploaded.name

            with st.spinner("🤖 Parsing medicines with LLaMA 3…"):
                parsed = _ai_parse_prescription(ocr_text)
            st.session_state.ocr_parsed = parsed

            med_names = [
                m.get("name", "")
                for m in parsed.get("medicines", [])
                if m.get("name")
            ]
            if len(med_names) >= 2:
                with st.spinner("🔬 Running interaction check…"):
                    _, _, interactions = _check_interactions(med_names)
                st.session_state.ocr_interactions = interactions
            else:
                st.session_state.ocr_interactions = None

    # ── Results ───────────────────────────────────────────────────────────
    if st.session_state.ocr_raw_text:
        st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

        # Raw OCR text
        with st.expander("📄 Raw OCR Text", expanded=False):
            st.text_area(
                "Extracted text:",
                value=st.session_state.ocr_raw_text,
                height=180,
                key="ocr_raw_display",
                disabled=True,
            )

        # Parsed medicines
        parsed = st.session_state.ocr_parsed or {}
        medicines_list = parsed.get("medicines", [])

        col_summary, col_json = st.columns([3, 2])
        with col_summary:
            st.markdown("#### 🧪 Identified Medicines")
            if not medicines_list:
                st.warning(
                    "⚠️ No medicines could be identified. "
                    "Try a clearer image or review the raw OCR output above."
                )
            else:
                for med in medicines_list:
                    name = med.get("name") or "Unknown"
                    salt = med.get("salt") or "N/A"
                    dosage = med.get("dosage") or "Not specified"
                    db_key = find_medicine(name) if name != "Unknown" else None
                    with st.expander(f"💊 {name}", expanded=True):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown(f"**Active Salt:** {salt}")
                            st.markdown(f"**Dosage:** {dosage}")
                        with c2:
                            if db_key:
                                st.success(f"✅ Matched: {MED_DB[db_key]['name']}")
                                se = MED_DB[db_key].get("side_effects", [])
                                if se:
                                    st.caption(f"Side effects: {', '.join(se[:3])}")
                            else:
                                st.warning("⚠️ Not in local database")

        with col_json:
            st.markdown("#### 🔧 Structured JSON Output")
            with st.expander("View raw JSON", expanded=True):
                st.json(parsed)

        # Interaction check for prescription
        if st.session_state.ocr_interactions is not None:
            st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Prescription Interaction Check")
            if st.session_state.ocr_interactions:
                st.error(
                    f"🚨 {len(st.session_state.ocr_interactions)} "
                    "interaction(s) detected on this prescription:"
                )
                _render_interaction_cards(st.session_state.ocr_interactions)
            else:
                st.success("✅ No major interactions detected between identified medicines.")

        st.caption(
            f"File: {st.session_state.ocr_filename}  ·  "
            f"Analysed: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  Tab 3 — Symptom & Doubt Solver
# ══════════════════════════════════════════════════════════════════════════════

def _tab_symptom_solver() -> None:
    st.markdown(
        '<div class="ms-tab-header">'
        '<span style="font-size:1.5rem">🌡️</span>'
        '<p class="ms-tab-title">Symptom &amp; Doubt Solver</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Describe your symptom to receive rule-based guidance complemented by an "
        "AI-generated educational explanation."
    )
    st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="ms-card">', unsafe_allow_html=True)
        st.markdown('<p class="ms-card-title">🔍 Describe Your Symptom</p>', unsafe_allow_html=True)

        symptom_input = st.text_input(
            "Enter your symptom:",
            value=st.session_state.sym_input,
            placeholder="e.g., I have a runny nose with sneezing and slight fever since yesterday",
            key="sym_text_input",
            help="Be descriptive — duration, severity, and associated symptoms improve response quality.",
        )
        use_ai = st.checkbox(
            "✨ Enhance with AI explanation (requires Groq API)",
            value=True,
            key="sym_use_ai",
        )

        col_btn, col_clr = st.columns([2, 3])
        with col_btn:
            analyse_btn = st.button("🔍 Analyse Symptom", type="primary", key="sym_analyse_btn")
        with col_clr:
            st.markdown('<div class="ms-btn-secondary">', unsafe_allow_html=True)
            if st.button("✕ Clear", key="sym_clear_btn"):
                st.session_state.sym_input = ""
                st.session_state.sym_advice = ""
                st.session_state.sym_ai = ""
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown(
            '<div class="ms-card">'
            '<p class="ms-card-title">📖 Quick Reference</p>'
            '<p style="color:#8b949e; font-size:0.82rem; margin-bottom:10px">'
            'Click a category for instant guidance:</p>',
            unsafe_allow_html=True,
        )
        _QUICK = [
            ("🤧", "Cold / Runny Nose", "cold"),
            ("🌡️", "Fever", "fever"),
            ("💧", "Diarrhea", "diarrhea"),
            ("🤕", "Headache", "headache"),
            ("😮", "Cough", "cough"),
            ("🤢", "Nausea", "nausea"),
            ("🔴", "Skin Rash", "rash"),
            ("🦴", "Joint Pain", "joint pain"),
            ("💫", "Dizziness", "dizziness"),
            ("🚨", "Chest Pain", "chest pain"),
        ]
        cols = st.columns(2)
        for idx, (icon, label, kw) in enumerate(_QUICK):
            with cols[idx % 2]:
                if st.button(f"{icon} {label}", key=f"quick_{kw.replace(' ','_')}"):
                    st.session_state.sym_input = kw
                    st.session_state.sym_advice = symptom_advice(kw)
                    st.session_state.sym_ai = ""
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Processing ────────────────────────────────────────────────────────
    if analyse_btn:
        if not symptom_input.strip():
            st.error("⛔ Please describe your symptom before clicking Analyse.")
        else:
            st.session_state.sym_input = symptom_input
            with st.spinner("🔬 Analysing symptom…"):
                advice = symptom_advice(symptom_input)
            st.session_state.sym_advice = advice

            if use_ai:
                with st.spinner("🤖 Generating AI explanation…"):
                    st.session_state.sym_ai = _ai_symptom_explanation(symptom_input, advice)
            else:
                st.session_state.sym_ai = ""

    # ── Results ───────────────────────────────────────────────────────────
    if st.session_state.sym_advice:
        st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)
        col_advice, col_ai = st.columns([1, 1])

        with col_advice:
            st.markdown("#### 📋 Guidance")
            st.markdown(
                f'<div class="ms-card">{st.session_state.sym_advice}</div>',
                unsafe_allow_html=True,
            )
            st.caption(
                f"Analysed: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ·  "
                "Rule-based + educational only"
            )

        with col_ai:
            if st.session_state.sym_ai:
                st.markdown("#### 🤖 AI Enhanced Advice")
                _render_ai_box(st.session_state.sym_ai)


# ══════════════════════════════════════════════════════════════════════════════
#  Tab 4 — Side-Effect Monitor
# ══════════════════════════════════════════════════════════════════════════════

def _tab_side_effect_monitor() -> None:
    st.markdown(
        '<div class="ms-tab-header">'
        '<span style="font-size:1.5rem">⚠️</span>'
        '<p class="ms-tab-title">Experience &amp; Side-Effect Monitor</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Report what you are experiencing. An AI-assisted educational analysis will "
        "help identify potential medicine side effects based on your profile."
    )
    st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

    # ── Input form ────────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="ms-card">', unsafe_allow_html=True)
        st.markdown('<p class="ms-card-title">👤 Patient Profile</p>', unsafe_allow_html=True)

        se_age = st.number_input(
            "Enter your age:",
            min_value=0,
            max_value=120,
            value=st.session_state.se_age,
            step=1,
            key="se_age_input",
        )
        se_gender = st.selectbox(
            "Select your gender:",
            options=["Male", "Female", "Other / Prefer not to say"],
            index=["Male", "Female", "Other / Prefer not to say"].index(
                st.session_state.se_gender
            ),
            key="se_gender_input",
        )
        se_meds = st.text_input(
            "Enter medicine(s) taken (comma-separated):",
            value=st.session_state.se_medicines,
            placeholder="e.g.  Atorvastatin, Metformin, Lisinopril",
            key="se_meds_input",
        )
        se_doses = st.text_input(
            "Enter dose(s) taken in mg (comma-separated if multiple):",
            value=st.session_state.se_doses,
            placeholder="e.g.  10, 500, 10",
            key="se_doses_input",
            help="Enter doses in the same order as the medicines above.",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="ms-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="ms-card-title">📝 Reported Experience</p>', unsafe_allow_html=True
        )
        se_experience = st.text_area(
            "Describe what you are experiencing:",
            value=st.session_state.se_experience,
            placeholder=(
                "e.g., I have been experiencing muscle aches and weakness in my legs "
                "since starting Atorvastatin three days ago…"
            ),
            height=130,
            key="se_experience_input",
        )
        se_duration = st.selectbox(
            "How long have you experienced this?",
            options=["< 24 hours", "1–3 days", "4–7 days", "1–2 weeks", "> 2 weeks"],
            index=["< 24 hours", "1–3 days", "4–7 days", "1–2 weeks", "> 2 weeks"].index(
                st.session_state.se_duration
            ),
            key="se_duration_input",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    col_btn, col_clr = st.columns([2, 5])
    with col_btn:
        se_btn = st.button("🔍 Analyse Side Effects", type="primary", key="se_analyse_btn")
    with col_clr:
        st.markdown('<div class="ms-btn-secondary">', unsafe_allow_html=True)
        if st.button("✕ Clear", key="se_clear_btn"):
            for k in ("se_medicines", "se_doses", "se_experience"):
                st.session_state[k] = ""
            st.session_state.se_results = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Validation ────────────────────────────────────────────────────────
    if se_btn:
        errors: list[str] = []
        if se_age < 0 or se_age > 120:
            errors.append("Age must be between 0 and 120.")
        if not se_meds.strip():
            errors.append("Please enter at least one medicine name.")
        if not se_experience.strip():
            errors.append("Please describe what you are experiencing.")

        if errors:
            for e in errors:
                st.error(f"⛔ {e}")
        else:
            # Persist inputs
            st.session_state.se_age = se_age
            st.session_state.se_gender = se_gender
            st.session_state.se_medicines = se_meds
            st.session_state.se_doses = se_doses
            st.session_state.se_experience = se_experience
            st.session_state.se_duration = se_duration

            medicines = _parse_medicine_list(se_meds)
            doses = [d.strip() for d in se_doses.split(",") if d.strip()]

            # Urgent keyword flag
            urgent_kws = [
                "chest pain", "difficulty breathing", "throat swelling",
                "face swelling", "anaphylaxis", "severe bleeding",
                "loss of consciousness", "seizure", "vision loss",
            ]
            urgent = any(kw in se_experience.lower() for kw in urgent_kws)

            # Build side-effect profiles from DB
            profiles: list[dict] = []
            unmatched: list[str] = []
            for med in medicines:
                key = find_medicine(med)
                if key:
                    profiles.append({"key": key, "data": MED_DB[key]})
                else:
                    unmatched.append(med)

            with st.spinner("🤖 Generating AI side-effect analysis…"):
                ai_analysis = _ai_side_effect_analysis(
                    int(se_age), se_gender, medicines, doses, se_experience, se_duration
                )

            # Log side-effect report for audit trail
            _logger.info(
                "Side-effect report — age=%s gender=%s medicines=%s duration=%s experience=%r urgent=%s",
                se_age, se_gender, medicines, se_duration, se_experience[:120], urgent
            )

            st.session_state.se_results = {
                "profiles": profiles,
                "unmatched": unmatched,
                "ai_analysis": ai_analysis,
                "urgent": urgent,
                "medicines": medicines,
                "duration": se_duration,
            }

    # ── Results ───────────────────────────────────────────────────────────
    res = st.session_state.se_results
    if res:
        st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

        if res["urgent"]:
            st.error(
                "🚨 **Possible Serious Adverse Reaction Detected**\n\n"
                "The symptoms you described may indicate a severe or life-threatening "
                "adverse drug reaction. **Contact your healthcare provider or emergency "
                "services immediately.**"
            )

        # AI analysis
        st.markdown("#### 🤖 AI Side-Effect Analysis")
        _render_ai_box(res["ai_analysis"])

        # DB profiles
        st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)
        st.markdown("#### 📊 Medicine Side-Effect Profiles")

        if res["profiles"]:
            for profile in res["profiles"]:
                data = profile["data"]
                se_list = data.get("side_effects", [])
                ci_list = data.get("contraindications", [])
                with st.expander(
                    f"💊 {data['name']}  ·  {data.get('category', 'N/A')}", expanded=True
                ):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(
                            "**Known Side Effects:**\n"
                            + "\n".join(f"- {s}" for s in se_list)
                        )
                    with c2:
                        if ci_list:
                            st.markdown(
                                "**Contraindications:**\n"
                                + "\n".join(f"- {c}" for c in ci_list)
                            )

        if res["unmatched"]:
            st.warning(
                f"⚠️ Not found in database: **{', '.join(res['unmatched'])}**. "
                "Try the generic name."
            )

        st.caption(
            f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ·  "
            f"Duration reported: {res['duration']}"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  Tab 5 — Emergency Risk Predictor
# ══════════════════════════════════════════════════════════════════════════════

def _tab_risk_predictor() -> None:
    st.markdown(
        '<div class="ms-tab-header">'
        '<span style="font-size:1.5rem">🚨</span>'
        '<p class="ms-tab-title">Emergency Risk Predictor</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Calculates a transparent, rule-based emergency risk score (0–100) from "
        "patient demographics, medication burden, current symptoms, and known conditions."
    )
    st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

    # ── Input form ────────────────────────────────────────────────────────
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="ms-card">', unsafe_allow_html=True)
        st.markdown('<p class="ms-card-title">👤 Patient Details</p>', unsafe_allow_html=True)
        er_age = st.number_input(
            "Age:",
            min_value=0,
            max_value=120,
            value=st.session_state.er_age,
            step=1,
            key="er_age_input",
        )
        er_gender = st.selectbox(
            "Gender:",
            options=["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(st.session_state.er_gender),
            key="er_gender_input",
        )
        er_meds = st.text_area(
            "Current Medicines (one per line or comma-separated):",
            value=st.session_state.er_medicines,
            placeholder="e.g.\nWarfarin\nAspirin\nAtorvastatin\nMetoprolol",
            height=120,
            key="er_meds_input",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="ms-card">', unsafe_allow_html=True)
        st.markdown(
            '<p class="ms-card-title">🩺 Clinical Picture</p>', unsafe_allow_html=True
        )
        er_symptoms = st.text_area(
            "Current Symptoms (one per line):",
            value=st.session_state.er_symptoms,
            placeholder="e.g.\nchest pain\nshortness of breath\ndizziness",
            height=100,
            key="er_symptoms_input",
        )
        er_conditions = st.text_area(
            "Known Medical Conditions (one per line):",
            value=st.session_state.er_conditions,
            placeholder="e.g.\ndiabetes\nhypertension\nheart failure\nCKD",
            height=100,
            key="er_conditions_input",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    col_btn, col_clr = st.columns([2, 5])
    with col_btn:
        er_btn = st.button("🚨 Calculate Risk Score", type="primary", key="er_calc_btn")
    with col_clr:
        st.markdown('<div class="ms-btn-secondary">', unsafe_allow_html=True)
        if st.button("✕ Clear", key="er_clear_btn"):
            for k in ("er_medicines", "er_symptoms", "er_conditions"):
                st.session_state[k] = ""
            st.session_state.er_result = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Validation ────────────────────────────────────────────────────────
    if er_btn:
        errors: list[str] = []
        if not er_meds.strip() and not er_symptoms.strip():
            errors.append(
                "Please enter at least one medicine or symptom to calculate a meaningful risk score."
            )
        if errors:
            for e in errors:
                st.error(f"⛔ {e}")
        else:
            st.session_state.er_age = er_age
            st.session_state.er_gender = er_gender
            st.session_state.er_medicines = er_meds
            st.session_state.er_symptoms = er_symptoms
            st.session_state.er_conditions = er_conditions

            medicines = _parse_medicine_list(er_meds)
            symptoms = [s.strip() for s in er_symptoms.splitlines() if s.strip()]
            conditions = [c.strip() for c in er_conditions.splitlines() if c.strip()]

            with st.spinner("🔬 Calculating risk score…"):
                t_risk = time.perf_counter()
                result = calculate_risk_score(
                    age=int(er_age),
                    gender=er_gender,
                    medicines=medicines,
                    symptoms=symptoms,
                    conditions=conditions,
                )
                _logger.info(
                    "Risk score calculated in %.3fs — score=%d level=%s medicines=%s",
                    time.perf_counter() - t_risk, result["score"], result["level"], medicines
                )
            st.session_state.er_result = result

    # ── Results ───────────────────────────────────────────────────────────
    result = st.session_state.er_result
    if result:
        st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)

        score = result["score"]
        color = result["color"]
        level = result["level"]
        recommendation = result["recommendation"]

        # ── Visual risk gauge ─────────────────────────────────────────
        css_class_map = {
            "red": "ms-risk-critical",
            "orange": "ms-risk-high",
            "yellow": "ms-risk-moderate",
            "green": "ms-risk-low",
        }
        gauge_class = css_class_map.get(color, "ms-risk-low")

        col_gauge, col_details = st.columns([1, 2])
        with col_gauge:
            st.markdown(
                f'<div class="ms-risk-gauge {gauge_class}">'
                f'<div class="ms-risk-number">{score}</div>'
                f'<div style="font-size:0.75rem; color:#8b949e; margin:4px 0">out of 100</div>'
                f'<div class="ms-risk-label">{level}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            # progress bar (color via st.progress note: limited native styling)
            st.progress(score / 100)

        with col_details:
            st.markdown("#### 📋 Recommendation")
            if color == "red":
                st.error(f"🚨 {recommendation}")
            elif color == "orange":
                st.warning(f"⚠️ {recommendation}")
            elif color == "yellow":
                st.warning(f"⚠️ {recommendation}")
            else:
                st.success(f"✅ {recommendation}")

            # Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Risk Score", f"{score}/100")
            c2.metric("Medicines Matched", len(result.get("resolved_medicines", [])))
            c3.metric(
                "Dangerous Combos",
                len(result.get("warnings", [])),
                delta="⚠️ Alert" if result.get("warnings") else None,
                delta_color="inverse",
            )

        # Dangerous combinations
        if result.get("warnings"):
            st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)
            st.markdown("#### 🚨 Dangerous Drug Combinations Detected")
            for w in result["warnings"]:
                st.markdown(
                    f'<div class="ms-interaction-critical">🚨 {w}</div>',
                    unsafe_allow_html=True,
                )

        # Risk factor breakdown
        st.markdown('<hr class="ms-divider"/>', unsafe_allow_html=True)
        st.markdown("#### 📊 Risk Factor Breakdown")

        factors = result.get("factors", [])
        if factors:
            for factor in factors:
                pts_text = ""
                dot_class = "ms-factor-dot-blue"
                if "+30" in factor or "+35" in factor or "+40" in factor or "+20" in factor:
                    dot_class = "ms-factor-dot-red"
                elif "+15" in factor or "+12" in factor:
                    dot_class = "ms-factor-dot-orange"
                elif "+8" in factor or "+10" in factor:
                    dot_class = "ms-factor-dot-yellow"
                st.markdown(
                    f'<div class="ms-factor">'
                    f'<div class="ms-factor-dot {dot_class}"></div>'
                    f'<span>{factor}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.success("No significant risk factors identified from the provided information.")

        # Resolved medicines expander
        resolved = result.get("resolved_medicines", [])
        if resolved:
            with st.expander(f"💊 {len(resolved)} Medicine(s) Matched in Database"):
                for key in resolved:
                    st.markdown(
                        f"• **{MED_DB[key]['name']}** · "
                        f"_{MED_DB[key].get('category', 'N/A')}_"
                    )

        st.caption(
            f"Assessment generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  ·  "
            "Educational use only — not a clinical risk tool"
        )


# ══════════════════════════════════════════════════════════════════════════════
#  Main application
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    _inject_css()
    _init_session_state()
    _render_header()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💊 Medicine Interaction Checker",
        "📋 Prescription OCR",
        "🌡️ Symptom & Doubt Solver",
        "⚠️ Side-Effect Monitor",
        "🚨 Emergency Risk Predictor",
    ])

    with tab1:
        _tab_interaction_checker()
    with tab2:
        _tab_prescription_ocr()
    with tab3:
        _tab_symptom_solver()
    with tab4:
        _tab_side_effect_monitor()
    with tab5:
        _tab_risk_predictor()

    # Footer
    st.markdown(
        f'<div class="ms-footer">'
        f'MedSafe AI v1.0 &nbsp;·&nbsp; Educational Use Only &nbsp;·&nbsp; '
        f'© {datetime.now().year} &nbsp;·&nbsp; '
        f'Not a substitute for professional medical advice'
        f'</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
