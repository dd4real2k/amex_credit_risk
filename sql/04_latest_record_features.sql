CREATE OR REPLACE TABLE `amex-46887.amex_risk.customer_features_latest` AS
WITH ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY customer_ID
      ORDER BY CAST(S_2 AS DATE) DESC
    ) AS rn
  FROM `amex-46887.amex_risk.train_joined`
)
SELECT
  customer_ID,
  target,
  CAST(S_2 AS DATE) AS latest_statement_date,
  P_2 AS P_2_latest,
  D_39 AS D_39_latest,
  B_9 AS B_9_latest,
  R_1 AS R_1_latest,
  B_11 AS B_11_latest,
  S_3 AS S_3_latest
FROM ranked
WHERE rn = 1;
