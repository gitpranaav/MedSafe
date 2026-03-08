# risk_engine.py — MedSafe AI Emergency Risk Scoring Engine
# Computes a transparent, rule-based risk score based on patient demographics,
# current medicines, symptoms, and known medical conditions.
# For educational purposes only — not a clinical decision-support tool.

from __future__ import annotations
from typing import Optional
from rapidfuzz import process, fuzz
from med_db import MED_DB


# ── Medicine Lookup ────────────────────────────────────────────────────────────

def find_medicine(name: str) -> Optional[str]:
    """
    Fuzzy-match a medicine name string to a MED_DB key.

    Returns the matching key (str) or None if no confident match is found.
    Confidence threshold: 65 (token_sort_ratio).
    """
    if not name or not name.strip():
        return None

    name_lower = name.lower().strip()

    # Direct key match (exact)
    if name_lower in MED_DB:
        return name_lower

    keys = list(MED_DB.keys())
    display_names = [MED_DB[k]["name"].lower() for k in keys]

    # Fuzzy match against database keys
    key_match = process.extractOne(
        name_lower, keys, scorer=fuzz.token_sort_ratio, score_cutoff=65
    )
    if key_match:
        return key_match[0]

    # Fuzzy match against display names
    name_match = process.extractOne(
        name_lower, display_names, scorer=fuzz.token_sort_ratio, score_cutoff=65
    )
    if name_match:
        idx = display_names.index(name_match[0])
        return keys[idx]

    return None


# ── Risk Tables ────────────────────────────────────────────────────────────────

# Symptom keyword → risk points
_HIGH_RISK_SYMPTOMS: dict[str, int] = {
    "chest pain": 30,
    "difficulty breathing": 25,
    "shortness of breath": 25,
    "breathlessness": 20,
    "loss of consciousness": 35,
    "unconscious": 35,
    "seizure": 35,
    "convulsion": 35,
    "stroke": 40,
    "severe bleeding": 35,
    "vomiting blood": 30,
    "anaphylaxis": 40,
    "allergic reaction": 20,
    "heart attack": 40,
    "confusion": 20,
    "fainting": 20,
    "sudden weakness": 25,
    "paralysis": 35,
    "vision loss": 20,
    "severe headache": 15,
    "high fever": 15,
    "cyanosis": 30,
    "blue lips": 30,
}

# Known dangerous drug-combination pairs → (frozenset of db keys, description)
_HIGH_RISK_COMBOS: list[tuple[frozenset, str]] = [
    (frozenset({"warfarin", "aspirin"}),
     "Warfarin + Aspirin — combined anticoagulant and antiplatelet effect: high haemorrhage risk"),
    (frozenset({"warfarin", "ibuprofen"}),
     "Warfarin + Ibuprofen — NSAID dramatically increases bleeding risk and INR"),
    (frozenset({"warfarin", "ciprofloxacin"}),
     "Warfarin + Ciprofloxacin — fluoroquinolone significantly elevates INR"),
    (frozenset({"warfarin", "azithromycin"}),
     "Warfarin + Azithromycin — macrolide enhances anticoagulant effect"),
    (frozenset({"warfarin", "clopidogrel"}),
     "Warfarin + Clopidogrel — triple antithrombotic risk of major bleeding"),
    (frozenset({"metoprolol", "verapamil"}),
     "Metoprolol + Verapamil — additive AV node depression: bradycardia/heart block"),
    (frozenset({"metoprolol", "diltiazem"}),
     "Metoprolol + Diltiazem — risk of severe bradycardia and AV block"),
    (frozenset({"metoprolol", "amiodarone"}),
     "Metoprolol + Amiodarone — additive conduction slowing: serious bradyarrhythmia risk"),
    (frozenset({"simvastatin", "gemfibrozil"}),
     "Simvastatin + Gemfibrozil — contraindicated: very high rhabdomyolysis risk"),
    (frozenset({"atorvastatin", "gemfibrozil"}),
     "Atorvastatin + Gemfibrozil — increased myopathy and rhabdomyolysis risk"),
    (frozenset({"azithromycin", "amiodarone"}),
     "Azithromycin + Amiodarone — additive QT prolongation: potentially fatal arrhythmia"),
    (frozenset({"clopidogrel", "omeprazole"}),
     "Clopidogrel + Omeprazole — CYP2C19 inhibition reduces clopidogrel efficacy"),
    (frozenset({"digoxin", "amiodarone"}),
     "Digoxin + Amiodarone — amiodarone increases digoxin levels by ~70%: toxicity risk"),
    (frozenset({"aspirin", "clopidogrel"}),
     "Aspirin + Clopidogrel — dual antiplatelet therapy: significantly increased bleeding risk"),
    (frozenset({"metformin", "iodinated contrast"}),
     "Metformin + Iodinated Contrast — must withhold metformin before contrast: lactic acidosis risk"),
]

