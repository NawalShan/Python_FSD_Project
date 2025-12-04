# train_model.py
import os
from pathlib import Path
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt

# === Configuration ===
DATA_PATH = "loan_amount_prediction_dataset_v2.csv"   # update path if needed
OUT_DIR = Path("loan_tool_output")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# === Load data ===
df = pd.read_csv(DATA_PATH)
print("Loaded dataset shape:", df.shape)
print("Columns:", list(df.columns))

# === Quick EDA (console-friendly) ===
print("\nMissing values per column:")
print(df.isnull().sum())

print("\nNumeric summary:")
print(df.describe().T)

# If you have commas/currency in numeric columns, pre-clean:
for col in df.columns:
    if df[col].dtype == object:
        if df[col].astype(str).str.contains(',', regex=False).any() or df[col].astype(str).str.contains('₹', regex=False).any():
            df[col] = df[col].astype(str).str.replace('₹','',regex=False).str.replace(',','',regex=False)
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                pass

# === Select features & target ===
# Columns expected by the problem (adjust if your CSV has different names)
FEATURE_COLS = ['Age', 'Monthly_Income', 'Credit_Score', 'Loan_Tenure_Years', 'Existing_Loan_Amount', 'Num_of_Dependents']
TARGET_COL = 'Loan_Amount'

# Validate these columns exist
missing = [c for c in FEATURE_COLS + [TARGET_COL] if c not in df.columns]
if missing:
    raise SystemExit(f"Missing columns in dataset: {missing}. Update FEATURE_COLS / TARGET_COL accordingly.")

# Drop NA rows for modeling
model_df = df[FEATURE_COLS + [TARGET_COL]].dropna()
print("Rows used for modeling:", len(model_df))

X = model_df[FEATURE_COLS].values
y = model_df[TARGET_COL].values

# === Train-test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === Model training ===
rf = RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)

# === Evaluation ===
y_pred = rf.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)  # changed from squared=False parameter
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("RMSE:", rmse)
print("R2:", r2)

# Feature importances
importances = pd.Series(rf.feature_importances_, index=FEATURE_COLS).sort_values(ascending=False)
print("\nFeature importances:")
print(importances)

# === Save model & report ===
model_path = OUT_DIR / "loan_amount_model.joblib"
joblib.dump(rf, model_path)
report = {
    "model_metrics": {"MAE": float(mae), "RMSE": float(rmse), "R2": float(r2)},
    "feature_importances": importances.to_dict(),
    "feature_columns": FEATURE_COLS,
    "target_column": TARGET_COL
}
with open(OUT_DIR / "report.json", "w") as f:
    json.dump(report, f, indent=2)
print("Saved model to:", model_path)
print("Saved report to:", OUT_DIR / "report.json")

# === Simple plots for EDA (saved to OUT_DIR) ===
# 1) Monthly Income vs Loan Amount scatter
plt.figure(figsize=(6,4))
plt.scatter(model_df['Monthly_Income'], model_df[TARGET_COL], s=10)
plt.xlabel('Monthly_Income')
plt.ylabel(TARGET_COL)
plt.title('Monthly Income vs Loan Amount')
plt.tight_layout()
plt.savefig(OUT_DIR / "income_vs_loan_scatter.png")
plt.close()

# 2) Median Loan by Credit Score bucket
df['credit_bucket'] = pd.cut(df['Credit_Score'], bins=[299,600,650,700,750,800,850], labels=['<600','600-650','650-700','700-750','750-800','800+'])
median_by_bucket = df.groupby('credit_bucket')[TARGET_COL].median().reset_index()
median_by_bucket.to_csv(OUT_DIR / "median_loan_by_credit_bucket.csv", index=False)

print("Saved EDA plots and tables to", OUT_DIR)
