-- sql/01_profile_raw_data.sql

-- 1. train_data row count and distinct customers
SELECT
  COUNT(*) AS train_rows,
  COUNT(DISTINCT customer_ID) AS train_customers
FROM `amex-46887.amex_risk.train_data_raw`;

-- 2. label row count and distinct customers
SELECT
  COUNT(*) AS label_rows,
  COUNT(DISTINCT customer_ID) AS label_customers
FROM `amex-46887.amex_risk.train_labels_raw`;

-- 3. class balance
SELECT
  target,
  COUNT(*) AS n_customers
FROM `amex-46887.amex_risk.train_labels_raw`
GROUP BY target
ORDER BY target;

-- 4. label customers missing from train_data_raw
SELECT
  COUNT(*) AS missing_label_customers
FROM `amex-46887.amex_risk.train_labels_raw` l
LEFT JOIN (
  SELECT DISTINCT customer_ID
  FROM `amex-46887.amex_risk.train_data_raw`
) t
USING (customer_ID)
WHERE t.customer_ID IS NULL;

-- 5. statement count distribution
WITH statement_counts AS (
  SELECT
    customer_ID,
    COUNT(*) AS n_statements
  FROM `amex-46887.amex_risk.train_data_raw`
  GROUP BY customer_ID
)
SELECT
  n_statements,
  COUNT(*) AS n_customers
FROM statement_counts
GROUP BY n_statements
ORDER BY n_statements;

-- 6. summary of sequence lengths
WITH statement_counts AS (
  SELECT
    customer_ID,
    COUNT(*) AS n_statements
  FROM `amex-46887.amex_risk.train_data_raw`
  GROUP BY customer_ID
)
SELECT
  MIN(n_statements) AS min_statements,
  MAX(n_statements) AS max_statements,
  AVG(n_statements) AS avg_statements
FROM statement_counts;
