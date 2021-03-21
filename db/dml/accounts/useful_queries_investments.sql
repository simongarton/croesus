select
	date,
	sum(quantity * price) as total
from
	"transaction" t
group by
	"date"
order by
	date;

Ï

select exchange, symbol, min(date) from "transaction" t  where exchange  = 'NZX' group by exchange, symbol ;

INSERT INTO transaction (date, exchange, symbol, quantity, price) VALUES ('2021-01-25', 'NZX','NZG', 694.927032, 2.878);
INSERT INTO transaction (date, exchange, symbol, quantity, price) VALUES ('2021-01-25', 'NZX','TWF', 736.279808, 2.709);

select date, sum(value) from value v group by date order by date;

insert into total_value (date, value)

select * from price;
select * from price_history where exchange = 'nzx' order by date, symbol ;

select * from total_value order by date;

select * from value where date = '2021-02-08';