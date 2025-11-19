-- ============================================================
--  CREATE INSURANCE ANALYTICS DATABASE & TABLE STRUCTURE
-- ============================================================

DROP DATABASE IF EXISTS insurance_db;
CREATE DATABASE insurance_db;
USE insurance_db;

-- ============================================================
-- HOSPITAL TABLE
-- ============================================================
DROP TABLE IF EXISTS hospital;

CREATE TABLE hospital (
    hospital_id INT PRIMARY KEY,
    hospital_name VARCHAR(100),
    region VARCHAR(50)
);

-- ============================================================
-- PATIENT TABLE
-- ============================================================
DROP TABLE IF EXISTS patient;

CREATE TABLE patient (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_id INT,
    age INT,
    gender VARCHAR(10),
    bmi DECIMAL(5,2),
    children INT,
    smoker TINYINT,
    charges DECIMAL(10,2),
    FOREIGN KEY (hospital_id) REFERENCES hospital(hospital_id)
);

-- ============================================================
-- INSURANCE PREDICTION TABLE (MODEL OUTPUT)
-- ============================================================
DROP TABLE IF EXISTS insurance_prediction;

CREATE TABLE insurance_prediction (
    id INT PRIMARY KEY AUTO_INCREMENT,
    age INT,
    bmi DECIMAL(5,2),
    smoker TINYINT,
    predicted_charges DECIMAL(10,2)
);

-- ============================================================
-- CLEAN STRUCTURE READY FOR DATA LOAD
-- ============================================================
