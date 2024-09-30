CREATE DATABASE TRAFFIC_ANALYTICS_DB;

CREATE SCHEMA IF NOT EXISTS staging;

SELECT schema_name
FROM information_schema.schemata;

GRANT USAGE ON SCHEMA staging TO postgres;