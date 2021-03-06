CREATE TABLE "price" (
    id            BIGSERIAL PRIMARY KEY,
    exchange      TEXT      NOT NULL,
    symbol        TEXT      NOT NULL,
    price         MONEY -- NZ dollars
);

ALTER TABLE "price"
    ADD CONSTRAINT price_unique UNIQUE (exchange, symbol);
