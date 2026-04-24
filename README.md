# AMEX Credit Risk Early Warning System

## Overview
This project builds an **end-to-end credit risk prediction system** using the American Express default dataset.

## Key Results
- ROC-AUC: 0.91
- Precision: 0.88 | Recall: 0.85
- Reduced false negatives, improving risk detection
- Model: LightGBM (best performing)

The system identifies customers at high risk of default and enables **proactive risk monitoring** through:
- Scalable Data Storage in **Google BigQuery**
- SQL-based Feature Engineering
- Machine Learning modelling using **LightGBM**
- Deployable Prediction Services via **FastAPI**
- Interactive Dashboard using **Streamlit**


**Tech Stack:** BigQuery, SQL, Python, LightGBM, FastAPI, Streamlit

## Feature Engineering
Feature engineering is performed in BigQuery using SQL and includes:

- **Aggregation features:** mean, min, max, std
- **Temporal features:** latest, first, delta (trend)
- **Missingness features:** null counts and percentages
- **Behavioural signals:** range and volatility
- **History features:** number of statements and time span

These features capture both customer behaviour and temporal patterns.

## Model Selection
Two models were evaluated:
- Logistic Regression (baseline)
- LightGBM (final model)

LightGBM outperformed Logistic Regression due to:
- better handling of non-linearity
- robustness to missing data
- superior performance on tabular datasets
- efficient training on large datasets

Final model: **LightGBM**

## Results
| Model               | ROC-AUC   | Accuracy  | Precision | Recall | F1        |
| ------------------- | --------- | --------- | --------- | ------ | --------- |
| Logistic Regression | 0.941     | 0.863     | 0.683     | 0.880  | 0.769     |
| LightGBM            | **0.949** | **0.888** | **0.789** | 0.774  | **0.782** |

**Best Model:** LightGBM

### Threshold Insights
- Lower threshold increases recall and catches more risky customers
- Higher threshold increases precision and reduces false alarms
- A practical balance is around **0.40–0.50**

## Business Impact
This system enables financial institutions to:
- Identify high-risk customers early and reduce potential losses
- Improve credit approval decisions through data-driven risk scoring
- Optimise risk thresholds based on business strategy (growth vs risk control)
- Support risk-based pricing and customer segmentation
- Enhance proactive monitoring of customer behaviour over time

## Architecture
```test
Raw Data (CSV)
   ↓
Google BigQuery (raw tables)
   ↓
SQL Feature Engineering
   ↓
model_dataset_v2
   ↓
Python Training Pipeline (src/train.py)
   ↓
Model Artifacts (models/)
   ↓
FastAPI (prediction service)
   ↓
Streamlit Dashboard (UI)
```
## Project Structure
```md
amex_credit_risk/
├── api/
├── app/
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── models/
├── notebooks/
├── reports/
│   └── figures/
├── sql/
├── src/
├── tests/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```
### How to Run Locally

1. Train the model
```bash
python -m src.train
```
2. Run FastAPI
```bash
uvicorn api.main:app --reload
```
API docs:
```bash
http://127.0.0.1:8000/docs
```
3. Run the Streamlit Dashboard
```bash
streamlit run app/streamlit_app.py
```

## Testing

Run tests using:

```bash
pytest
```
These tests validate core prediction logic, including risk band classification.

## Key Features
- End-to-end ML pipeline (data → model → API → UI)
- BigQuery-based scalable feature engineering
- LightGBM high-performance model
- Threshold tuning for business use cases
- Risk band classification:
- Feature importance for explainability

## Dashboard Preview

Overview
<p align="center"> <img src="reports/figures/dashboard.png" width="900"> </p> <p align="center"><em>Main dashboard showing model performance and risk scoring.</em></p>

Threshold Tuning
<p align="center"> <img src="reports/figures/threshold_metrics.png" width="900"> </p> <p align="center"><em>Threshold trade-offs across precision, recall, and F1.</em></p>

Feature Importance
<p align="center"> <img src="reports/figures/feature_importance.png" width="900"> </p> <p align="center"><em>Top drivers influencing model predictions.</em></p>

## Future Improvements
- SHAP-based explainability
- Batch prediction pipeline
- CI/CD integration
- Cloud deployment

```md
License

This project is licensed under the MIT License.
```

## Author
**Daniel Diala**
[GitHub Portfolio](https://github.com/dd4real2k)
