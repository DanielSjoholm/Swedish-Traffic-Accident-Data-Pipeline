WITH ts AS (
    SELECT 
        *
    FROM {{ ref('fct_traffic_situation') }}
),

l AS (
    SELECT
        *
    FROM {{ ref('dim_location') }}
),

m AS (
    SELECT
        *
    FROM {{ ref('dim_message') }}
),

t AS (
    SELECT
        *
    FROM {{ ref('dim_time') }}
)

SELECT
    ts.id AS id,
    t.creation_time,
    t.start_time,
    t.start_year,
    t.start_month,
    t.start_day,
    t.start_hour,
    t.end_time,
    t.end_year,
    t.end_month,
    t.end_day,
    t.end_hour,
    ts.situation_type,
    ts.affected_direction,
    ts.number_of_lanes_restricted,
    ts.temporary_limit,
    ts.location_descriptor,
    ts.traffic_restriction_type,
    l.road_name,
    l.road_number,
    l.wgs84_line_coordinates,
    l.wgs84_point_coordinates,
    m.message_type,
    m.message_code,
    m.message,
    m.severity_text
FROM
    ts
LEFT JOIN
    l ON ts.location_key = l.location_id
LEFT JOIN
    m ON ts.message_key = m.message_id
LEFT JOIN
    t ON ts.time_key = t.time_id