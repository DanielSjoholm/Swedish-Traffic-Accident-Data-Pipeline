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
    road_number_numeric,
    road_name,
    geometry__point__sweref99_tm AS geometry_point_sweref99_tm,
    geometry__point__wgs84 AS geometry_point_wgs84,
    geometry__line__sweref99_tm AS geometry_line_sweref99_tm,
    geometry__line__wgs84 AS geometry_line_wgs84

FROM stg_traffic