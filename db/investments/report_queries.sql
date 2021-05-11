-- main query
select transaction.exchange, transaction.symbol, transaction.account, host, region, type, transaction.quantity, price.price, transaction.quantity * price.price as value
from transaction, price, region
where transaction.exchange = price.exchange
and transaction.symbol = price.symbol
and transaction.exchange = region.exchange
and transaction.symbol = region.symbol
order by transaction.exchange, transaction.symbol

-- account and host
select transaction.account, host, sum(transaction.quantity * price.price)as value
from transaction, price, region
where transaction.exchange = price.exchange
and transaction.symbol = price.symbol
and transaction.exchange = region.exchange
and transaction.symbol = region.symbol
group by account, host
order by account, host

-- account
select account, sum(transaction.quantity * price.price)as value
from transaction, price, region
where transaction.exchange = price.exchange
and transaction.symbol = price.symbol
and transaction.exchange = region.exchange
and transaction.symbol = region.symbol
group by account
order by account

-- region
select region, sum(transaction.quantity * price.price)as value
from transaction, price, region
where transaction.exchange = price.exchange
and transaction.symbol = price.symbol
and transaction.exchange = region.exchange
and transaction.symbol = region.symbol
group by region
order by region

-- account and region
select account, region, sum(transaction.quantity * price.price)as value
from transaction, price, region
where transaction.exchange = price.exchange
and transaction.symbol = price.symbol
and transaction.exchange = region.exchange
and transaction.symbol = region.symbol
group by account, region
order by account, region

-- hatch
select transaction.exchange, transaction.symbol, sum(transaction.quantity), sum(transaction.quantity * price.price) as value
from transaction, price, region
where transaction.exchange = price.exchange
and transaction.symbol = price.symbol
and transaction.exchange = region.exchange
and transaction.symbol = region.symbol
and account = 'simon'
and host = 'hatch'
group by transaction.exchange, transaction.symbol
order by transaction.exchange, transaction.symbol