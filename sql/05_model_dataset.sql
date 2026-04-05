-- sql/05_model_dataset.sql

CREATE OR REPLACE TABLE `amex-46887.amex_risk.model_dataset_v1` AS
SELECT
  b.customer_ID,
  b.target,
  b.n_statements,

  b.P_2_avg, b.P_2_min, b.P_2_max, b.P_2_std, b.P_2_nulls,
  b.D_39_avg, b.D_39_min, b.D_39_max, b.D_39_std, b.D_39_nulls,
  b.B_9_avg, b.B_9_min, b.B_9_max, b.B_9_std, b.B_9_nulls,
  b.R_1_avg, b.R_1_min, b.R_1_max, b.R_1_std, b.R_1_nulls,
  b.B_11_avg, b.B_11_min, b.B_11_max, b.B_11_std, b.B_11_nulls,
  b.S_3_avg, b.S_3_min, b.S_3_max, b.S_3_std, b.S_3_nulls,

  l.P_2_first, l.P_2_last, l.P_2_delta,
  l.D_39_first, l.D_39_last, l.D_39_delta,
  l.B_9_first, l.B_9_last, l.B_9_delta,
  l.R_1_first, l.R_1_last, l.R_1_delta,
  l.B_11_first, l.B_11_last, l.B_11_delta,
  l.S_3_first, l.S_3_last, l.S_3_delta

FROM `amex-46887.amex_risk.customer_features_base` b
LEFT JOIN `amex-46887.amex_risk.customer_features_latest` l
USING (customer_ID, target);
