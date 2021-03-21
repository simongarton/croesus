CREATE TABLE "exchange-rate" (
    id            BIGSERIAL PRIMARY KEY,
    date          DATE      NOT NULL,
    source        TEXT      NOT NULL,
    target        TEXT      NOT NULL,
    rate          DOUBLE PRECISION     NOT NULL
);

ALTER TABLE "exchange-rate"
    ADD CONSTRAINT exchange-rate-unique UNIQUE (date, source, target);