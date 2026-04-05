CREATE OR REPLACE TABLE `amex-46887.amex_risk.customer_missingness_features` AS
SELECT
  customer_ID,
  ANY_VALUE(target) AS target,
  COUNT(*) AS n_statements,

  COUNTIF(P_2 IS NULL) AS P_2_missing_count,
  SAFE_DIVIDE(COUNTIF(P_2 IS NULL), COUNT(*)) AS P_2_missing_pct,

  COUNTIF(D_39 IS NULL) AS D_39_missing_count,
  SAFE_DIVIDE(COUNTIF(D_39 IS NULL), COUNT(*)) AS D_39_missing_pct,

  COUNTIF(B_9 IS NULL) AS B_9_missing_count,
  SAFE_DIVIDE(COUNTIF(B_9 IS NULL), COUNT(*)) AS B_9_missing_pct,

  COUNTIF(R_1 IS NULL) AS R_1_missing_count,
  SAFE_DIVIDE(COUNTIF(R_1 IS NULL), COUNT(*)) AS R_1_missing_pct,

  COUNTIF(B_11 IS NULL) AS B_11_missing_count,
  SAFE_DIVIDE(COUNTIF(B_11 IS NULL), COUNT(*)) AS B_11_missing_pct,

  COUNTIF(S_3 IS NULL) AS S_3_missing_count,
  SAFE_DIVIDE(COUNTIF(S_3 IS NULL), COUNT(*)) AS S_3_missing_pct

FROM `amex-46887.amex_risk.train_joined`
GROUP BY customer_ID;
