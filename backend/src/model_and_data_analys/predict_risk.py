from fastapi import HTTPException, status
from backend.src.database.db import AsyncSession
from backend.src.models.models import HeartRisk
from backend.src.model_and_data_analys.converting_for_model import convert_form_to_features
from backend.src.services.risk_form_service import get_form_from_user
import joblib
import pandas as pd

model = joblib.load("train_model\heart_rf_best.pkl")
df = pd.read_csv("train_model\heart_2020_cleaned.csv")

feature_order = [
        'BMI', 'Smoking', 'AlcoholDrinking', 'Stroke', 'PhysicalHealth',
        'MentalHealth', 'DiffWalking', 'Sex', 'AgeCategory', 'Diabetic',
        'PhysicalActivity', 'GenHealth', 'SleepTime', 'Asthma', 'KidneyDisease', 'SkinCancer'
    ]

async def predict_risk(features: dict):
    X = pd.DataFrame([{col: features[col] for col in feature_order}])

    prob = model.predict_proba(X)[0][1] 
    return round(prob * 100, 2)

  
# kullanıcı yaşına ve cinsiyete göre aynen onun gibi insanların ortalama riski ve kullanıcının riski karşılaştırma

async def filter_by_user_age_and_sex(session: AsyncSession, user_id: int):
    user_data = await get_form_from_user(session=session, user_id = user_id)
    
    features = await convert_form_to_features(user_data)
    
    group_df = df[
        (df["AgeCategory"] == features["AgeCategory"]) &
        (df["Sex"] == features["Sex"])
    ].copy()

    if group_df.empty:
        return {
            "message": "Bu yaş ve cinsiyet grubunda veri bulunamadı"
        }

    group_size = len(group_df)

    X_group = group_df[feature_order]

    group_probs = model.predict_proba(X_group)[:, 1]
    group_df["PredictedRisk"] = group_probs * 100
    
    group_mean_risk = group_df["PredictedRisk"].mean()

    #Ortalama grubun riski
    average_group_risk = f"{group_mean_risk:.2f}%"


    # İnme geçiren ve geçirmeyen grubu
    stroke_yes = (group_df["Stroke"] == "Yes").sum()
    stroke_no = (group_df["Stroke"] == "No").sum()

    stroke_yes_percent = round((stroke_yes / group_size) * 100, 2)
    stroke_no_percent = round((stroke_no / group_size) * 100, 2)
    
    # aynı yaş ve cinsiyet düşük riskli olan insanlar
    low_risk_df = group_df[group_df["PredictedRisk"] < 40]

    if low_risk_df.empty:
        return {
            "message": "Bu yaş ve cinsiyet için düşük riskli grup bulunamadı."
        }
    
    compare_numeric = ["BMI", "MentalHealth", "SleepTime"]
    compare_categorical = ["Smoking", "AlcoholDrinking", "PhysicalActivity"]

    differences = {}

    for col in compare_numeric:
        group_avg = low_risk_df[col].mean()
        user_val = features[col]

        differences[col] = {
            "type": "numeric",
            "user": round(user_val, 2),
            "low_risk_avg": round(group_avg, 2),
            "difference": round(user_val - group_avg, 2)
        }

    for col in compare_categorical:
        group_yes_percent = (low_risk_df[col] == "Yes").mean() * 100
        user_val = features[col]

        differences[col] = {
            "type": "categorical",
            "user": user_val,
            "low_risk_yes_percent": round(group_yes_percent, 2),
            "user_vs_group": (
                "Aynı" if (
                    (user_val == "Yes" and group_yes_percent > 50) or
                    (user_val == "No" and group_yes_percent <= 50)
                )
                else "Farklı"
            )
        }

    insights = []

    # BMI
    if differences["BMI"]["difference"] > 0:
        insights.append(
            f"BMI değeriniz düşük riskli olan insanlara göre "
            f"{differences['BMI']['difference']:.1f} puan daha yüksektir."
        )

    # Mental sağlık
    if differences["MentalHealth"]["difference"] > 0:
        insights.append(
            "Mental sağlık problemi gün sayınız düşük riskli gruba göre daha fazladır."
        )

    # Sigara
    if features["Smoking"] == "Yes":
        insights.append(
            f"Düşük riskli grupta sigara içenlerin oranı yalnızca "
            f"%{differences['Smoking']['low_risk_yes_percent']:.1f}."
        )

    # Fiziksel aktivite
    if features["PhysicalActivity"] == "No":
        insights.append(
            "Düşük riskli olan insanların büyük çoğunluğu fiziksel olarak aktiftir."
        )

    # Alkol
    if features["AlcoholDrinking"] == "Yes":
        insights.append(
            f"Düşük riskli grupta alkol kullananların oranı yalnızca "
            f"%{differences['AlcoholDrinking']['low_risk_yes_percent']:.1f}."
        )

    # Uyku süresi
    sleep_diff = differences["SleepTime"]["difference"]

    if sleep_diff < -1:
        insights.append(
            f"Uyku süreniz düşük riskli olan insanlara göre "
            f"{abs(sleep_diff):.1f} saat daha azdır."
        )
    elif sleep_diff > 1:
        insights.append(
            f"Uyku süreniz düşük riskli olan insanlara göre "
            f"{sleep_diff:.1f} saat daha fazladır."
        )

    risk_percent = float(await predict_risk(features))
    risk_level = (
        "Düşük seviye" if risk_percent < 35 else
        "Orta seviye" if risk_percent < 70 else
        "Yüksek seviye"
    )

    diff = risk_percent - group_mean_risk

    if diff > 0:
        conclusion = f"Kullanıcının riski, grubun ortalamasından daha yüksektir {diff:.2f}%"
    else:
        conclusion = f"Kullanıcının riski, grubun ortalama riskinin altındadır {abs(diff):.2f}%"

    return {
        "features": features,
        "User_risk_percent": f"{round(risk_percent, 5)}%",
        "User_risk_level": risk_level,
        "group_size_by_user_age_and_sex": group_size,
        "average_group_risk": average_group_risk,
        "difference": conclusion,
        "interpretation": (
            f"Sizin yaş ve cinsiyet grubundaki kişilerin"
            f" yüzde {stroke_yes_percent}'i daha önce inme geçirmiştir, "
            f" yüzde {stroke_no_percent}'inde ise inme geçirmemiştir."
        ),
        "Sizin yaş ve cinsiyet grubundaki kişilerin": insights,
        "differences_numeric": {
            "BMI": differences["BMI"]["difference"] if differences["BMI"]["difference"] > 0 else None,
            "MentalHealth": differences["MentalHealth"]["difference"] if differences["MentalHealth"]["difference"] > 0 else None,
            "Smoking": differences["Smoking"]["low_risk_yes_percent"] if features["Smoking"] == "Yes" else None,
            "PhysicalActivity": 1 if features["PhysicalActivity"] == "No" else None,
            "Alcohol": differences["AlcoholDrinking"]["low_risk_yes_percent"] if features["AlcoholDrinking"] == "Yes" else None,
            "Sleep": sleep_diff if abs(sleep_diff) > 1 else None
        }
    }








