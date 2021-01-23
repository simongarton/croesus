SELECT category, sub_category, count(*) AS records
FROM category
GROUP BY category, sub_category
HAVING count(*) > 1