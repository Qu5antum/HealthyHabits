import pandas as pd
import numpy as np
import joblib
from collections import Counter
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    classification_report,
    f1_score
)
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns


RANDOM_STATE = 42
TEST_SIZE = 0.2
TARGET_COL = "HeartDisease"


# Görsel ayarlar
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (8,5)

df = pd.read_csv("heart_2020_cleaned.csv")

df.info()
df.head()

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
class_weights = {0: 1.0, 1: scale_pos_weight}
print(f"scale_pos_weight = {scale_pos_weight:.3f}")

# Pipeline
xgb_pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", XGBClassifier(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.9,
        colsample_bytree=0.8,
        eval_metric="logloss",
        scale_pos_weight=scale_pos_weight,
        random_state=RANDOM_STATE
    ))
])

rf_pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", RandomForestClassifier(
        n_estimators=400,
        max_depth=5,
        min_samples_split=10,
        min_samples_leaf=5,
        class_weight=class_weights,
        n_jobs=1,
        random_state=RANDOM_STATE
    ))
])

xgb_pipeline.fit(X_train, y_train)
rf_pipeline.fit(X_train, y_train)

def evaluate_model(name, model):
    y_proba = model.predict_proba(X_test)[:, 1]

    roc = roc_auc_score(y_test, y_proba)
    pr = average_precision_score(y_test, y_proba)

    thresholds = np.linspace(0.1, 0.9, 81)
    f1_scores = [
        f1_score(y_test, (y_proba >= t).astype(int))
        for t in thresholds
    ]
    best_t = thresholds[np.argmax(f1_scores)]

    y_pred = (y_proba >= best_t).astype(int)

    print(f"\n===== {name} =====")
    print(f"ROC-AUC : {roc:.4f}")
    print(f"PR-AUC  : {pr:.4f}")
    print(f"Best threshold: {best_t:.2f}")
    print(classification_report(y_test, y_pred))

    return roc, pr

xgb_roc, xgb_pr = evaluate_model("XGBoost", xgb_pipeline)
rf_roc, rf_pr = evaluate_model("Random Forest", rf_pipeline)

# 10. Pikle formatin dosyasina kaydetme
XGB_MODEL_PATH = "heart_xgb_best.pkl"
RF_MODEL_PATH = "heart_rf_best.pkl"
joblib.dump(xgb_pipeline, XGB_MODEL_PATH)
joblib.dump(rf_pipeline, RF_MODEL_PATH)

print("\nModels saved:")
print(XGB_MODEL_PATH)
print(RF_MODEL_PATH)

xgb_model = joblib.load("heart_xgb_best.pkl")
rf_model = joblib.load("heart_rf_best.pkl")

print("======XGB_model======")
print(xgb_model)
print("======RF_model======")
print(rf_model)

def plot_roc_bar(models):
    names = []
    auc_values = []

    for name, model in models.items():
        y_proba = model.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, y_proba) * 100

        names.append(name)
        auc_values.append(auc)

    plt.figure(figsize=(6, 4))
    bars = plt.bar(names, auc_values, color=["tab:blue", "tab:orange"] )

    plt.ylabel("ROC-AUC (%)")
    plt.title("ROC-AUC Comparison")

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}%",
            ha="center",
            va="bottom"
        )

    plt.ylim(0, 100)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

plot_roc_bar({
    "XGBoost": xgb_pipeline,
    "Random Forest": rf_pipeline
})

