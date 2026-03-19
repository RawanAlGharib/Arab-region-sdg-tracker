CREATE VIEW master_sdg_data AS 

WITH CleanData AS (
    SELECT 
        c.country_name,
        c.region_code,
        i.indicator_name,
        f.year,
        f.indicator_value
    FROM fact_sdg_data AS f
    JOIN dim_countries AS c ON f.country_code = c.country_code
    JOIN dim_indicators AS i ON f.indicator_code = i.indicator_code
)

SELECT 
    country_name,
    region_code,
    indicator_name,
    year,
    ROUND(indicator_value, 2) AS current_value,
    ROUND(LAG(indicator_value) OVER (PARTITION BY country_name, indicator_name ORDER BY year), 2) AS previous_year_value,
    ROUND(indicator_value - LAG(indicator_value) OVER (PARTITION BY country_name, indicator_name ORDER BY year), 2) AS net_change
FROM CleanData
WHERE country_name IN (
    'Algeria', 'Bahrain', 'Comoros', 'Djibouti', 'Egypt, Arab Rep.', 
    'Iraq', 'Jordan', 'Kuwait', 'Lebanon', 'Libya', 
    'Mauritania', 'Morocco', 'Oman', 'Qatar', 'Saudi Arabia', 
    'Somalia', 'Sudan', 'Syrian Arab Republic', 'Tunisia', 
    'United Arab Emirates', 'West Bank and Gaza', 'Yemen, Rep.'
)
ORDER BY country_name, indicator_name, year DESC;


SELECT * FROM master_sdg_data;