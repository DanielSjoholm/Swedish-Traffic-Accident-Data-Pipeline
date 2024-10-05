{% macro format_date(column) %}
    to_char({{ column }}, 'YYYY-MM-DD HH24:MI')
{% endmacro %}