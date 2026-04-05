CREATE OR REPLACE TABLE `amex-46887.amex_risk.model_dataset_v1` AS
SELECT
  b.*,
  l.latest_statement_date,
  l.P_2_latest,
  l.D_39_latest,
  l.B_9_latest,
  l.R_1_latest,
  l.B_11_latest,
  l.S_3_latest
FROM `amex-46887.amex_risk.customer_features_base` AS b
JOIN `amex-46887.amex_risk.customer_features_latest` AS l
USING (customer_ID, target);
