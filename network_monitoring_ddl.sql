CREATE DATABASE network_monitoring;
CREATE USER <user> WITH PASSWORD <'password'>;
GRANT ALL PRIVILEGES ON DATABASE network_monitoring TO <user>;
GRANT INSERT, SELECT ON TABLE daily_usage TO <user>;
GRANT USAGE, SELECT ON SEQUENCE daily_usage_id_seq TO <user>;


CREATE TABLE IF NOT EXISTS daily_usage
(
    id          serial PRIMARY KEY,
    timestamp   timestamp NOT NULL,
    download_mb real      NOT NULL,
    upload_mb   real      NOT NULL
);