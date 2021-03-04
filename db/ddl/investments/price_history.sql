CREATE TABLE "price_history" (
    id            BIGSERIAL PRIMARY KEY,
    date          date      NOT NULL,
    exchange      TEXT      NOT NULL,
    symbol        TEXT      NOT NULL,
    price         MONEY -- NZ dollars
);

