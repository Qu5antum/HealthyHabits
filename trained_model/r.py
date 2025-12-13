import joblib


model = joblib.load("heart_model.pkl")
print(model.feature_names_in_)