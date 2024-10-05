WITH ts AS (
    SELECT *
    FROM {{ ref('src_traffic_situation') }}
),

m AS (
    SELECT *
    FROM {{ ref('src_message') }}
),

l AS (
    SELECT *
    FROM {{ ref('src_location') }}
),

t AS (
    SELECT *
    FROM {{ ref('src_time') }}
)

SELECT
    ts.id AS id,
    {{ dbt_utils.generate_surrogate_key(['m.id', 'm.message_code']) }} AS message_key,
    {{ dbt_utils.generate_surrogate_key(['l.id']) }} AS location_key,
    {{ dbt_utils.generate_surrogate_key(['t.id', 't.start_time']) }} AS time_key,
    ts.icon_id,
    ts.severity_text,
    ts.affected_direction,
    ts.number_of_lanes_restricted,
    ts.temporary_limit,
    ts.location_descriptor,
    ts.traffic_restriction_type
FROM 
    ts
LEFT JOIN
    m ON ts.id = m.id
LEFT JOIN
    l ON ts.id = l.id
LEFT JOIN
    t ON ts.id = t.id