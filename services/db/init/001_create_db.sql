-- 001_create_db.sql
-- Create initial databases for the pipeline.
-- Adjust OWNER, LC_COLLATE/LC_CTYPE, or remove DROP lines as needed.
-- This section targets PostgreSQL.

DROP DATABASE IF EXISTS postgres;

CREATE DATABASE ingestion
    WITH OWNER = pgadmin
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TEMPLATE = template0;

CREATE DATABASE curated
    WITH OWNER = pgadmin
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TEMPLATE = template0;