CREATE TABLE "value" (
    id            BIGSERIAL PRIMARY KEY,
    date          date      NOT NULL,
    exchange      TEXT      NOT NULL,
    symbol        TEXT      NOT NULL,
    price         MONEY     NOT NULL, -- NZ dollars
    value         MONEY     NOT NULL -- NZ dollars
);

ALTER TABLE "value"
    ADD CONSTRAINT value_unique UNIQUE (date, exchange, symbol);
