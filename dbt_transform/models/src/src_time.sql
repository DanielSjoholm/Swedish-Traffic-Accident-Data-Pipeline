{{
  config(
    materialized = 'ephemeral',
  )
}}

WITH stg_traffic AS (
    SELECT
        *
    FROM {{ source('traffic_analytics_db', 'stg_traffic') }}
)

SELECT
    id,
    start_time,
    end_time,
    creation_time
FROM stg_traffic