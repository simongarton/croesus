
-- investment_transaction : a record of transactions for my
-- investments. each is related back to the original investment
-- and will include the initial cost, plus any fees; plus what I get when I cash it out

CREATE TABLE investment_transaction (
    id            BIGSERIAL PRIMARY KEY,
    date          DATE   NOT NULL,
    investment_id BIGINT NOT NULL,
    value         MONEY -- NZ dollars
);

ALTER TABLE investment_transaction
    ADD CONSTRAINT investment_transaction_investment_fk FOREIGN KEY (investment_id) REFERENCES investment;
