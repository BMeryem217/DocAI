import joblib
import pandas as pd               # NEW
from flask_cors import CORS
from flask import Flask, render_template, request

app = Flask(__name__)              # fixed typo
CORS(app)

# 1. Liste complète des symptômes
SYMPTOMS = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", 
    "shivering", "chills", "joint_pain", "stomach_pain", "acidity", 
    "ulcers_on_tongue", "muscle_wasting", "vomiting", "burning_micturition", 
    "spotting_urination", "fatigue", "weight_gain", "anxiety", 
    "cold_hands_and_feets", "mood_swings", "weight_loss", "restlessness", 
    "lethargy", "patches_in_throat", "irregular_sugar_level", "cough", 
    "high_fever", "sunken_eyes", "breathlessness", "sweating", "dehydration", 
    "indigestion", "headache", "yellowish_skin", "dark_urine", "nausea", 
    "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "constipation", 
    "abdominal_pain", "diarrhoea", "mild_fever", "yellow_urine", "yellowing_of_eyes", 
    "acute_liver_failure", "swelling_of_stomach", "swelled_lymph_nodes", "malaise", 
    "blurred_and_distorted_vision", "phlegm", "throat_irritation", "redness_of_eyes", 
    "sinus_pressure", "runny_nose", "congestion", "chest_pain", "weakness_in_limbs", 
    "fast_heart_rate", "pain_during_bowel_movements", "pain_in_anal_region", 
    "bloody_stool", "irritation_in_anus", "neck_pain", "dizziness", "cramps", 
    "bruising", "obesity", "swollen_legs", "swollen_blood_vessels", "puffy_face_and_eyes", 
    "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "excessive_hunger", 
    "extra_marital_contacts", "drying_and_tingling_lips", "slurred_speech", "knee_pain", 
    "hip_joint_pain", "muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness", 
    "spinning_movements", "loss_of_balance", "unsteadiness", "weakness_of_one_body_side", 
    "loss_of_smell", "bladder_discomfort", "foul_smell_of_urine", "continuous_feel_of_urine", 
    "passage_of_gases", "internal_itching", "toxic_look_(typhos)", "depression", "irritability", 
    "muscle_pain", "altered_sensorium", "red_spots_over_body", "belly_pain", "abnormal_menstruation", 
    "dischromic_patches", "watering_from_eyes", "increased_appetite", "polyuria", "family_history", 
    "mucoid_sputum", "rusty_sputum", "lack_of_concentration", "visual_disturbances", 
    "receiving_blood_transfusion", "receiving_unsterile_injections", "coma", "stomach_bleeding", 
    "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload_1", "blood_in_sputum", 
    "prominent_veins_on_calf", "palpitations", "painful_walking", "pus_filled_pimples", "blackheads", 
    "scurring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", 
    "blister", "red_sore_around_nose", "yellow_crust_ooze"
]

# 2. Liste des noms de maladies
DISEASES = [
    "(vertigo) Paroymsal  Positional Vertigo", "AIDS", "Acne", "Alcoholic hepatitis", "Allergy",
    "Arthritis", "Bronchial Asthma", "Cervical spondylosis", "Chicken pox", "Chronic cholestasis",
    "Common Cold", "Dengue", "Diabetes ", "Dimorphic hemorrhoids(piles)", "Drug Reaction", "Fungal infection",
    "GERD", "Gastroenteritis", "Heart attack", "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E",
    "Hypertension ", "Hyperthyroidism", "Hypoglycemia", "Hypothyroidism", "Impetigo", "Jaundice", "Malaria",
    "Migraine", "Osteoarthritis", "Paralysis (brain hemorrhage)", "Peptic ulcer disease", "Pneumonia", "Psoriasis",
    "Tuberculosis", "Typhoid", "Urinary tract infection", "Varicose veins", "hepatitis A"
]

# 3. Chargement du modèle entraîné (même dossier que app.py)
model = joblib.load('model.joblib')

# 4. Chargement du fichier précautions  -------------------------------  <<< NEW >>>
#    ➜  Save your Excel as CSV named “precautions.csv”
prec_df = pd.read_csv('precautions.csv')
#    Build lookup: {"Disease": ["p1", "p2", ...]}
desc_df = pd.read_csv('disease_descriptions.csv')
descriptions = dict(zip(desc_df['Disease'], desc_df['Description'].fillna('')))
precautions_lookup = (
    prec_df.set_index('Disease')
           .apply(lambda r: [r[c] for c in prec_df.columns[1:] if pd.notna(r[c])],
                  axis=1)
           .to_dict()
)
# ---------------------------------------------------------------------


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # a. Vecteur binaire
        user_symptoms_vector = [1 if request.form.get(symptom) else 0
                                for symptom in SYMPTOMS]

        # b. Prédiction
        prediction_index = model.predict([user_symptoms_vector])[0]
        disease_name = (DISEASES[prediction_index]
                        if 0 <= prediction_index < len(DISEASES)
                        else "Unknown Disease")
        description = descriptions.get(disease_name) or "Description non disponible pour l’instant."
        # c. Précautions pour la maladie prédite ----------------------  <<< NEW >>>
        precautions = precautions_lookup.get(disease_name, [])
        # --------------------------------------------------------------

        # d. Symptômes cochés pour l’affichage
        checked_symptoms = [
            SYMPTOMS[i].replace("_", " ")
            for i, val in enumerate(user_symptoms_vector) if val
        ]

        return render_template(
            "result.html",
            symptoms=checked_symptoms,
            disease_name=disease_name,
            precautions=precautions,
            description=description       # <<< NEW >>>
        )

    return render_template("index.html", symptoms=SYMPTOMS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
