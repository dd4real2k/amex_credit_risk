-- sql/04_latest_record_features.sql

CREATE OR REPLACE TABLE `amex-46887.amex_risk.customer_features_latest` AS
WITH ordered AS (
  SELECT
    customer_ID,
    target,
    S_2,
    P_2,
    D_39,
    B_9,
    R_1,
    B_11,
    S_3,
    ROW_NUMBER() OVER (PARTITION BY customer_ID ORDER BY S_2 ASC) AS rn_asc,
    ROW_NUMBER() OVER (PARTITION BY customer_ID ORDER BY S_2 DESC) AS rn_desc
  FROM `amex-46887.amex_risk.train_joined`
),
first_last AS (
  SELECT
    customer_ID,
    ANY_VALUE(target) AS target,

    MAX(CASE WHEN rn_asc = 1 THEN P_2 END) AS P_2_first,
    MAX(CASE WHEN rn_desc = 1 THEN P_2 END) AS P_2_last,

    MAX(CASE WHEN rn_asc = 1 THEN D_39 END) AS D_39_first,
    MAX(CASE WHEN rn_desc = 1 THEN D_39 END) AS D_39_last,

    MAX(CASE WHEN rn_asc = 1 THEN B_9 END) AS B_9_first,
    MAX(CASE WHEN rn_desc = 1 THEN B_9 END) AS B_9_last,

    MAX(CASE WHEN rn_asc = 1 THEN R_1 END) AS R_1_first,
    MAX(CASE WHEN rn_desc = 1 THEN R_1 END) AS R_1_last,

    MAX(CASE WHEN rn_asc = 1 THEN B_11 END) AS B_11_first,
    MAX(CASE WHEN rn_desc = 1 THEN B_11 END) AS B_11_last,

    MAX(CASE WHEN rn_asc = 1 THEN S_3 END) AS S_3_first,
    MAX(CASE WHEN rn_desc = 1 THEN S_3 END) AS S_3_last

  FROM ordered
  GROUP BY customer_ID
)
SELECT
  *,
  P_2_last - P_2_first AS P_2_delta,
  D_39_last - D_39_first AS D_39_delta,
  B_9_last - B_9_first AS B_9_delta,
  R_1_last - R_1_first AS R_1_delta,
  B_11_last - B_11_first AS B_11_delta,
  S_3_last - S_3_first AS S_3_delta
FROM first_last;
