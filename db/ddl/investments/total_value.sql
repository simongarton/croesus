CREATE TABLE "total_value" (
    id            BIGSERIAL PRIMARY KEY,
    date          date      NOT NULL,
    value         MONEY     NOT NULL -- NZ dollars
);

ALTER TABLE "total_value"
    ADD CONSTRAINT total_value_unique UNIQUE (date);
