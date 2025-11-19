import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 1. READ CSV FILES ---------------------------------------------------------

# Adjust paths only if your folder structure is different
hospital_path = "C:/projects/InsuranceAnalytics/data/Hospital.csv"
patient_path = "C:/projects/InsuranceAnalytics/data/Patient.csv"
prediction_path = "C:/projects/InsuranceAnalytics/data/assume.csv"

hospital = pd.read_csv(hospital_path)
patient = pd.read_csv(patient_path)
prediction = pd.read_csv(prediction_path)

# Normalize column names to lowercase for consistency
hospital.columns = hospital.columns.str.lower()
patient.columns = patient.columns.str.lower()
prediction.columns = prediction.columns.str.lower()

# assume.csv has 'predict_charges' -> rename to 'predicted_charges'
if "predict_charges" in prediction.columns:
    prediction = prediction.rename(columns={"predict_charges": "predicted_charges"})

print("CSV files loaded successfully.")

# 2. (OPTIONAL) SIMPLE CLEANING ---------------------------------------------

# Strip whitespace from hospital_id & hospital_name if any
if "hospital_id" in hospital.columns:
    hospital["hospital_id"] = hospital["hospital_id"].astype(str).str.strip()

if "hospital_id" in patient.columns:
    patient["hospital_id"] = patient["hospital_id"].astype(str).str.strip()

# Ensure smoker is numeric 0/1
if "smoker" in patient.columns:
    patient["smoker"] = patient["smoker"].astype(int)

if "smoker" in prediction.columns:
    prediction["smoker"] = prediction["smoker"].astype(int)

print("Basic cleaning done.")

# 3. OPTIONAL: TRAIN A SIMPLE MODEL ON PATIENT DATA ------------------------

# We'll use patient table to train a regression model to predict charges
feature_cols = ["age", "bmi", "children", "smoker"]
ml_df = patient.dropna(subset=feature_cols + ["charges"])

X = ml_df[feature_cols]
y = ml_df["charges"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

print("ML model trained. R2 on train:", model.score(X_train, y_train))
print("R2 on test:", model.score(X_test, y_test))

# Apply model to prediction dataset to create a second prediction column
common_cols = [col for col in feature_cols if col in prediction.columns]
if common_cols:
    prediction["predicted_charges_model"] = model.predict(prediction[common_cols])
else:
    prediction["predicted_charges_model"] = np.nan

print("Predictions generated for assume.csv.")

# 4. CONNECT TO MYSQL ------------------------------------------------------


USER = "root"
PASSWORD = "password"  
HOST = "localhost"
PORT = 3306
DB = "insurance_db"

connection_url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
engine = create_engine(connection_url)

print("Connected to MySQL.")

# 5. DROP TABLES IF THEY ALREADY EXIST -------------------------------------

with engine.begin() as conn:
    conn.execute(text("DROP TABLE IF EXISTS insurance_prediction"))
    conn.execute(text("DROP TABLE IF EXISTS patient"))
    conn.execute(text("DROP TABLE IF EXISTS hospital"))

print("Old tables dropped (if existed).")

# 6. WRITE DATAFRAMES INTO MYSQL -------------------------------------------

hospital.to_sql("hospital", engine, if_exists="replace", index=False)
print("hospital table created and loaded.")

patient.to_sql("patient", engine, if_exists="replace", index=False)
print("patient table created and loaded.")

prediction.to_sql("insurance_prediction", engine, if_exists="replace", index=False)
print("insurance_prediction table created and loaded.")

print("All tables loaded into MySQL successfully.")

# 7. OPTIONAL: CREATE VIEW FROM PYTHON (same as SQL in section 2.2) -------

view_sql = """
CREATE OR REPLACE VIEW insurance_analytics AS
WITH base_data AS (
    SELECT
        p.hospital_id,
        p.age,
        p.gender,
        p.bmi,
        p.children,
        p.smoker,
        p.charges,
        h.hospital_name
    FROM patient p
    LEFT JOIN hospital h
        ON p.hospital_id = h.hospital_id
),
analytics AS (
    SELECT
        b.*,
        CASE
            WHEN b.smoker = 1 AND b.bmi > 30 THEN 'High Risk'
            WHEN b.smoker = 1 THEN 'Medium Risk'
            ELSE 'Low Risk'
        END AS risk_group,
        AVG(b.charges) OVER (PARTITION BY b.hospital_id) AS avg_hospital_charges,
        ROW_NUMBER() OVER (
            PARTITION BY b.hospital_id ORDER BY b.charges DESC
        ) AS rank_in_hospital,
        AVG(b.charges) OVER (
            ORDER BY b.age
            ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
        ) AS rolling_6patient_avg
    FROM base_data b
)
SELECT * FROM analytics;
"""

with engine.begin() as conn:
    conn.execute(text(view_sql))

print("View insurance_analytics created.")

print("✅ ETL + ML + DB setup complete.")
