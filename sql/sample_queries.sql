USE insurance_db;

-- ============================================================
-- SAMPLE ANALYTICS QUERIES FOR DASHBOARD INSIGHTS
-- ============================================================

-- 1. Top 10 highest-charge patients
SELECT patient_id, age, bmi, charges
FROM patient
ORDER BY charges DESC
LIMIT 10;

-- 2. Average charges by region
SELECT region, AVG(charges) AS avg_region_charges
FROM insurance_analytics
GROUP BY region;

-- 3. Hospital performance summary
SELECT hospital_name,
       ROUND(AVG(charges), 2) AS avg_charges,
       ROUND(SUM(charges), 2) AS total_revenue
FROM insurance_analytics
GROUP BY hospital_name
ORDER BY avg_charges DESC;

-- 4. Number of patients in each risk group
SELECT risk_group, COUNT(*) AS total_patients
FROM insurance_analytics
GROUP BY risk_group;

-- 5. Patients with charges above hospital average
SELECT *
FROM insurance_analytics
WHERE charges > avg_hospital_charges;

-- 6. Rolling average trend by patient ID
SELECT patient_id, age, charges, rolling_6patient_avg
FROM insurance_analytics
ORDER BY patient_id ASC;
