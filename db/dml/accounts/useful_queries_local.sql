-- sum up transactions by category

select
	name,
	min(date) as earliest,
	max(date) as latest,
	count(*) as transactions,
	sum(amount) as total
from
	transaction
inner join account on
	transaction.account_id = account.id
group by
	name;


-- find transactions without categories

select
	id,
	date,
	amount,
	payee,
	particulars,
	code,
	reference,
	category ,
	sub_category
from
	"transaction" t
where
	account_id = 3
	and category is null
order by
	date desc;

-- delete all transactions

delete
from
	"transaction" ;

select
	*
from
	category c ;

-- show rule count for a category

select
	category,
	sub_category,
	count(*)
from
	category c
group by
	category,
	sub_category
order by
	category,
	sub_category;

-- generic query to add a category rule

insert
	into
	public.category (category,
	sub_category,
	rules)
values('Simon',
'Petrol',
'{"column":"payee","operation":"contains","value":"MOBIL "}');


-- show categories, usage and value

select
	category,
	sub_category,
	count(*),
	sum(amount)
from
	"transaction" t
group by
	category,
	sub_category
order by
	sum(amount) desc;

-- find specific transactions matching a category

select
	*
from
	"transaction" t
where
	category = 'Transfer'
	and sub_category = 'Supermarket';
