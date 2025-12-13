from backend.src.models.schemas import HeartRiskInput
import joblib
import pandas as pd
from typing import Dict

model = joblib.load("heart_model.pkl")


async def convert_form_to_features(form: HeartRiskInput) -> Dict:
    # BMI
    bmi = round(form.weight / ((form.height / 100) ** 2), 2)

    age = form.age  
    if age < 30:
        age_cat = "18-29"
    elif age < 45:
        age_cat = "30-44"
    elif age < 60:
        age_cat = "45-54"
    elif age < 60:
        age_cat = "55-59"
    elif age < 65:
        age_cat = "60-64"
    elif age < 65:
        age_cat = "65-69"
    elif age < 70:
        age_cat = "70-74"
    elif age < 75:
        age_cat = "75-79"
    else:
        age_cat = "80 or older"

    physical_health = min(max(getattr(form, "physical_health", 0) or 0, 0), 30)
    mental_health = min(max(getattr(form, "mental_health", 0) or 0, 0), 30)

    return {
        "BMI": bmi,
        "Smoking": form.smoke,                     
        "AlcoholDrinking": form.alcohol,           
        "Stroke": form.stroke,   
        "PhysicalHealth": float(physical_health),        
        "MentalHealth": float(mental_health),            
        "DiffWalking": form.difficulty_walking,   
        "Sex": form.sex,                          
        "AgeCategory": age_cat,                   
        "Diabetic": form.high_sugar_level,        
        "PhysicalActivity": form.physical_activity, 
        "GenHealth": form.general_health,         
        "SleepTime": float(form.sleep),                 
        "Asthma": form.asthma,                  
        "KidneyDisease": form.kidney_problems,    
        "SkinCancer": form.skin_diseases          
    }


async def predict_risk(features: dict):
    feature_order = [
        'BMI', 'Smoking', 'AlcoholDrinking', 'Stroke', 'PhysicalHealth',
        'MentalHealth', 'DiffWalking', 'Sex', 'AgeCategory', 'Diabetic',
        'PhysicalActivity', 'GenHealth', 'SleepTime', 'Asthma', 'KidneyDisease', 'SkinCancer'
    ]

    X = pd.DataFrame([{col: features[col] for col in feature_order}])

    prob = model.predict_proba(X)[0][1] 
    return round(prob * 100, 2)
