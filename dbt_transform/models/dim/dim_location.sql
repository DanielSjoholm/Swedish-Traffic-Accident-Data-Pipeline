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
    {{capitalize_first_letter("COALESCE(road_name, 'ej specificerat')")}} AS road_name,
    COALESCE(road_number, -1) AS road_number,
    COALESCE(wgs84_line_coordinates, 'Ej specificerat') AS wgs84_line_coordinates,
    COALESCE(wgs84_point_coordinates, 'Ej specificerat') AS wgs84_point_coordinates,
    COALESCE(sweref99_tm_line_coordinates, 'Ej specificerat') AS sweref99_tm_line_coordinates,
    COALESCE(sweref99_tm_point_coordinates, 'Ej specificerat') AS sweref99_tm_point_coordinates
FROM src_location