{{
  config(
    materialized = 'view',
  )
}}

WITH src_time AS (
    SELECT
        *
    FROM {{ ref('src_time') }}
)

SELECT
    {{dbt_utils.generate_surrogate_key(['id', 'start_time']) }} AS time_id,
    COALESCE({{format_date('start_time')}}, '1970-01-01') AS start_time,
    COALESCE(EXTRACT(YEAR FROM start_time), -1) AS start_year,
    COALESCE(EXTRACT(MONTH FROM start_time), -1) AS start_month,
    COALESCE(EXTRACT(DAY FROM start_time), -1) AS start_day,
    COALESCE(EXTRACT(HOUR FROM start_time), -1) AS start_hour,
    COALESCE(EXTRACT(MINUTE FROM start_time), -1) AS start_minute,
    COALESCE(EXTRACT(SECOND FROM start_time), -1) AS start_second,
    COALESCE({{format_date('end_time')}}, '1970-01-01') AS end_time,
    COALESCE(EXTRACT(YEAR FROM end_time), -1) AS end_year,
    COALESCE(EXTRACT(MONTH FROM end_time), -1) AS end_month,
    COALESCE(EXTRACT(DAY FROM end_time), -1) AS end_day,
    COALESCE(EXTRACT(HOUR FROM end_time), -1) AS end_hour,
    COALESCE(EXTRACT(MINUTE FROM end_time), -1) AS end_minute,
    COALESCE(EXTRACT(SECOND FROM end_time), -1) AS end_second,
    COALESCE({{format_date('creation_time')}}, '1970-01-01') AS creation_time,
    COALESCE(EXTRACT(YEAR FROM creation_time), -1) AS creation_year,
    COALESCE(EXTRACT(MONTH FROM creation_time), -1) AS creation_month,
    COALESCE(EXTRACT(DAY FROM creation_time), -1) AS creation_day,
    COALESCE(EXTRACT(HOUR FROM creation_time), -1) AS creation_hour,
    COALESCE(EXTRACT(MINUTE FROM creation_time), -1) AS creation_minute,
    COALESCE(EXTRACT(SECOND FROM creation_time), -1) AS creation_second

FROM src_time