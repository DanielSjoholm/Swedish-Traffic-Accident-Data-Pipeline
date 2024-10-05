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
    {{ capitalize_first_letter(trim_spaces("COALESCE(message_type, 'Inte specifierat')")) }} AS message_type,
    {{ capitalize_first_letter(trim_spaces("COALESCE(message_code, 'Inte specifierat')")) }} AS message_code,
    {{ capitalize_first_letter(trim_spaces("COALESCE(message, 'Inte specifierat')")) }} AS message,
    {{ capitalize_first_letter(trim_spaces("COALESCE(severity_text, 'Inte specifierat')")) }} AS severity_text

FROM src_message