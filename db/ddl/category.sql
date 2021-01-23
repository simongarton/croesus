CREATE TABLE category (
    id           BIGSERIAL PRIMARY KEY,
    category     TEXT NOT NULL,
    sub_category TEXT,
    rules        TEXT NOT NULL
)