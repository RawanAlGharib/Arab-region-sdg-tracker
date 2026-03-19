# Arab Region SDG Progress Tracker: 2013–2023

## Executive Summary
This project is an end-to-end data pipeline and interactive macroeconomic dashboard designed to track Sustainable Development Goal (SDG) progress across the 22 states of the Arab region. By extracting and transforming a decade of longitudinal data, this tool visualizes structural economic shifts, focusing on key indicators such as Female Labor Force Participation and GDP per Capita Growth.

**[View the Interactive Tableau Dashboard Here]**(https://public.tableau.com/views/ArabRegionSDGProgressTracker20132023/)

## ETL Architecture & Tech Stack
* **Data Extraction:** Python (`wbgapi`, `pandas`)
* **Database Management:** SQLite (`.db` generated via Python)
* **Data Transformation:** SQL (CTEs, `JOIN`s, Window Functions)
* **Data Visualization:** Tableau Public

## Methodology & Pipeline Workflow
1. **Automated Extraction:** Engineered a Python script utilizing the World Bank API to programmatically extract historical data for targeted SDG indicators across the Arab region.
2. **Database Modeling:** Designed a local SQLite star schema consisting of centralized fact tables and descriptive dimension tables (country metadata, indicator definitions).
3. **Advanced SQL Transformations:** * Cleaned and joined the relational data.
   * Utilized the `LAG()` window function to engineer a `net_change` metric, calculating exact Year-over-Year (YoY) momentum for every country and indicator.
4. **Visual Analytics:** Connected the SQL output to Tableau to build an interactive choropleth map and a comparative time-series momentum chart.

## Key Analytical Features & Data Governance
* **Pre-SDG Baseline Tracking:** Intentionally included data from 2013–2014 to establish historical macroeconomic momentum prior to the official UN adoption of the 2030 Agenda in 2015, allowing for a more accurate assessment of policy impact.
* **Handling Data Sparsity:** Maintained statistical integrity by transparently navigating missing data points (`NULL` values) in conflict-affected or fragile contexts (e.g., Sudan, Yemen) rather than forcing inaccurate zero values.
* **Accurate Rate Aggregation:** Configured dashboard aggregations to calculate *Averages* rather than *Sums* to mathematically protect rate-based metrics (like percentages) when user filters are adjusted.
* **Diverging Visualizations:** Implemented diverging color palettes centered at zero to clearly distinguish between economic growth and macroeconomic contraction (negative GDP growth).

## Repository Structure
* `etl_pipeline.py`: Python script for World Bank API data extraction.
* `data_transformations.sql`: SQL queries featuring the data cleaning, table joins, and YoY momentum calculations.
* `arab_region_sdg_master.csv`: The final, cleaned dataset exported from the database, structured for Tableau ingestion.
* `dashboard_screenshot.png`: High-resolution capture of the final interactive dashboard.
