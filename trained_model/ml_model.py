# train_xgb_model.py
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier
from collections import Counter

# ===== CONFIG =====
DATA_PATH = "heart_2020_cleaned.csv"
TARGET_COL = "HeartDisease"
MODEL_PATH = "heart_model.pkl"
RANDOM_STATE = 42
TEST_SIZE = 0.2
# ==================

# 1. Load data
df = pd.read_csv(DATA_PATH)

# Remove Race
if "Race" in df.columns:
    df = df.drop(columns=["Race"])
    print("Column 'Race' removed from dataset.")

# Convert Yes/No → 1/0 automatically
if df[TARGET_COL].dtype == "object":
    df[TARGET_COL] = df[TARGET_COL].map(
        lambda x: 1 if str(x).lower() in ("yes", "y", "1", "true") else 0
    )

y = df[TARGET_COL]
X = df.drop(columns=[TARGET_COL])

# 2. Detect column types
cat_cols = [c for c in X.columns if X[c].dtype == "object"]
num_cols = [c for c in X.columns if c not in cat_cols]

print("Numeric:", num_cols)
print("Categorical:", cat_cols)

# 3. Preprocessing
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols)
])

# 4. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
)

print("Train distribution:", Counter(y_train))
print("Test distribution:", Counter(y_test))

# 5. Handle imbalance
neg, pos = np.sum(y_train == 0), np.sum(y_train == 1)
scale_pos_weight = neg / (pos + 1e-9)
print(f"scale_pos_weight = {scale_pos_weight:.3f}")

# 6. Create model
model = XGBClassifier(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.9,
    colsample_bytree=0.8,
    eval_metric="logloss",
    scale_pos_weight=scale_pos_weight,
    random_state=RANDOM_STATE
)

# 7. Build pipeline
pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", model)
])

# 8. Fit
pipeline.fit(X_train, y_train)

# 9. Evaluate
y_proba = pipeline.predict_proba(X_test)[:, 1]
y_pred = pipeline.predict(X_test)

print("AUC:", roc_auc_score(y_test, y_proba))
print("\nClassification report:")
print(classification_report(y_test, y_pred))

# 10. Save
joblib.dump(pipeline, MODEL_PATH)
print("Model saved →", MODEL_PATH)
