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
    {{ capitalize_first_letter(trim_spaces("COALESCE(ts.icon_id, 'ej specificerat')")) }} AS situation_type,
    {{ capitalize_first_letter(trim_spaces("COALESCE(ts.affected_direction, 'ej specificerat')")) }} AS affected_direction,
    COALESCE(ts.number_of_lanes_restricted, -1) AS number_of_lanes_restricted,
    {{ capitalize_first_letter(trim_spaces("COALESCE(ts.temporary_limit, 'ej specificerat')")) }} AS temporary_limit,
    {{ capitalize_first_letter(trim_spaces("COALESCE(ts.location_descriptor, 'ej specificerat')")) }} AS location_descriptor,
    {{ capitalize_first_letter(trim_spaces("COALESCE(ts.traffic_restriction_type, 'ej specificerat')")) }} AS traffic_restriction_type
FROM 
    ts
LEFT JOIN
    m ON ts.id = m.id
LEFT JOIN
    l ON ts.id = l.id
LEFT JOIN
    t ON ts.id = t.id