# AMEX Credit Risk Early Warning System

## Overview
This project builds an end-to-end credit risk prediction system using the American Express default dataset. The goal is to identify high-risk customers early and support proactive risk management.

## Architecture
- Data Storage: Google BigQuery
- Data Processing: SQL + Python
- Feature Engineering: BigQuery SQL
- Modelling: Python (Scikit-learn, LightGBM)
- Deployment (planned): FastAPI + Streamlit

## Project Structure
amex_credit_risk/
├── data/
├── notebooks/
├── sql/
├── src/
├── models/
├── api/
├── app/


## Current Progress
- BigQuery project setup completed
- Raw data loaded into BigQuery
- Initial feature engineering pipeline created
- Customer-level feature table built

## Next Steps
- Validate data integrity
- Expand feature engineering
- Train baseline model
- Add model explainability
- Deploy prediction API

## Author
Daniel Diala
