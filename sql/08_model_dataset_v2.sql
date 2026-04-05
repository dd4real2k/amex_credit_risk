CREATE OR REPLACE TABLE `amex-46887.amex_risk.model_dataset_v2` AS
SELECT
  b.customer_ID,
  b.target,
  b.n_statements,

  b.P_2_avg,
  b.P_2_min,
  b.P_2_max,
  b.P_2_std,
  (b.P_2_max - b.P_2_min) AS P_2_range,

  b.D_39_avg,
  b.D_39_min,
  b.D_39_max,
  b.D_39_std,
  (b.D_39_max - b.D_39_min) AS D_39_range,

  b.B_9_avg,
  b.B_9_min,
  b.B_9_max,
  b.B_9_std,
  (b.B_9_max - b.B_9_min) AS B_9_range,

  b.R_1_avg,
  b.R_1_min,
  b.R_1_max,
  b.R_1_std,
  (b.R_1_max - b.R_1_min) AS R_1_range,

  b.B_11_avg,
  b.B_11_min,
  b.B_11_max,
  b.B_11_std,
  (b.B_11_max - b.B_11_min) AS B_11_range,

  b.S_3_avg,
  b.S_3_min,
  b.S_3_max,
  b.S_3_std,
  (b.S_3_max - b.S_3_min) AS S_3_range,

  l.latest_statement_date,
  l.P_2_latest,
  l.D_39_latest,
  l.B_9_latest,
  l.R_1_latest,
  l.B_11_latest,
  l.S_3_latest,

  f.first_statement_date,
  f.P_2_first,
  f.D_39_first,
  f.B_9_first,
  f.R_1_first,
  f.B_11_first,
  f.S_3_first,

  (l.P_2_latest - f.P_2_first) AS P_2_delta,
  (l.D_39_latest - f.D_39_first) AS D_39_delta,
  (l.B_9_latest - f.B_9_first) AS B_9_delta,
  (l.R_1_latest - f.R_1_first) AS R_1_delta,
  (l.B_11_latest - f.B_11_first) AS B_11_delta,
  (l.S_3_latest - f.S_3_first) AS S_3_delta,

  m.P_2_missing_count,
  m.P_2_missing_pct,
  m.D_39_missing_count,
  m.D_39_missing_pct,
  m.B_9_missing_count,
  m.B_9_missing_pct,
  m.R_1_missing_count,
  m.R_1_missing_pct,
  m.B_11_missing_count,
  m.B_11_missing_pct,
  m.S_3_missing_count,
  m.S_3_missing_pct,

  DATE_DIFF(l.latest_statement_date, f.first_statement_date, DAY) AS history_days

FROM `amex-46887.amex_risk.customer_features_base` AS b
JOIN `amex-46887.amex_risk.customer_features_latest` AS l
  USING (customer_ID, target)
JOIN `amex-46887.amex_risk.customer_features_first` AS f
  USING (customer_ID, target)
JOIN `amex-46887.amex_risk.customer_missingness_features` AS m
  USING (customer_ID, target);
