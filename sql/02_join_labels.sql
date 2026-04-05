CREATE OR REPLACE TABLE `amex-46887.amex_risk.train_joined` AS
SELECT
  t.*,
  l.target
FROM `amex-46887.amex_risk.train_data_raw` AS t
JOIN `amex-46887.amex_risk.train_labels_raw` AS l
USING (customer_ID);
