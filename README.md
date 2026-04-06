# AMEX Credit Risk Early Warning System

## Overview
This project builds an end-to-end credit risk prediction system using the American Express default dataset.

The goal is to identify customers at high risk of default and support proactive risk monitoring through:
- scalable data storage in BigQuery
- SQL-based feature engineering
- machine learning modelling in Python
- planned deployment with FastAPI and Streamlit

## Architecture
- **Data Storage:** Google BigQuery
- **Data Processing:** BigQuery SQL + Python
- **Feature Engineering:** BigQuery SQL
- **Modelling:** Python (Scikit-learn, LightGBM)
- **Deployment (planned):** FastAPI + Streamlit

## Project Structure
```text
amex_credit_risk/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── models/
├── notebooks/
├── sql/
├── src/
├── reports/
├── api/
├── app/
├── .gitignore
├── README.md
└── requirements.txt
```

## Deployment

### Run the FastAPI app
```bash
uvicorn api.main:app --reload

## Run the Streamlit dashboard
streamlit run app/streamlit_app.py

```
## Local test checklist

Run these in order:

```bash
python -m src.train
uvicorn api.main:app --reload
streamlit run app/streamlit_app.py
```

## Author
Daniel Diala