# Medical condition keyword → risk points
_HIGH_RISK_CONDITIONS: dict[str, int] = {
    "heart failure": 15,
    "cardiac failure": 15,
    "renal failure": 15,
    "kidney failure": 15,
    "liver failure": 15,
    "hepatic failure": 15,
    "chronic kidney disease": 12,
    "ckd": 12,
    "liver disease": 12,
    "hepatic impairment": 12,
    "cirrhosis": 12,
    "diabetes": 8,
    "type 1 diabetes": 8,
    "type 2 diabetes": 8,
    "hypertension": 6,
    "high blood pressure": 6,
    "copd": 10,
    "asthma": 8,
    "epilepsy": 10,
    "seizure disorder": 10,
    "pregnancy": 15,
    "pregnant": 15,
    "immunosuppressed": 15,
    "immunocompromised": 15,
    "hiv": 12,
    "cancer": 12,
    "atrial fibrillation": 10,
    "afib": 10,
    "heart disease": 10,
    "coronary artery disease": 10,
    "stroke history": 12,
    "bleeding disorder": 12,
}


# ── Main Scoring Function ──────────────────────────────────────────────────────

def calculate_risk_score(
    age: int,
    gender: str,
    medicines: list[str],
    symptoms: list[str],
    conditions: list[str],
) -> dict:
    """
    Calculate an educational emergency risk score (0–100).

    Parameters
    ----------
    age        : Patient age in years.
    gender     : Patient gender string (informational only).
    medicines  : List of medicine name strings (free text).
    symptoms   : List of symptom description strings.
    conditions : List of known medical condition strings.

    Returns
    -------
    dict with keys:
        score           : int — final capped risk score (0–100)
        level           : str — risk level label
        color           : str — 'red' | 'orange' | 'yellow' | 'green'
        recommendation  : str — action guidance
        factors         : list[str] — human-readable score breakdown
        warnings        : list[str] — dangerous drug combination alerts
        resolved_medicines : list[str] — matched MED_DB keys
    """
    score = 0
    factors: list[str] = []
    warnings: list[str] = []

    # ── 1. Age-based risk ─────────────────────────────────────────────
    if age >= 75:
        score += 20
        factors.append(
            "Age ≥ 75 (+20): High-risk group — reduced organ reserve and polypharmacy sensitivity"
        )
    elif age >= 65:
        score += 12
        factors.append(
            "Age ≥ 65 (+12): Elderly patient — increased drug sensitivity and fall risk"
        )
    elif age <= 2:
        score += 15
        factors.append(
            "Age ≤ 2 (+15): Infant — weight-based dosing essential; many drugs contraindicated"
        )
    elif age <= 12:
        score += 8
        factors.append(
            "Age ≤ 12 (+8): Child — paediatric dosing and formulation considerations required"
        )

    # ── 2. Resolve medicine names via fuzzy matching ───────────────────
    resolved: list[str] = []
    for med in medicines:
        key = find_medicine(med)
        if key and key not in resolved:
            resolved.append(key)

    # ── 3. Polypharmacy risk ───────────────────────────────────────────
    n = len(resolved)
    if n >= 10:
        score += 20
        factors.append(f"Polypharmacy: {n} medicines (+20): Severe polypharmacy — very high interaction risk")
    elif n >= 7:
        score += 15
        factors.append(f"Polypharmacy: {n} medicines (+15): Major polypharmacy concern")
    elif n >= 5:
        score += 10
        factors.append(f"Polypharmacy: {n} medicines (+10): Moderate polypharmacy")
    elif n >= 3:
        score += 5
        factors.append(f"{n} medicines (+5): Multiple medications in use")

    # ── 4. Known dangerous drug combinations ──────────────────────────
    med_set = set(resolved)
    for combo, description in _HIGH_RISK_COMBOS:
        if combo.issubset(med_set):
            score += 15
            factors.append(f"Dangerous combination (+15): {description}")
            warnings.append(description)

    # ── 5. Pairwise interaction severity from MED_DB ──────────────────
    interaction_points = 0
    for key in resolved:
        db_interactions = MED_DB[key].get("interactions", {})
        for other_key in resolved:
            if other_key == key:
                continue
            other_name = MED_DB[other_key]["name"].lower()
            for interaction_name, severity_text in db_interactions.items():
                similarity = fuzz.token_sort_ratio(interaction_name.lower(), other_key.lower())
                name_similarity = fuzz.token_sort_ratio(interaction_name.lower(), other_name)
                if max(similarity, name_similarity) >= 70:
                    if "High" in severity_text:
                        interaction_points += 8
                    elif "Moderate" in severity_text:
                        interaction_points += 4
                    break  # count once per pair per direction

    if interaction_points > 0:
        # Cap interaction contribution at 30 points
        contribution = min(interaction_points, 30)
        score += contribution
        factors.append(
            f"Drug–drug interactions detected (+{contribution}): "
            f"Cross-referenced against medicine database"
        )

    # ── 6. Symptom-based risk ──────────────────────────────────────────
    symptom_text = " ".join(symptoms).lower()
    for symptom_kw, pts in _HIGH_RISK_SYMPTOMS.items():
        if symptom_kw in symptom_text:
            score += pts
            factors.append(
                f"High-risk symptom '{symptom_kw}' (+{pts}): Requires urgent clinical evaluation"
            )

    # ── 7. Medical conditions ──────────────────────────────────────────
    condition_text = " ".join(conditions).lower()
    for condition_kw, pts in _HIGH_RISK_CONDITIONS.items():
        if condition_kw in condition_text:
            score += pts
            factors.append(f"High-risk condition '{condition_kw}' (+{pts})")

    # ── 8. Cap and classify ────────────────────────────────────────────
    score = min(score, 100)

    if score >= 70:
        level = "🚨 CRITICAL"
        recommendation = (
            "Seek emergency medical care immediately. "
            "Call 911 / 112 or proceed to the nearest emergency department."
        )
        color = "red"
    elif score >= 50:
        level = "⚠️ HIGH"
        recommendation = (
            "Consult a healthcare provider urgently — ideally within 24 hours. "
            "Do not delay if symptoms are worsening."
        )
        color = "orange"
    elif score >= 30:
        level = "⚠️ MODERATE"
        recommendation = (
            "Schedule an appointment with your doctor soon. "
            "Monitor your symptoms closely and seek earlier care if they worsen."
        )
        color = "yellow"
    else:
        level = "✅ LOW"
        recommendation = (
            "Risk appears low based on the information provided. "
            "Continue regular monitoring and maintain scheduled check-ups."
        )
        color = "green"

    return {
        "score": score,
        "level": level,
        "color": color,
        "recommendation": recommendation,
        "factors": factors,
        "warnings": warnings,
        "resolved_medicines": resolved,
    }
