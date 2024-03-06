

-- This query returns unique professional titles from the responses and the quantity of occurrences
SELECT title, COUNT(title) AS title_count
FROM responses
GROUP BY title
ORDER BY title_count DESC;
