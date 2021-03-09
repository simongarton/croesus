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