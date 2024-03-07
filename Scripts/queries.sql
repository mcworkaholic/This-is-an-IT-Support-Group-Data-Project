

-- This query returns professional titles from the responses and the quantity of occurrences
-- How similar are the professional titles? Can we group some together?
SELECT title, COUNT(title) AS title_count
FROM responses
GROUP BY title
ORDER BY title_count DESC;


-- For comparison between the professional titles that were supplied and the ones that were formatted
SELECT 
    o.id, 
    o.title AS original_title, 
    f.formatted_title
FROM 
    original_responses o
INNER JOIN 
    formatted_responses f ON o.id = f.id
ORDER BY 
    o.id ASC;