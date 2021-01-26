
-- investment_value : a snapshot of the value of this investment on
-- a given day. ideally all investments will get a value on the same
-- day, otherwise I'll have to look for the previous value

CREATE TABLE investment_value (
    id            BIGSERIAL PRIMARY KEY,
    date          DATE   NOT NULL,
    investment_id BIGINT NOT NULL,
    value         MONEY -- NZ dollars
);

ALTER TABLE investment_value
    ADD CONSTRAINT investment_value_investment_fk FOREIGN KEY (investment_id) REFERENCES investment;
