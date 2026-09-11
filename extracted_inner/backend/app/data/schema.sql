-- =====================================================================
-- India AQI–Weather Tracker — Database Schema
-- =====================================================================
-- 5 tables: districts, stations, daily_readings, district_rollups, sources
-- Compatible with both PostgreSQL/Timescale and SQLite.
-- The hypertable line is handled in Python (db.py) — it only runs on
-- PostgreSQL with the timescaledb extension.
-- =====================================================================

-- ---------------------------------------------------------------------
-- districts: every administrative district in India (LGD-coded)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS districts (
    district_id    TEXT PRIMARY KEY,
    lgd_code       TEXT UNIQUE,
    name           TEXT NOT NULL,
    state          TEXT NOT NULL,
    latitude       FLOAT,
    longitude      FLOAT
);

-- ---------------------------------------------------------------------
-- stations: CPCB / IMD monitoring stations
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS stations (
    station_id     TEXT PRIMARY KEY,
    station_name   TEXT,
    district_id    TEXT REFERENCES districts(district_id),
    latitude       FLOAT,
    longitude      FLOAT,
    source         TEXT NOT NULL,
    is_active      BOOLEAN DEFAULT TRUE
);

-- ---------------------------------------------------------------------
-- daily_readings: Contract A rows (one per station per day)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS daily_readings (
    station_id     TEXT REFERENCES stations(station_id),
    date           DATE NOT NULL,
    aqi            FLOAT,
    pm2_5          FLOAT,
    pm10           FLOAT,
    no2            FLOAT,
    temperature    FLOAT,
    rainfall_mm    FLOAT,
    wind_speed_kmh FLOAT,
    data_type      TEXT DEFAULT 'observed',
    source         TEXT NOT NULL,
    fetched_at     TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (station_id, date)
);

-- ---------------------------------------------------------------------
-- district_rollups: Contract B rows (one per district per day)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS district_rollups (
    district_id    TEXT REFERENCES districts(district_id),
    date           DATE,
    avg_aqi        FLOAT,
    max_aqi        FLOAT,
    avg_temp       FLOAT,
    avg_rainfall   FLOAT,
    avg_wind       FLOAT,
    season         TEXT,
    station_count  INT DEFAULT 0,
    coverage_type  TEXT,
    PRIMARY KEY (district_id, date)
);

-- ---------------------------------------------------------------------
-- sources: metadata about data providers (CPCB, Open-Meteo, etc.)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sources (
    source_name    TEXT PRIMARY KEY,
    source_url     TEXT,
    license_note   TEXT,
    last_synced_at TIMESTAMPTZ
);
