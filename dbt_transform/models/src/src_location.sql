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
    road_number_numeric AS road_number,
    road_name,
    geometry__point__sweref99_tm AS sweref99_tm_point_coordinates,
    geometry__point__wgs84 AS wgs84_point_coordinates,
    geometry__line__sweref99_tm AS sweref99_tm_line_coordinates,
    geometry__line__wgs84 AS wgs84_line_coordinates

FROM stg_traffic