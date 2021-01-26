CREATE TABLE investment (
    id        BIGSERIAL PRIMARY KEY,
    date      DATE NOT NULL,
    name      TEXT NOT NULL,
    type      TEXT NOT NULL,
    exchange  TEXT,
    code      TEXT,
    details   TEXT,
    value     MONEY, -- NZ dollars
    date_sold DATE
)
