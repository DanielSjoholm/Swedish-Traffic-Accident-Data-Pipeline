
{{
    config(
    materialized = 'view',
    )
}}

WITH src_message AS (
    SELECT
        *
    FROM {{ ref('src_message') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['id', 'message_code']) }} AS message_id,
    message_type,
    message_code,
    message,
    severity_text,
    safety_related_message
from src_message