-- Verificar si la tabla existe y eliminarla si es así
DROP TABLE IF EXISTS isabido86_coderhouse.weather_data_final;

-- Crear la tabla con el campo ID autogenerado y ingest_timestamp para llevar el control
CREATE TABLE isabido86_coderhouse.weather_data_final (
    id INTEGER IDENTITY(1,1) PRIMARY KEY,
    id_estado INTEGER,
    id_municipio INTEGER,
    cve_inegi VARCHAR(255),
    municipio VARCHAR(255),
    estado VARCHAR(255),
    country VARCHAR(255),
    lat FLOAT,
    lon FLOAT,
    tz_id VARCHAR(255),
    localtime_epoch BIGINT,
    local_time TIMESTAMP,
    ingest_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_last_updated_epoch BIGINT,
    current_last_updated TIMESTAMP,
    temperatura FLOAT,
    current_temp_f FLOAT,
    current_is_day INTEGER,
    current_condition_text VARCHAR(255),
    humedad INTEGER,
    viento_kph FLOAT,
    current_wind_degree INTEGER,
    current_wind_dir VARCHAR(10)
);

ALTER TABLE isabido86_coderhouse.weather_data_final 
ADD CONSTRAINT unique_municipio_estado_localtime UNIQUE (municipio, estado, current_last_updated_epoch);