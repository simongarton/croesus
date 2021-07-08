CREATE TABLE "log" (
    id            BIGSERIAL     PRIMARY KEY,
    log_time      timestamp     NOT NULL,
    source        TEXT      NOT NULL,
    details       TEXT      NOT NULL,
    status_code   INTEGER   NOT NULL
);
