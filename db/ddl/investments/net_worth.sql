CREATE TABLE "net_worth" (
    id            BIGSERIAL PRIMARY KEY,
    date          DATE      NOT NULL,
    share_spend   MONEY     NOT NULL, -- NZ dollars
    share_value   MONEY     NOT NULL, -- NZ dollars
    share_gain_loss    MONEY     NOT NULL, -- NZ dollars
    share_percentage   DOUBLE PRECISION     NOT NULL,
    share_cagr         DOUBLE PRECISION     NOT NULL,
    other_value   MONEY     NOT NULL, -- NZ dollars
    total_value   MONEY     NOT NULL, -- NZ dollars
    four_percent  MONEY     NOT NULL, -- NZ dollars
    two_point_five_million    DOUBLE PRECISION     NOT NULL
);
