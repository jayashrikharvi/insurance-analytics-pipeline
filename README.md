# Insurance Analytics – Python + MySQL + Tableau

The goal of this project is to analyze patient–hospital–insurance data, build predictive models for insurance charges, and visualize key insights through professional dashboards.
- Loads hospital & patient CSVs with Python
- Cleans and enriches the data
- Trains a regression model to predict insurance charges
- Stores data in MySQL (`insurance_db`)
- Creates an analytics view using SQL CTEs + window functions
- Visualizes metrics in Tableau (hospital performance, risk groups, rolling averages)

CSV Files → Python (ETL + ML) → MySQL Database → SQL View → Tableau Dashboards
## Tableau Dashboards

### 1. Insurance Charges by Age  
![Age vs Charges](tableau/screenshots/age_vs_charges.png)

### 2. Hospital Performance  
![Hospital Performance](tableau/screenshots/hospital_performance.png)

### 3. Risk Group Distribution  
![Risk Group](tableau/screenshots/risk_group.png)
