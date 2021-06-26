CREATE TABLE "other_asset" (
    id            BIGSERIAL PRIMARY KEY,
    date          DATE      NOT NULL,
    account       TEXT      NOT NULL,
    asset         TEXT      NOT NULL,
    value         MONEY     NOT NULL, -- NZ dollars
    details       TEXT
);

