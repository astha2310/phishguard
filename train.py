"""
PhishGuard - model training
Built by Astha Patel

Trains three models on data/dataset.csv, compares them on a held-out
test set, and saves the best one to models/ for app.py and predict.py.

Run:  python3 train.py
"""

import os
import warnings

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

DATA_PATH = "data/dataset.csv"
MODEL_DIR = "models"

print("=" * 50)
print("TRAINING PHISHGUARD")
print("=" * 50)

# 1. Load the feature dataset built by build_dataset.py
df = pd.read_csv(DATA_PATH)
feature_cols = [c for c in df.columns if c not in ("url", "label")]
X, y = df[feature_cols], df["label"]
print(f"\nLoaded {len(df)} URLs ({int(y.sum())} phishing, {int((y == 0).sum())} legitimate)")
print(f"Features: {len(feature_cols)}")

# 2. Hold out 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Candidate models
models = {
    "Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1),
}
try:
    from xgboost import XGBClassifier
    models["XGBoost"] = XGBClassifier(
        n_estimators=300, max_depth=6, learning_rate=0.1,
        eval_metric="logloss", random_state=42,
    )
except ImportError:
    print("(xgboost not installed - skipping XGBoost)")

# 4. Train and compare on AUC-ROC
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    proba = model.predict_proba(X_test)[:, 1]
    results[name] = roc_auc_score(y_test, proba)
    print(f"  {name:<20} AUC-ROC: {results[name] * 100:.2f}%")

best_name = max(results, key=results.get)
best_model = models[best_name]
print(f"\nBest model: {best_name} ({results[best_name] * 100:.2f}% AUC-ROC)")
print("\n=== Test-set report ===")
print(classification_report(y_test, best_model.predict(X_test), target_names=["Legitimate", "Phishing"]))

# 5. Save for app.py / predict.py
os.makedirs(MODEL_DIR, exist_ok=True)
joblib.dump(best_model, os.path.join(MODEL_DIR, "best_model.pkl"))
joblib.dump(feature_cols, os.path.join(MODEL_DIR, "feature_cols.pkl"))
print("Saved models/best_model.pkl and models/feature_cols.pkl")

print("\nNote: a high test score only means the model separates THIS dataset well.")
print("Run `python3 predict.py --real-world` to see how it handles real websites.")
