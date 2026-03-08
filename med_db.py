# med_db.py — MedSafe AI Medicine Database
# Contains medicine interaction metadata, dosing information,
# side effects, and contraindications for educational purposes.

MED_DB = {
    "atorvastatin": {
        "name": "Atorvastatin",
        "standard_dose_mg": {"adult": 10, "pediatric": None},
        "interactions": {
            "clarithromycin": "High ⚠️ CYP3A4 inhibitor — significantly increases atorvastatin plasma levels, raising myopathy risk",
            "grapefruit juice": "High ⚠️ Inhibits CYP3A4 — increases atorvastatin blood levels, avoid consumption",
            "cyclosporine": "High ⚠️ Markedly increases atorvastatin exposure — high risk of myopathy/rhabdomyolysis",
            "gemfibrozil": "High ⚠️ Increased risk of myopathy and rhabdomyolysis — avoid combination",
            "itraconazole": "High ⚠️ Strong CYP3A4 inhibitor — significantly raises statin levels",
            "erythromycin": "Moderate ⚠️ CYP3A4 inhibition increases atorvastatin levels",
            "niacin": "Moderate ⚠️ Combined use increases myopathy risk, especially at high niacin doses",
            "warfarin": "Moderate ⚠️ May enhance anticoagulant effect — monitor INR closely",
            "digoxin": "Moderate ⚠️ Atorvastatin may increase digoxin serum levels by ~20%",
            "oral contraceptives": "Low ℹ️ Slight increase in norethindrone and ethinyl estradiol levels",
        },
        "side_effects": [
            "muscle pain (myalgia)", "elevated liver enzymes", "headache",
            "nausea", "constipation", "diarrhea", "rhabdomyolysis (rare)"
        ],
        "contraindications": [
            "pregnancy", "breastfeeding", "active liver disease",
            "unexplained elevated transaminases"
        ],
        "category": "Statin / HMG-CoA Reductase Inhibitor",
    },

    "rosuvastatin": {
        "name": "Rosuvastatin",
        "standard_dose_mg": {"adult": 10, "pediatric": 5},
        "interactions": {
            "cyclosporine": "High ⚠️ Markedly increases rosuvastatin AUC — use with extreme caution",
            "gemfibrozil": "Moderate ⚠️ Increased myopathy risk — avoid or use lowest statin dose",
            "warfarin": "Moderate ⚠️ May increase INR — monitor anticoagulation closely",
            "lopinavir/ritonavir": "High ⚠️ HIV protease inhibitors significantly increase rosuvastatin exposure",
            "niacin": "Moderate ⚠️ Increased myopathy risk especially at high niacin doses",
            "antacids": "Low ℹ️ Aluminum/magnesium antacids may slightly reduce rosuvastatin absorption",
        },
        "side_effects": [
            "muscle pain", "headache", "abdominal pain", "nausea",
            "weakness", "proteinuria (rare at high doses)"
        ],
        "contraindications": [
            "pregnancy", "active liver disease", "unexplained elevated CPK"
        ],
        "category": "Statin / HMG-CoA Reductase Inhibitor",
    },

    "simvastatin": {
        "name": "Simvastatin",
        "standard_dose_mg": {"adult": 20, "pediatric": None},
        "interactions": {
            "amiodarone": "High ⚠️ Increases simvastatin levels — do not exceed 20 mg/day",
            "verapamil": "High ⚠️ Increases risk of myopathy — do not exceed 10 mg/day",
            "diltiazem": "Moderate ⚠️ Increases simvastatin levels — do not exceed 10 mg/day",
            "amlodipine": "High ⚠️ Do not exceed simvastatin 20 mg/day — increased myopathy risk",
            "clarithromycin": "High ⚠️ Strong CYP3A4 inhibitor — significantly raises statin levels",
            "itraconazole": "High ⚠️ Contraindicated — massive increase in simvastatin levels",
            "gemfibrozil": "High ⚠️ Contraindicated — very high myopathy/rhabdomyolysis risk",
            "niacin": "Moderate ⚠️ Increased myopathy risk",
            "grapefruit juice": "High ⚠️ Avoid grapefruit products entirely",
            "cyclosporine": "High ⚠️ Increased statin exposure — myopathy risk",
        },
        "side_effects": [
            "myalgia", "elevated CK", "liver function abnormalities",
            "headache", "GI disturbances", "rhabdomyolysis (rare)"
        ],
        "contraindications": [
            "pregnancy", "active hepatic disease",
            "concomitant strong CYP3A4 inhibitors"
        ],
        "category": "Statin / HMG-CoA Reductase Inhibitor",
    },

    "metformin": {
        "name": "Metformin",
        "standard_dose_mg": {"adult": 500, "pediatric": 500},
        "interactions": {
            "alcohol": "High ⚠️ Chronic alcohol use increases lactic acidosis risk — avoid excessive alcohol",
            "iodinated contrast": "High ⚠️ Withhold before contrast procedures — risk of AKI and lactic acidosis",
            "cimetidine": "Moderate ⚠️ Increases metformin plasma levels by reducing renal excretion",
            "furosemide": "Moderate ⚠️ May increase metformin plasma levels",
            "topiramate": "Moderate ⚠️ May increase risk of lactic acidosis",
            "insulin": "Moderate ⚠️ Combined hypoglycemia risk — monitor blood glucose frequently",
            "glipizide": "Moderate ⚠️ Additive hypoglycemic effect — dose adjustment may be needed",
        },
        "side_effects": [
            "nausea", "diarrhea", "abdominal discomfort", "metallic taste",
            "lactic acidosis (rare but serious)", "vitamin B12 deficiency (long-term)"
        ],
        "contraindications": [
            "eGFR < 30 mL/min", "hepatic impairment",
            "acute illness with dehydration", "excessive alcohol use"
        ],
        "category": "Biguanide / Antidiabetic",
    },

    "glipizide": {
        "name": "Glipizide",
        "standard_dose_mg": {"adult": 5, "pediatric": None},
        "interactions": {
            "fluconazole": "High ⚠️ CYP2C9 inhibitor — significantly increases glipizide levels and hypoglycemia risk",
            "metformin": "Moderate ⚠️ Additive hypoglycemia — monitor glucose regularly",
            "beta-blockers": "Moderate ⚠️ May mask tachycardia symptoms of hypoglycemia",
            "alcohol": "High ⚠️ Disulfiram-like reaction and enhanced hypoglycemia",
            "NSAIDs": "Moderate ⚠️ May enhance hypoglycemic effect",
            "warfarin": "Moderate ⚠️ Interaction may alter anticoagulant effect",
        },
        "side_effects": [
            "hypoglycemia", "weight gain", "nausea", "dizziness", "skin reactions"
        ],
        "contraindications": [
            "type 1 diabetes", "diabetic ketoacidosis",
            "severe renal or hepatic impairment", "pregnancy"
        ],
        "category": "Sulfonylurea / Antidiabetic",
    },

    "insulin": {
        "name": "Insulin",
        "standard_dose_mg": {"adult": None, "pediatric": None},
        "interactions": {
            "metformin": "Moderate ⚠️ Additive hypoglycemic effect — monitor blood glucose",
            "glipizide": "Moderate ⚠️ Additive hypoglycemia risk",
            "beta-blockers": "Moderate ⚠️ Masks tachycardia symptom of hypoglycemia",
            "alcohol": "High ⚠️ Potentiates hypoglycemia — may mask recovery response",
            "corticosteroids": "High ⚠️ Steroids raise blood glucose — insulin dose adjustment needed",
            "fluoroquinolones": "Moderate ⚠️ May cause unpredictable hypo/hyperglycemia with insulin",
        },
        "side_effects": [
            "hypoglycemia", "weight gain", "lipodystrophy at injection sites",
            "hypokalemia (IV high-dose)"
        ],
        "contraindications": ["hypoglycemia episode (active)"],
        "category": "Hormone / Antidiabetic",
    },

    "amoxicillin": {
        "name": "Amoxicillin",
        "standard_dose_mg": {"adult": 500, "pediatric": 250},
        "interactions": {
            "warfarin": "Moderate ⚠️ May increase anticoagulant effect — monitor INR",
            "methotrexate": "High ⚠️ Reduced methotrexate renal clearance — toxicity risk",
            "allopurinol": "Moderate ⚠️ Increased incidence of skin rash (ampicillin-type rash)",
            "oral contraceptives": "Low ℹ️ Theoretical reduction in contraceptive efficacy — use backup method",
            "probenecid": "Moderate ⚠️ Increases amoxicillin plasma levels by blocking renal excretion",
        },
        "side_effects": [
            "diarrhea", "nausea", "skin rash", "vomiting",
            "allergic reactions (including anaphylaxis — rare)",
            "oral/vaginal candidiasis"
        ],
        "contraindications": [
            "penicillin allergy", "infectious mononucleosis (high risk of rash)"
        ],
        "category": "Beta-lactam Antibiotic / Aminopenicillin",
    },

    "amoxicillin_clavulanate": {
        "name": "Amoxicillin-Clavulanate",
        "standard_dose_mg": {"adult": 875, "pediatric": 400},
        "interactions": {
            "warfarin": "Moderate ⚠️ Enhanced anticoagulant effect — monitor INR",
            "methotrexate": "High ⚠️ Reduced clearance of methotrexate — risk of toxicity",
            "allopurinol": "Moderate ⚠️ Increased risk of skin rash",
            "probenecid": "Moderate ⚠️ Increases amoxicillin-clavulanate levels",
        },
        "side_effects": [
            "diarrhea (more common than amoxicillin alone)", "nausea",
            "vomiting", "skin rash", "hepatotoxicity (rare)",
            "cholestatic jaundice (rare)"
        ],
        "contraindications": [
            "penicillin allergy",
            "history of amoxicillin-clavulanate-associated cholestatic jaundice"
        ],
        "category": "Beta-lactam + Beta-lactamase Inhibitor Combination",
    },

    "cefuroxime": {
        "name": "Cefuroxime",
        "standard_dose_mg": {"adult": 500, "pediatric": 125},
        "interactions": {
            "warfarin": "Moderate ⚠️ May enhance anticoagulant effect",
            "probenecid": "Moderate ⚠️ Increases cefuroxime levels by reducing renal secretion",
            "antacids": "Low ℹ️ H2 blockers and PPIs reduce oral bioavailability — take with food",
            "loop diuretics": "Low ℹ️ Possible increased nephrotoxicity with high intravenous doses",
        },
        "side_effects": [
            "diarrhea", "nausea", "headache", "rash",
            "Clostridioides difficile colitis (rare)"
        ],
        "contraindications": [
            "cephalosporin allergy",
            "history of severe penicillin allergy (cross-reactivity possible)"
        ],
        "category": "Second-generation Cephalosporin Antibiotic",
    },

    "azithromycin": {
        "name": "Azithromycin",
        "standard_dose_mg": {"adult": 500, "pediatric": 10},
        "interactions": {
            "warfarin": "High ⚠️ Significantly increases anticoagulant effect — monitor INR",
            "amiodarone": "High ⚠️ QT prolongation risk — potentially fatal ventricular arrhythmia",
            "hydroxychloroquine": "High ⚠️ Additive QT prolongation — avoid combination",
            "digoxin": "Moderate ⚠️ Azithromycin increases digoxin serum levels",
            "cyclosporine": "Moderate ⚠️ May increase cyclosporine blood levels",
            "antacids": "Low ℹ️ Aluminum/magnesium antacids reduce peak azithromycin concentration",
        },
        "side_effects": [
            "nausea", "diarrhea", "abdominal pain", "vomiting",
            "QT prolongation", "hearing loss (rare, high-dose)"
        ],
        "contraindications": [
            "history of cholestatic jaundice with prior azithromycin use",
            "known QT prolongation syndrome", "myasthenia gravis"
        ],
        "category": "Macrolide Antibiotic",
    },

    "ciprofloxacin": {
        "name": "Ciprofloxacin",
        "standard_dose_mg": {"adult": 500, "pediatric": None},
        "interactions": {
            "warfarin": "High ⚠️ Significantly increases INR — monitor closely",
            "theophylline": "High ⚠️ Markedly increases theophylline levels — toxicity risk",
            "antacids": "High ⚠️ Magnesium/aluminum chelate ciprofloxacin — take 2h apart",
            "tizanidine": "High ⚠️ Contraindicated — dramatically increases tizanidine levels and risk of severe hypotension",
            "iron supplements": "Moderate ⚠️ Chelation reduces ciprofloxacin absorption",
            "NSAIDs": "Moderate ⚠️ Increased CNS stimulation and seizure risk",
            "metformin": "Low ℹ️ May slightly increase metformin levels",
        },
        "side_effects": [
            "nausea", "diarrhea", "headache", "dizziness", "photosensitivity",
            "tendinopathy/tendon rupture", "QT prolongation", "peripheral neuropathy"
        ],
        "contraindications": [
            "children/adolescents (growth plate damage risk)",
            "pregnancy",
            "history of fluoroquinolone-associated tendinopathy"
        ],
        "category": "Fluoroquinolone Antibiotic",
    },

    "ibuprofen": {
        "name": "Ibuprofen",
        "standard_dose_mg": {"adult": 400, "pediatric": 200},
        "interactions": {
            "warfarin": "High ⚠️ Increases bleeding risk — avoid or monitor closely",
            "aspirin": "Moderate ⚠️ May diminish aspirin's cardioprotective effect; additive GI bleeding risk",
            "methotrexate": "High ⚠️ NSAIDs reduce methotrexate clearance — significant toxicity risk",
            "lithium": "Moderate ⚠️ NSAIDs increase lithium serum levels — monitor for toxicity",
            "ACE inhibitors": "Moderate ⚠️ Reduced antihypertensive effect and increased nephrotoxicity risk",
            "lisinopril": "Moderate ⚠️ May reduce ACE inhibitor antihypertensive effect",
            "diuretics": "Moderate ⚠️ Reduced diuretic efficacy; may worsen renal function",
            "corticosteroids": "Moderate ⚠️ Additive GI ulceration and bleeding risk",
            "SSRIs": "Moderate ⚠️ Increased GI bleeding risk — consider gastroprotection",
            "ciprofloxacin": "Moderate ⚠️ Increased CNS stimulation and seizure risk",
        },
        "side_effects": [
            "GI upset", "peptic ulcer", "GI bleeding", "hypertension",
            "renal impairment", "edema", "hepatotoxicity (rare)"
        ],
        "contraindications": [
            "active peptic ulcer", "severe renal/hepatic impairment",
            "third trimester pregnancy", "NSAID hypersensitivity (aspirin-sensitive asthma)"
        ],
        "category": "NSAID / Anti-inflammatory Analgesic",
    },

    "paracetamol": {
        "name": "Paracetamol (Acetaminophen)",
        "standard_dose_mg": {"adult": 500, "pediatric": 250},
        "interactions": {
            "warfarin": "Moderate ⚠️ Regular high-dose use increases INR — monitor anticoagulation",
            "alcohol": "High ⚠️ Chronic alcohol use dramatically increases hepatotoxicity risk",
            "isoniazid": "High ⚠️ Significantly increased hepatotoxicity risk",
            "carbamazepine": "Moderate ⚠️ Induces paracetamol metabolism — reduced efficacy and increased toxic metabolite",
            "rifampicin": "Moderate ⚠️ Hepatic enzyme induction increases production of toxic NAPQI metabolite",
        },
        "side_effects": [
            "hepatotoxicity (overdose — major risk)", "nausea (rare at therapeutic doses)", "rash"
        ],
        "contraindications": [
            "severe hepatic impairment",
            "chronic alcoholism during concurrent use"
        ],
        "category": "Analgesic / Antipyretic",
    },

    "aspirin": {
        "name": "Aspirin (Acetylsalicylic Acid)",
        "standard_dose_mg": {"adult": 75, "pediatric": None},
        "interactions": {
            "warfarin": "High ⚠️ Combined antiplatelet + anticoagulant effect — major bleeding risk",
            "clopidogrel": "Moderate ⚠️ Dual antiplatelet therapy — increases bleeding risk significantly",
            "ibuprofen": "Moderate ⚠️ Ibuprofen may competitively block aspirin's cardioprotective COX-1 binding",
            "methotrexate": "High ⚠️ Reduced methotrexate clearance — toxicity risk",
            "valproic acid": "Moderate ⚠️ Displaces valproic acid from protein binding — increases free drug levels",
            "ACE inhibitors": "Moderate ⚠️ High-dose aspirin may reduce ACE inhibitor benefit in heart failure",
        },
        "side_effects": [
            "GI irritation", "peptic ulcer", "bleeding", "tinnitus (high doses)",
            "Reye's syndrome (children with viral illness)"
        ],
        "contraindications": [
            "children < 16 with viral illness (Reye's syndrome risk)",
            "active GI bleeding", "peptic ulcer", "gout (may exacerbate)"
        ],
        "category": "Antiplatelet / NSAID / Analgesic",
    },

    "lisinopril": {
        "name": "Lisinopril",
        "standard_dose_mg": {"adult": 10, "pediatric": None},
        "interactions": {
            "potassium": "High ⚠️ ACE inhibitors + potassium supplements — risk of life-threatening hyperkalemia",
            "spironolactone": "High ⚠️ Increased hyperkalemia risk — monitor potassium levels closely",
            "NSAIDs": "Moderate ⚠️ Reduced antihypertensive effect and increased renal impairment risk",
            "ibuprofen": "Moderate ⚠️ Reduced ACE inhibitor efficacy and increased nephrotoxicity",
            "lithium": "Moderate ⚠️ ACE inhibitors increase lithium toxicity risk",
            "aliskiren": "High ⚠️ Dual RAAS blockade contraindicated in diabetic patients",
            "diuretics": "Moderate ⚠️ First-dose hypotension risk — start low and titrate carefully",
        },
        "side_effects": [
            "dry cough (very common)", "hypotension", "hyperkalemia",
            "angioedema (rare but serious)", "renal impairment", "dizziness"
        ],
        "contraindications": [
            "pregnancy", "bilateral renal artery stenosis",
            "history of ACE inhibitor-induced angioedema"
        ],
        "category": "ACE Inhibitor / Antihypertensive",
    },

    "amlodipine": {
        "name": "Amlodipine",
        "standard_dose_mg": {"adult": 5, "pediatric": None},
        "interactions": {
            "simvastatin": "High ⚠️ Do not exceed simvastatin 20 mg/day — increased myopathy risk",
            "cyclosporine": "Moderate ⚠️ Amlodipine may increase cyclosporine blood levels",
            "tacrolimus": "Moderate ⚠️ May increase tacrolimus blood levels",
            "CYP3A4 inhibitors": "Moderate ⚠️ Ketoconazole/itraconazole increase amlodipine levels",
            "grapefruit juice": "Low ℹ️ May slightly increase amlodipine bioavailability",
        },
        "side_effects": [
            "peripheral edema (ankle swelling)", "flushing", "headache",
            "dizziness", "palpitations", "fatigue"
        ],
        "contraindications": [
            "cardiogenic shock", "severe aortic stenosis", "unstable angina"
        ],
        "category": "Calcium Channel Blocker / Antihypertensive",
    },

    "metoprolol": {
        "name": "Metoprolol",
        "standard_dose_mg": {"adult": 50, "pediatric": None},
        "interactions": {
            "verapamil": "High ⚠️ Additive negative chronotropic effect — risk of severe bradycardia/heart block",
            "diltiazem": "High ⚠️ Risk of AV block and severe bradycardia — monitor continuously",
            "amiodarone": "High ⚠️ Additive conduction slowing — serious bradyarrhythmia risk",
            "clonidine": "Moderate ⚠️ Rebound hypertension on clonidine withdrawal — taper clonidine first",
            "insulin": "Moderate ⚠️ Masks tachycardia symptom of hypoglycemia",
            "fluoxetine": "Moderate ⚠️ CYP2D6 inhibition increases metoprolol levels significantly",
            "NSAIDs": "Moderate ⚠️ May reduce antihypertensive effect",
        },
        "side_effects": [
            "bradycardia", "fatigue", "cold extremities", "depression",
            "bronchoconstriction", "hypotension", "dizziness"
        ],
        "contraindications": [
            "severe bradycardia", "AV block (2nd/3rd degree)",
            "decompensated heart failure", "asthma/reactive airway disease"
        ],
        "category": "Selective Beta-1 Blocker / Antihypertensive",
    },

    "warfarin": {
        "name": "Warfarin",
        "standard_dose_mg": {"adult": 5, "pediatric": None},
        "interactions": {
            "aspirin": "High ⚠️ Major bleeding risk — combined antiplatelet + anticoagulant effect",
            "ibuprofen": "High ⚠️ NSAIDs increase bleeding risk and may elevate INR significantly",
            "ciprofloxacin": "High ⚠️ Substantial INR increase — monitor very closely",
            "azithromycin": "High ⚠️ Increases anticoagulant effect — monitor INR during and after course",
            "amoxicillin": "Moderate ⚠️ May elevate INR — monitor during and after antibiotic course",
            "fluconazole": "High ⚠️ CYP2C9 inhibition dramatically increases warfarin effect",
            "carbamazepine": "High ⚠️ CYP enzyme induction decreases warfarin effect — INR may drop",
            "omeprazole": "Moderate ⚠️ May increase anticoagulant effect via CYP2C19 inhibition",
            "atorvastatin": "Moderate ⚠️ Monitor INR — statins may modestly increase anticoagulant effect",
            "vitamin k foods": "High ⚠️ Green leafy vegetables reduce warfarin effect — maintain consistent diet",
        },
        "side_effects": [
            "bleeding (major risk)", "bruising", "hemorrhage",
            "skin necrosis (rare)", "purple toe syndrome (rare)"
        ],
        "contraindications": [
            "pregnancy", "active major bleeding",
            "recent CNS/eye surgery", "uncontrolled severe hypertension"
        ],
        "category": "Vitamin K Antagonist / Anticoagulant",
    },

    "omeprazole": {
        "name": "Omeprazole",
        "standard_dose_mg": {"adult": 20, "pediatric": 10},
        "interactions": {
            "clopidogrel": "High ⚠️ CYP2C19 inhibition reduces clopidogrel activation — reduced antiplatelet effect",
            "warfarin": "Moderate ⚠️ May increase INR via CYP2C19 inhibition",
            "methotrexate": "Moderate ⚠️ May increase methotrexate plasma levels",
            "ketoconazole": "Moderate ⚠️ Elevated gastric pH reduces antifungal absorption",
            "iron supplements": "Low ℹ️ Reduced iron absorption — take at least 2h apart",
            "vitamin B12": "Low ℹ️ Long-term use may impair B12 absorption",
        },
        "side_effects": [
            "headache", "nausea", "diarrhea", "abdominal pain",
            "hypomagnesemia (long-term)", "C. difficile risk",
            "increased fracture risk (long-term use)"
        ],
        "contraindications": ["known hypersensitivity to proton pump inhibitors"],
        "category": "Proton Pump Inhibitor / Acid Suppressant",
    },

    "clopidogrel": {
        "name": "Clopidogrel",
        "standard_dose_mg": {"adult": 75, "pediatric": None},
        "interactions": {
            "omeprazole": "High ⚠️ Reduces clopidogrel efficacy by inhibiting CYP2C19-mediated activation",
            "aspirin": "Moderate ⚠️ Dual antiplatelet therapy — significantly increased bleeding risk",
            "warfarin": "High ⚠️ Triple antithrombotic therapy markedly increases bleeding risk",
            "NSAIDs": "High ⚠️ Additive GI bleeding risk",
            "fluconazole": "Moderate ⚠️ CYP2C19 inhibition may reduce clopidogrel activation",
        },
        "side_effects": [
            "bleeding", "bruising", "GI upset", "rash",
            "thrombotic thrombocytopenic purpura/TTP (rare but life-threatening)"
        ],
        "contraindications": [
            "active pathological bleeding", "severe hepatic impairment"
        ],
        "category": "P2Y12 Inhibitor / Antiplatelet Agent",
    },

    "amiodarone": {
        "name": "Amiodarone",
        "standard_dose_mg": {"adult": 200, "pediatric": None},
        "interactions": {
            "warfarin": "High ⚠️ Dramatically increases anticoagulant effect — reduce warfarin dose by 30–50%",
            "digoxin": "High ⚠️ Increases digoxin levels by ~70% — reduce digoxin dose and monitor",
            "metoprolol": "High ⚠️ Additive bradycardia and AV block risk",
            "simvastatin": "High ⚠️ Do not exceed simvastatin 20 mg/day — myopathy risk",
            "azithromycin": "High ⚠️ Additive QT prolongation risk — potentially fatal",
            "fluoroquinolones": "High ⚠️ Additive QT prolongation",
            "cyclosporine": "Moderate ⚠️ May increase cyclosporine levels",
        },
        "side_effects": [
            "thyroid dysfunction (hypo/hyperthyroidism)", "pulmonary toxicity",
            "hepatotoxicity", "corneal microdeposits", "photosensitivity",
            "peripheral neuropathy", "bradycardia", "QT prolongation"
        ],
        "contraindications": [
            "severe sinus node disease without pacemaker",
            "AV block without pacemaker", "thyroid dysfunction",
            "iodine hypersensitivity", "pregnancy"
        ],
        "category": "Class III Antiarrhythmic",
    },

    "digoxin": {
        "name": "Digoxin",
        "standard_dose_mg": {"adult": 0.125, "pediatric": None},
        "interactions": {
            "amiodarone": "High ⚠️ Increases digoxin levels by ~70% — serious toxicity risk",
            "azithromycin": "Moderate ⚠️ Macrolides increase digoxin bioavailability",
            "atorvastatin": "Moderate ⚠️ Statin may increase digoxin levels by ~20%",
            "verapamil": "High ⚠️ Increases digoxin levels and additive AV node depression",
            "spironolactone": "Moderate ⚠️ Interferes with digoxin assay and may increase levels",
            "diuretics": "High ⚠️ Hypokalemia from diuretics dramatically increases digoxin toxicity",
        },
        "side_effects": [
            "nausea", "vomiting", "bradycardia", "heart block",
            "visual disturbances (yellow-green halo)", "arrhythmias (toxicity)"
        ],
        "contraindications": [
            "ventricular fibrillation", "hypertrophic obstructive cardiomyopathy",
            "Wolf-Parkinson-White syndrome", "digoxin toxicity"
        ],
        "category": "Cardiac Glycoside / Antiarrhythmic",
    },
}
