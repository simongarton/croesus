-- total value of all investments, based on last value record

SELECT sum(value)
FROM investment_value
         INNER JOIN (
    SELECT i.id, max(iv.date) AS max_date
    FROM investment_value iv
             INNER JOIN investment i ON iv.investment_id = i.id
    GROUP BY i.id) sub ON investment_value.investment_id = sub.id AND investment_value.date = sub.max_date;

-- individual value of all investments, based on last value record

SELECT investment_value.id, sum(value)
FROM investment_value
         INNER JOIN (
    SELECT i.id, max(iv.date) AS max_date
    FROM investment_value iv
             INNER JOIN investment i ON iv.investment_id = i.id
    GROUP BY i.id) sub ON investment_value.investment_id = sub.id AND investment_value.date = sub.max_date
GROUP BY investment_value.id;

-- most recent date for each investment - used for subquery

SELECT i.id, max(iv.date) AS date
FROM investment_value iv
         INNER JOIN investment i ON iv.investment_id = i.id
GROUP BY i.id;