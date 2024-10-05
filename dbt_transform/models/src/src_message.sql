{{
    config (
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
    message_type,
    message,
    severity_text,
    message_code
from stg_traffic
