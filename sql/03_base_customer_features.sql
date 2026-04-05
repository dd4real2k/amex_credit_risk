CREATE OR REPLACE TABLE `amex-46887.amex_risk.customer_features_base` AS
SELECT
  customer_ID,
  ANY_VALUE(target) AS target,
  COUNT(*) AS n_statements,

  AVG(P_2) AS P_2_avg,
  MIN(P_2) AS P_2_min,
  MAX(P_2) AS P_2_max,
  STDDEV(P_2) AS P_2_std,

  AVG(D_39) AS D_39_avg,
  MIN(D_39) AS D_39_min,
  MAX(D_39) AS D_39_max,
  STDDEV(D_39) AS D_39_std,

  AVG(B_9) AS B_9_avg,
  MIN(B_9) AS B_9_min,
  MAX(B_9) AS B_9_max,
  STDDEV(B_9) AS B_9_std,

  AVG(R_1) AS R_1_avg,
  MIN(R_1) AS R_1_min,
  MAX(R_1) AS R_1_max,
  STDDEV(R_1) AS R_1_std,

  AVG(B_11) AS B_11_avg,
  MIN(B_11) AS B_11_min,
  MAX(B_11) AS B_11_max,
  STDDEV(B_11) AS B_11_std,

  AVG(S_3) AS S_3_avg,
  MIN(S_3) AS S_3_min,
  MAX(S_3) AS S_3_max,
  STDDEV(S_3) AS S_3_std,

FROM `amex-46887.amex_risk.train_joined`
GROUP BY customer_ID;
