USE insurance_db;

-- ============================================================
-- ANALYTICS VIEW USING CTEs & WINDOW FUNCTIONS
-- ============================================================

CREATE OR REPLACE VIEW insurance_analytics AS
WITH base_data AS (
    SELECT
        p.patient_id,
        p.hospital_id,
        p.age,
        p.gender,
        p.bmi,
        p.children,
        p.smoker,
        p.charges,
        h.hospital_name,
        h.region
    FROM patient p
    LEFT JOIN hospital h
        ON p.hospital_id = h.hospital_id
),

analytics AS (
    SELECT
        b.*,

        -- Risk classification logic
        CASE
            WHEN b.smoker = 1 AND b.bmi > 30 THEN 'High Risk'
            WHEN b.smoker = 1 THEN 'Medium Risk'
            ELSE 'Low Risk'
        END AS risk_group,

        -- Window Function 1: Hospital-wise average charges
        AVG(b.charges) OVER (
            PARTITION BY b.hospital_id
        ) AS avg_hospital_charges,

        -- Window Function 2: Region-wise average charges
        AVG(b.charges) OVER (
            PARTITION BY b.region
        ) AS avg_region_charges,

        -- Window Function 3: Ranking highest charge patient per hospital
        ROW_NUMBER() OVER (
            PARTITION BY b.hospital_id
            ORDER BY b.charges DESC
        ) AS rank_in_hospital,

        -- Window Function 4: Rolling average of last 6 patients
        AVG(b.charges) OVER (
            ORDER BY b.patient_id
            ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
        ) AS rolling_6patient_avg

    FROM base_data b
)

SELECT * FROM analytics;
