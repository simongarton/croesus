CREATE TABLE "price_history" (
    id            BIGSERIAL PRIMARY KEY,
    date          date      NOT NULL,
    exchange      TEXT      NOT NULL,
    symbol        TEXT      NOT NULL,
    price         MONEY -- NZ dollars
);

ALTER TABLE "price_history"
    ADD CONSTRAINT price_history_unique UNIQUE (date, exchange, symbol);
