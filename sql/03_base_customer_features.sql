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
  MAX(D_39) AS D_39_max,
  STDDEV(D_39) AS D_39_std

FROM `amex-46887.amex_risk.train_joined`
GROUP BY customer_ID;
