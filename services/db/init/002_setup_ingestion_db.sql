-- ==================================================
-- SCRAPER / INGESTION DATABASE SCHEMA
-- ==================================================
-- Database: ingestion (Scraper / ETL DB)
-- Purpose: Track samples through lifecycle (raw -> processed -> annotated -> ready)
-- ==================================================

CREATE TABLE IF NOT EXISTS samples_registry (
    id SERIAL PRIMARY KEY,
    sample_uid UUID NOT NULL,
    checkpoint TEXT NOT NULL,
    stage TEXT NOT NULL,
    create_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS samples_files (
    sample_uid UUID NOT NULL PRIMARY KEY,
    images TEXT[] NOT NULL,
    descriptions TEXT NOT NULL,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sample_labels (
    id SERIAL PRIMARY KEY,
);

CREATE TABLE IF NOT EXISTS checkpoints (
    checkpoint_id SERIAL PRIMARY KEY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    sample_count INT,
    notes TEXT
);




