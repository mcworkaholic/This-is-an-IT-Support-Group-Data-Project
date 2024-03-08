

/* This query returns formatted, professional titles from the responses and the quantity of occurrences for each.
How similar are the professional titles? Can we group some together? */
SELECT formatted_title, COUNT(formatted_title) AS title_count
FROM formatted_responses
GROUP BY formatted_title
ORDER BY title_count DESC;  

/* This query gets the average pay for IT professionals in Texas who are salaried. 
yields $76918.55 */
SELECT avg(pay) 
FROM formatted_responses 
WHERE state = 'Texas' AND pay_type = 'Salary'

/* This query gets the average pay for IT professionals whose title = 'IT Manager' and are paid a salary.
yields $83261.29.55 */
SELECT avg(pay) 
FROM formatted_responses 
WHERE formatted_title = 'IT Manager' AND pay_type = 'Salary'

/* This query gets the quantity of IT professionals whose pay type = 'Salary'.
yields 848 */
SELECT COUNT(pay_type) 
FROM formatted_responses 
WHERE pay_type = 'Salary'

/* This query gets the quantity of IT professionals whose pay type = 'Hourly'.
yields 263 */
SELECT COUNT(pay_type) 
FROM formatted_responses 
WHERE pay_type = 'Hourly'

/* This query identifies the states with the highest number of IT professionals.
Shows which states are major hubs for IT talent. */
SELECT state, COUNT(*) AS professional_count
FROM formatted_responses
GROUP BY state
ORDER BY professional_count DESC;

/* This query calculates the average salary for IT professionals across different job tiers.
Aids in understanding how compensation varies by tier. */
SELECT job_tier, AVG(pay) AS average_salary
FROM formatted_responses
WHERE pay_type = 'Salary'
GROUP BY job_tier
ORDER BY job_tier;

/* This query finds the top-paying cities for IT professionals.
Highlights cities where IT professionals are compensated most generously. */
SELECT city, state, AVG(pay) AS average_pay
FROM formatted_responses
WHERE pay_type = 'Salary'
GROUP BY city, state
ORDER BY average_pay DESC
LIMIT 10;

/* This query counts the number of IT professionals in each country/region,
providing a global perspective on the distribution of IT jobs. */
SELECT country_region, COUNT(*) AS professional_count
FROM formatted_responses
GROUP BY country_region
ORDER BY professional_count DESC;

/* This query evaluates the distribution of pay types (Salary vs. Hourly) across job tiers,
offering insight into common compensation structures. */
SELECT job_tier, pay_type, COUNT(*) AS count
FROM formatted_responses
GROUP BY job_tier, pay_type
ORDER BY job_tier, pay_type;

/* This query identifies how many IT professionals are in urban versus rural settings,
based on whether the 'city' field is populated. */
SELECT CASE WHEN city = '' THEN 'Rural' ELSE 'Urban' END AS setting, COUNT(*) AS count
FROM formatted_responses
GROUP BY setting;

/* This query calculates the average hourly wage for IT professionals,
facilitating comparisons with salaried positions. */
SELECT AVG(pay) AS average_hourly_wage
FROM formatted_responses
WHERE pay_type = 'Hourly';

/* This query finds the geographic coordinates (lat, lon) with the highest concentration of IT professionals,
useful for pinpointing IT hubs on a map. */
SELECT lat, lon, COUNT(*) AS professional_count
FROM formatted_responses
GROUP BY lat, lon
ORDER BY professional_count DESC
LIMIT 10;

/* This query determines the variance in pay within the top job tier,
helping to assess pay equity and range. */
SELECT job_tier, MAX(pay) - MIN(pay) AS pay_variance
FROM formatted_responses
WHERE job_tier = '3'
GROUP BY job_tier;

/* This query compares the number of IT professionals in different pay brackets,
shedding light on income distribution within the sector. */
SELECT 
  CASE 
    WHEN pay < 50000 THEN 'Under $50k'
    WHEN pay BETWEEN 50000 AND 99999 THEN '$50k - $99k'
    WHEN pay >= 100000 THEN 'Over $100k'
  END AS pay_bracket,
  COUNT(*) AS count
FROM formatted_responses
WHERE pay_type = 'Salary'
GROUP BY pay_bracket
ORDER BY pay_bracket;