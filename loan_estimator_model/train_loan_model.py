# ============================================================
# Loan Amount Estimation Model - Training Script
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# ------------------------------------------------------------
# 1. Load Dataset
# ------------------------------------------------------------
df = pd.read_csv("loan_amount_prediction_dataset_v2.csv")
print("✅ Data Loaded Successfully!\n")
print(df.head())

# ------------------------------------------------------------
# 2. Exploratory Data Analysis (EDA)
# ------------------------------------------------------------
print("\n--- Basic Information ---")
print(df.info())

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Descriptive Statistics ---")
print(df.describe())

# Correlation Matrix
corr = df.corr(numeric_only=True)
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap - Loan Amount Prediction")
plt.show()

# Correlation with target variable
print("\n--- Correlation with Loan_Amount ---")
corr_loan = corr["Loan_Amount"].sort_values(ascending=False)
print(corr_loan)

# Key Insights
print("\n--- Insights ---")
print("1️⃣ Monthly_Income has the strongest positive correlation (0.59) with Loan_Amount.")
print("2️⃣ Age and Credit_Score have mild influence.")
print("3️⃣ Existing_Loan_Amount and Num_of_Dependents have negative correlations (reduce eligibility).")

# ------------------------------------------------------------
# 3. Prepare Features & Target
# ------------------------------------------------------------
X = df[["Age", "Monthly_Income", "Credit_Score", "Loan_Tenure_Years", 
        "Existing_Loan_Amount", "Num_of_Dependents"]]
y = df["Loan_Amount"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("\nData Split Completed:")
print(f"Train Size: {X_train.shape}, Test Size: {X_test.shape}")

# ------------------------------------------------------------
# 4. Train Model
# ------------------------------------------------------------
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)
print("\n✅ Model Training Completed!")

# ------------------------------------------------------------
# 5. Evaluate Model
# ------------------------------------------------------------
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n--- Model Performance ---")
print(f"Mean Absolute Error (MAE): ₹{mae:,.2f}")
print(f"R² Score: {r2:.4f}")

# ------------------------------------------------------------
# 6. Save Trained Model
# ------------------------------------------------------------
model_filename = "loan_amount_estimation_model.pkl"
joblib.dump(model, model_filename)
print(f"\n💾 Model saved as '{model_filename}'")

# ------------------------------------------------------------
# 7. Example Prediction
# ------------------------------------------------------------
sample_input = [[30, 50000, 750, 10, 100000, 2]]
predicted_loan = model.predict(sample_input)[0]
print(f"\n💡 Example Prediction → Estimated Loan Amount: ₹{predicted_loan:,.2f}")
