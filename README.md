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


## Current Progress
- BigQuery project setup completed
- Raw data loaded into BigQuery
- Initial feature engineering pipeline created
- Customer-level feature table built

### Observations

- Dataset contains ~458k customers
- Strong class imbalance (~75% non-default)
- No missing customers between labels and transactions
- Most customers have 10–13 monthly statements
- Sequence data confirms time-series structure

## Next Steps
- Validate data integrity
- Expand feature engineering
- Train baseline model
- Add model explainability
- Deploy prediction API

## Author
Daniel Diala
