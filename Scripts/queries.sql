

-- This query returns professional titles from the responses and the quantity of occurrences
-- How similar are the professional titles? Can we group some together?
SELECT formatted_title, COUNT(formatted_title) AS title_count
FROM formatted_responses
GROUP BY formatted_title
ORDER BY title_count DESC;
