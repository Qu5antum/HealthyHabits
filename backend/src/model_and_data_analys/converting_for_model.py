from typing import Dict
from backend.src.models.schemas import HeartRiskInput

async def convert_form_to_features(form: HeartRiskInput) -> Dict:
    # BMI
    bmi = round(form.weight / ((form.height / 100) ** 2), 2)

    age = form.age

    if age < 25:
        age_cat = "18-24"
    elif age < 30:
        age_cat = "25-29"
    elif age < 35:
        age_cat = "30-34"
    elif age < 40:
        age_cat = "35-39"
    elif age < 45:
        age_cat = "40-44"
    elif age < 50:
        age_cat = "45-49"
    elif age < 55:
        age_cat = "50-54"
    elif age < 60:
        age_cat = "55-59"
    elif age < 65:
        age_cat = "60-64"
    elif age < 70:
        age_cat = "65-69"
    elif age < 75:
        age_cat = "70-74"
    elif age < 80:
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