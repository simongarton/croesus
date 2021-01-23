CREATE TABLE transaction (
    id               BIGSERIAL PRIMARY KEY,
    account_id       BIGINT NOT NULL,
    date             DATE   NOT NULL,
    amount           MONEY  NOT NULL,
    payee            TEXT,
    particulars      TEXT,
    code             TEXT,
    reference        TEXT,
    transaction_type TEXT,
    this_account     TEXT,
    other_account    TEXT,
    serial           TEXT,
    transaction_code TEXT,
    batch_number     TEXT,
    originating_bank TEXT,
    date_processed   DATE
);

