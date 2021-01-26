SELECT sum(value)
FROM investment_transaction
WHERE value::NUMERIC < 0;