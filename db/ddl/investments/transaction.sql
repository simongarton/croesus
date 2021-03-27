CREATE TABLE "transaction" (
    id            BIGSERIAL PRIMARY KEY,
    date          DATE      NOT NULL,
    exchange      TEXT      NOT NULL,
    symbol        TEXT      NOT NULL,
    account       TEXT      NOT NULL,
    quantity      DOUBLE PRECISION NOT NULL,
    price         MONEY     NOT NULL -- NZ dollars
);

