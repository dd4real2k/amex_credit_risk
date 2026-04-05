CREATE OR REPLACE TABLE `amex-46887.amex_risk.customer_features_first` AS
WITH ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY customer_ID
      ORDER BY CAST(S_2 AS DATE) ASC
    ) AS rn
  FROM `amex-46887.amex_risk.train_joined`
)
SELECT
  customer_ID,
  target,
  CAST(S_2 AS DATE) AS first_statement_date,
  P_2 AS P_2_first,
  D_39 AS D_39_first,
  B_9 AS B_9_first,
  R_1 AS R_1_first,
  B_11 AS B_11_first,
  S_3 AS S_3_first
FROM ranked
WHERE rn = 1;
