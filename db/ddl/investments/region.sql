CREATE TABLE "region" (
    id            BIGSERIAL PRIMARY KEY,
    exchange      TEXT      NOT NULL,
    symbol        TEXT      NOT NULL,
    region        TEXT      NOT NULL
);

ALTER TABLE "region"
    ADD CONSTRAINT region_unique UNIQUE (exchange, symbol);
