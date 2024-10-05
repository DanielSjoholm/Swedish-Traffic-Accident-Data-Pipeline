{% macro trim_spaces(column) %}
    case
        when {{ column }} is null then null
        else trim(both ' ' from {{ column }})
    end
{% endmacro %}