# symptom.py — MedSafe AI Symptom Advice Module
# Rule-based symptom guidance for educational purposes.
# NOT a substitute for professional medical advice.


def symptom_advice(symptom: str) -> str:
    """
    Return rule-based educational guidance for a described symptom.
    Input is matched against keyword groups for common conditions.
    """
    s = symptom.lower().strip()

    # ── Cold / Runny Nose / Sneezing ───────────────────────────────────────
    if any(k in s for k in ["cold", "runny nose", "sneezing", "stuffy nose",
                             "nasal congestion", "blocked nose", "sinus"]):
        return (
            "🤧 **Cold / Sneezing / Runny Nose**\n\n"
            "**Home Remedies:**\n"
            "- Drink warm liquids frequently — ginger tea, kadha, or chicken soup.\n"
            "- Honey + warm water helps soothe throat and reduce mucus.\n"
            "- Avoid cold drinks, ice cream, and refrigerated foods.\n"
            "- Try saline nasal drops or spray to clear congestion.\n\n"
            "**Steam Inhalation:**\n"
            "- Inhale steam 2–3 times daily; add eucalyptus oil for relief.\n\n"
            "**Yoga / Breathing:**\n"
            "- Anulom-Vilom and Kapalbhati pranayama (avoid if fever is present).\n\n"
            "**⚠️ See a doctor if:**\n"
            "- Symptoms persist beyond 10 days without improvement.\n"
            "- High fever (>103 °F / 39.4 °C) develops.\n"
            "- Blood in mucus or severe facial/sinus pain appears.\n\n"
            "_Usually resolves within 4–7 days with rest._"
        )

    # ── Fever / High Temperature ───────────────────────────────────────────
    if any(k in s for k in ["fever", "temperature", "pyrexia", "chills",
                             "hot body", "sweating fever"]):
        return (
            "🌡️ **Fever / High Temperature**\n\n"
            "**Immediate Steps:**\n"
            "- Rest in a cool, well-ventilated room.\n"
            "- Stay hydrated — water, ORS, coconut water, or clear broth.\n"
            "- Paracetamol (500 mg every 4–6 h) if temperature ≥ 38.5 °C (101.3 °F).\n"
            "- Apply a cool, damp cloth to the forehead and wrists.\n"
            "- Wear light, breathable cotton clothing.\n"
            "- Avoid cold baths — they may trigger shivering and raise temperature.\n\n"
            "**Monitor** temperature every 4 hours and log readings.\n\n"
            "**⚠️ Seek immediate medical attention if:**\n"
            "- Temperature exceeds 103 °F (39.4 °C).\n"
            "- Fever in infants < 3 months or adults > 65 years.\n"
            "- Accompanied by stiff neck, skin rash, confusion, or difficulty breathing.\n"
            "- Fever lasts more than 3 days without improvement.\n"
            "- Seizure occurs with fever (febrile convulsion)."
        )

    # ── Diarrhea / Loose Motion ────────────────────────────────────────────
    if any(k in s for k in ["diarrhea", "loose motion", "loose stool",
                             "watery stool", "gastro", "stomach upset",
                             "stomach infection", "food poisoning"]):
        return (
            "💧 **Diarrhea / Loose Motion**\n\n"
            "**Critical — Prevent Dehydration:**\n"
            "- ORS (Oral Rehydration Solution) is mandatory — take frequent small sips.\n"
            "- Drink coconut water, rice water (kanji), or clear broth.\n"
            "- Homemade ORS: 1 litre water + 6 tsp sugar + ½ tsp salt.\n\n"
            "**Diet (BRAT):**\n"
            "- Bananas, Rice, Applesauce (stewed apple), Toast — easy to digest.\n"
            "- Probiotics: curd/yoghurt helps restore gut flora.\n"
            "- Avoid milk, spicy food, raw salads, coffee, and fatty meals.\n\n"
            "**⚠️ See a doctor immediately if:**\n"
            "- Blood or mucus appears in stool.\n"
            "- Severe abdominal cramps or high fever.\n"
            "- Signs of dehydration: dry mouth, no urination for > 8 hours, dizziness.\n"
            "- More than 6 loose episodes in 24 hours.\n"
            "- Child under 2 years or elderly patient affected."
        )

    # ── Headache / Migraine ────────────────────────────────────────────────
    if any(k in s for k in ["headache", "migraine", "head pain",
                             "head ache", "throbbing head", "cluster headache"]):
        return (
            "🤕 **Headache / Migraine**\n\n"
            "**Relief Measures:**\n"
            "- Rest in a quiet, dark, and cool room.\n"
            "- Apply a cold compress on the forehead or warm compress on the neck.\n"
            "- Stay hydrated — dehydration is one of the most common triggers.\n"
            "- Gentle neck and shoulder stretches may reduce tension headaches.\n"
            "- Peppermint oil massage on temples can provide temporary relief.\n"
            "- Paracetamol or ibuprofen for tension headache (if no contraindications).\n\n"
            "**Common Triggers to Avoid:**\n"
            "Stress, bright/flickering lights, skipping meals, caffeine withdrawal, "
            "disrupted sleep, strong perfumes, and dehydration.\n\n"
            "**⚠️ Seek urgent care if:**\n"
            "- Sudden severe 'thunderclap' headache (worst headache of your life).\n"
            "- Headache with fever, stiff neck, or skin rash (possible meningitis).\n"
            "- Associated with vision changes, weakness, or speech difficulty.\n"
            "- Headache following a head injury or fall."
        )

    # ── Cough ──────────────────────────────────────────────────────────────
    if any(k in s for k in ["cough", "dry cough", "wet cough",
                             "productive cough", "whooping", "chest cough"]):
        return (
            "😮‍💨 **Cough**\n\n"
            "**Home Remedies:**\n"
            "- 1 teaspoon of honey in warm water — natural cough suppressant.\n"
            "- Ginger tea with honey and lemon is effective for throat irritation.\n"
            "- Steam inhalation helps loosen and clear mucus.\n"
            "- Stay well-hydrated to thin secretions.\n"
            "- Elevate your head while sleeping to reduce post-nasal drip.\n"
            "- Avoid cold drinks, fried food, and dairy (if productive cough).\n\n"
            "**Dry vs Wet Cough:**\n"
            "- Dry cough: often viral/allergic — honey, steam inhalation.\n"
            "- Wet/productive cough: focus on hydration and steam to clear secretions.\n\n"
            "**⚠️ See a doctor if:**\n"
            "- Cough persists more than 2–3 weeks.\n"
            "- Blood appears in cough (haemoptysis — seek urgent care).\n"
            "- Accompanied by chest pain, shortness of breath, or high fever.\n"
            "- Sudden weight loss alongside chronic cough."
        )

    # ── Chest Pain ─────────────────────────────────────────────────────────
    if any(k in s for k in ["chest pain", "chest tightness", "chest pressure",
                             "angina", "heart pain", "chest discomfort"]):
        return (
            "🚨 **CHEST PAIN — URGENT**\n\n"
            "⚠️ **Chest pain can be a life-threatening emergency. Do not ignore it.**\n\n"
            "**Call emergency services (911 / 112) immediately if:**\n"
            "- Pain is crushing, squeezing, or pressure-like.\n"
            "- Pain radiates to the left arm, jaw, back, or shoulder.\n"
            "- Accompanied by sweating, nausea, or vomiting.\n"
            "- Difficulty breathing occurs.\n"
            "- Symptoms are new or rapidly worsening.\n\n"
            "**While waiting for help:**\n"
            "- Sit or lie down in a comfortable position.\n"
            "- Chew one 325 mg aspirin (if no allergy and not already on anticoagulants).\n"
            "- Loosen any tight clothing around the chest.\n"
            "- Do NOT drive yourself to the hospital.\n\n"
            "_Non-cardiac causes include GERD, costochondritis, anxiety, and muscle strain — "
            "but always rule out cardiac causes first._"
        )

    # ── Nausea / Vomiting ──────────────────────────────────────────────────
    if any(k in s for k in ["nausea", "vomiting", "nauseous", "feeling sick",
                             "throwing up", "motion sickness"]):
        return (
            "🤢 **Nausea / Vomiting**\n\n"
            "**Relief Measures:**\n"
            "- Sip small amounts of clear fluids frequently (water, ginger ale, ORS).\n"
            "- Ginger tea, ginger candies, or ginger ale help reduce nausea naturally.\n"
            "- Eat small, bland meals — crackers, plain rice, toast.\n"
            "- Avoid strong smells, greasy, spicy, or dairy-rich foods.\n"
            "- Rest in a semi-reclined position.\n"
            "- Acupressure on the P6 point (3 fingers below inner wrist) may help.\n\n"
            "**⚠️ Seek medical attention if:**\n"
            "- Vomiting blood or dark 'coffee-ground' material.\n"
            "- Unable to keep any fluids down for more than 24 hours.\n"
            "- Signs of dehydration: dry mouth, sunken eyes, dark urine, extreme fatigue.\n"
            "- Severe abdominal pain accompanies vomiting.\n"
            "- Associated with severe headache or stiff neck (possible meningitis)."
        )

    # ── Skin Rash / Itching ────────────────────────────────────────────────
    if any(k in s for k in ["rash", "itching", "itch", "hives",
                             "urticaria", "skin irritation", "eczema",
                             "allergic reaction", "skin allergy"]):
        return (
            "🔴 **Skin Rash / Itching**\n\n"
            "**Relief Measures:**\n"
            "- Apply a cold compress or ice pack wrapped in cloth to the affected area.\n"
            "- Calamine lotion or mild hydrocortisone cream for localized rash.\n"
            "- Oral antihistamine (e.g., cetirizine 10 mg) for allergic rash or hives.\n"
            "- Keep the area clean, dry, and away from irritants.\n"
            "- Wear loose, breathable cotton clothing.\n"
            "- Avoid scratching — it worsens inflammation and increases infection risk.\n\n"
            "**Common Triggers:** Food allergies, medicines, insect bites, heat, "
            "laundry detergents, pet dander, latex, and cosmetics.\n\n"
            "**⚠️ Seek urgent care if:**\n"
            "- Rash spreads rapidly or face/throat swelling occurs (anaphylaxis risk).\n"
            "- Difficulty breathing or swallowing develops.\n"
            "- Rash with high fever — possible meningitis, scarlet fever.\n"
            "- Painful blistering rash in a band pattern — possible shingles (herpes zoster)."
        )

    # ── Shortness of Breath ────────────────────────────────────────────────
    if any(k in s for k in ["shortness of breath", "breathlessness",
                             "difficulty breathing", "dyspnea",
                             "can't breathe", "cannot breathe",
                             "breathing difficulty"]):
        return (
            "🚨 **Shortness of Breath — URGENT**\n\n"
            "⚠️ **Difficulty breathing requires immediate medical evaluation.**\n\n"
            "**Call emergency services if:**\n"
            "- Sudden severe breathlessness at rest.\n"
            "- Lips or fingertips turning blue (cyanosis).\n"
            "- Accompanied by chest pain or rapid heart rate.\n"
            "- Following an allergic reaction or insect sting.\n\n"
            "**While waiting for help:**\n"
            "- Sit upright, leaning slightly forward (tripod position).\n"
            "- Loosen tight clothing around the neck and chest.\n"
            "- Use a prescribed inhaler if you are asthmatic.\n"
            "- Open windows or move to fresh air.\n\n"
            "_Causes range from asthma/COPD, anemia, and anxiety to serious conditions "
            "like pulmonary embolism, pneumothorax, or acute heart failure._"
        )

    # ── Joint / Muscle / Back Pain ─────────────────────────────────────────
    if any(k in s for k in ["joint pain", "arthritis", "knee pain",
                             "back pain", "muscle pain", "body ache",
                             "muscle ache", "stiff joints", "hip pain"]):
        return (
            "🦴 **Joint / Muscle Pain**\n\n"
            "**Relief Measures:**\n"
            "- Ice pack for acute injury (first 48 h); warm compress for chronic aches.\n"
            "- Rest the affected joint and avoid activities that worsen pain.\n"
            "- Gentle stretching and low-impact exercises (swimming, walking).\n"
            "- Paracetamol or ibuprofen for pain relief (if no contraindications).\n"
            "- Turmeric milk (golden milk) has natural anti-inflammatory properties.\n"
            "- Maintain a healthy weight to reduce mechanical stress on joints.\n\n"
            "**⚠️ See a doctor if:**\n"
            "- Severe swelling, redness, or warmth at the joint.\n"
            "- Sudden inability to bear weight or move the joint.\n"
            "- Fever accompanying joint pain (possible septic arthritis).\n"
            "- Multiple joints affected simultaneously (possible autoimmune condition).\n"
            "- Pain not responding to over-the-counter medication after 1 week."
        )

    # ── Dizziness / Vertigo ────────────────────────────────────────────────
    if any(k in s for k in ["dizziness", "dizzy", "vertigo",
                             "lightheaded", "light headed", "spinning"]):
        return (
            "💫 **Dizziness / Vertigo**\n\n"
            "**Immediate Steps:**\n"
            "- Sit or lie down immediately to prevent falls.\n"
            "- Avoid sudden head movements.\n"
            "- Stay well-hydrated — dehydration is a common cause.\n"
            "- Eat small, regular meals to prevent low blood sugar.\n\n"
            "**Epley Manoeuvre** (for BPPV/benign positional vertigo) "
            "may provide rapid relief — ask your doctor to demonstrate.\n\n"
            "**Common Causes:** BPPV, dehydration, anaemia, hypotension, "
            "labyrinthitis, medication side effects, anxiety.\n\n"
            "**⚠️ Seek urgent care if:**\n"
            "- Sudden onset severe vertigo with hearing loss or tinnitus.\n"
            "- Associated with double vision, difficulty speaking, or weakness.\n"
            "- Dizziness following a head injury.\n"
            "- Fainting or loss of consciousness occurs."
        )

    # ── Abdominal / Stomach Pain ───────────────────────────────────────────
    if any(k in s for k in ["stomach pain", "abdominal pain", "belly pain",
                             "tummy ache", "cramps", "stomach cramps",
                             "indigestion", "acidity", "heartburn", "acid reflux"]):
        return (
            "🤧 **Abdominal Pain / Indigestion**\n\n"
            "**Relief Measures:**\n"
            "- Drink warm water or herbal teas (peppermint, chamomile, ginger).\n"
            "- Eat small, bland meals — avoid spicy, greasy, and acidic foods.\n"
            "- Antacids (e.g., Gaviscon, Gelusil) for heartburn/GERD symptoms.\n"
            "- Walk gently after meals to aid digestion.\n"
            "- Apply a warm heating pad on the abdomen for cramping.\n\n"
            "**Avoid:** Alcohol, caffeine, carbonated drinks, NSAIDs on an empty stomach.\n\n"
            "**⚠️ Seek urgent care if:**\n"
            "- Severe or sudden-onset abdominal pain (especially right lower quadrant).\n"
            "- Pain accompanied by fever and vomiting.\n"
            "- Abdomen feels rigid or board-like.\n"
            "- Blood in stool or vomit.\n"
            "- Pain in a pregnant patient."
        )

    # ── Default / General ──────────────────────────────────────────────────
    return (
        "ℹ️ **General Health Advice**\n\n"
        "Your symptom description did not closely match a specific category. "
        "Here is some general guidance:\n\n"
        "- Rest adequately and stay well-hydrated.\n"
        "- Eat a balanced, nutritious diet and avoid processed foods.\n"
        "- Monitor your symptoms and note any changes in severity or character.\n"
        "- Avoid self-medicating without proper guidance.\n\n"
        "**⚠️ Please consult a healthcare professional for:**\n"
        "- Persistent or worsening symptoms lasting more than 3 days.\n"
        "- Any symptom causing significant distress or concern.\n"
        "- Symptoms in infants, children, elderly patients, pregnant women, "
        "or immunocompromised individuals.\n\n"
        "_MedSafe AI provides educational information only and is NOT a substitute "
        "for professional medical advice, diagnosis, or treatment._"
    )
