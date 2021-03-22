# Lambdas

## croesus

Does very little, just a message for the root of the API.

```
GET /
```

## exchange-rate

Uses an **external API** (exchangerate-api.com) to get exchange rates and store them in the **database**. GET always goes to the DB, POST will update for the current day.

```
GET /exchange-rate/{source}/{target}/{date}
POST /exchange-rate/{source}/{target}
```

DB reads and writes (exchange-rate); secrets;

## history

Returns historical values from the DB (2 value tables).

```
GET /history
GET /history/{exchange}
GET /history/{exchange}/{symbol}
```

DB reads (value, total_value)

## holdings

Returns individual holdings (not grouped) from the transactions table.

```
GET /holdings
GET /holdings/{exchange}
GET /holdings/{exchange}/{symbol}
```

DB reads (transaction)

## major_domo

The scheduled job.

TBC

## spending

Sums up spending in different ways from the transactions table.

```
GET /holdings
GET /holdings/{exchange}
GET /holdings/{exchange}/{symbol}
```

DB reads (transaction)

## stocks

```
GET /stocks/{exchange}
GET /stocks/{exchange}/{symbol}/{date}
POST /stocks/{exchange}/{symbol}/{date}
```

Secrets.

## transactions

Add and get transactions.

```
GET /transactions
GET /transactions/{exchange}
GET /transactions/{exchange}/{symbol}
POST /transactions/{exchange}/{symbol}
```

DB reads and writes (transaction)

## value

Calls holdings, stocks and spending.

```
GET /value
GET /value/{exchange}
GET /value/{exchange}/{symbol}
```

Self-API;
