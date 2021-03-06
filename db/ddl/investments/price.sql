CREATE TABLE "price" (
    id            BIGSERIAL PRIMARY KEY,
    exchange      TEXT      NOT NULL,
    symbol        TEXT      NOT NULL,
    price         MONEY     NOT NULL -- NZ dollars
);

ALTER TABLE "price"
    ADD CONSTRAINT price_unique UNIQUE (exchange, symbol);
