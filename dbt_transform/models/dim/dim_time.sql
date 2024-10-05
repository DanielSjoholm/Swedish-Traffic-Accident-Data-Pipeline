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
    {{ dbt_utils.generate_surrogate_key(['id', 'start_time']) }} AS time_id,
    start_time,
    EXTRACT(YEAR FROM start_time) AS start_year,
    EXTRACT(MONTH FROM start_time) AS start_month,
    EXTRACT(DAY FROM start_time) AS start_day,
    EXTRACT(HOUR FROM start_time) AS start_hour,
    EXTRACT(MINUTE FROM start_time) AS start_minute,
    EXTRACT(SECOND FROM start_time) AS start_second,
    end_time,
    EXTRACT(YEAR FROM end_time) AS end_year,
    EXTRACT(MONTH FROM end_time) AS end_month,
    EXTRACT(DAY FROM end_time) AS end_day,
    EXTRACT(HOUR FROM end_time) AS end_hour,
    EXTRACT(MINUTE FROM end_time) AS end_minute,
    EXTRACT(SECOND FROM end_time) AS end_second,
    creation_time,
    EXTRACT(YEAR FROM creation_time) AS creation_year,
    EXTRACT(MONTH FROM creation_time) AS creation_month,
    EXTRACT(DAY FROM creation_time) AS creation_day,
    EXTRACT(HOUR FROM creation_time) AS creation_hour,
    EXTRACT(MINUTE FROM creation_time) AS creation_minute,
    EXTRACT(SECOND FROM creation_time) AS creation_second

FROM src_time