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
    severity_text,
    affected_direction,         
    number_of_lanes_restricted,
    temporary_limit,
    location_descriptor,
    traffic_restriction_type
FROM stg_traffic