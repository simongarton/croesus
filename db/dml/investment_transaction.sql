INSERT INTO investment_transaction (date, investment_id, value)
SELECT date, id, -value
FROM investment
WHERE id in (11,12,13,14,15);