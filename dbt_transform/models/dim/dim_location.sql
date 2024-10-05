{{
  config(
    materialized = 'view',
  )
}}

with src_location as (
    SELECT
        *
    FROM {{ ref('src_location') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['id']) }} AS location_id,
    road_number_numeric,
    road_name,
    geometry_point_sweref99_tm,
    geometry_point_wgs84,
    geometry_line_sweref99_tm,
    geometry_line_wgs84
FROM src_location