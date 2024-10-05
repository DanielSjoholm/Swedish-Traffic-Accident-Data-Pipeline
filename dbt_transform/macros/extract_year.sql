{% macro extract_year(column) %}
    extract(year from {{ column }})
{% endmacro %}