-- #1 how many transactions do I have ?
select
	count(*)
from
	"transaction" t;

-- #1 break down transactions by account annd show dates and counts
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

-- #3 list categories
select * from category c order by category, sub_category ;


-- #4 show unallocated transactions
select
	id, date, amount, payee, particulars, code, reference, category, sub_category 
from
	"transaction" t
where
	category is null
order by date desc ;

-- #5 add a category 
insert into public.category
(category, sub_category, rules)
values('Insurance', 'State', '{"column":"payee","operation":"contains","value":"State Insurance"}');

-- #6 categories by week
select date, date_trunc('week', date)::date as week_beginning, category, sub_category, count(*) as transactions, sum(amount)::numeric::float8
from "transaction" t
group by date, week_beginning, category, sub_category
order by date, week_beginning, category, sub_category;

-- #7 categories by month
select date, date_trunc('month', date)::date as month_beginning, category, sub_category, count(*) as transactions, sum(amount)::numeric::float8
from "transaction" t
group by date, month_beginning, category, sub_category 
order by date, month_beginning, category, sub_category ;

--#8 categories used
select  category, sub_category, count(*) as transactions, sum(amount)::numeric as total from "transaction" t
group by category, sub_category
order by category, sub_category;

--#9 category rules
select  category, sub_category, count(*) as rules from category c
group by category, sub_category
order by category, sub_category;


-- #10 categories by week for 2021 (spreadsheet query)
select date, date_trunc('week', date)::date as week_beginning, category, sub_category, count(*) as transactions, sum(amount)::numeric::float8
from "transaction" t
where date >= '2020-01-01'
and date <= '2020-12-31'
group by date, week_beginning, category, sub_category
order by date, week_beginning, category, sub_category;



-- #11 last months transactions
select 	id, date, amount, payee, particulars, code, reference, category, sub_category
from "transaction" t
where date >= '2021-03-01'
and date <= '2021-03-31'

select * from "transaction" t2  where date = '2021-01-25' and category != 'Transfer';

select * from "transaction" t where category  = 'Simon' and sub_category = 'Pets';

select * from "transaction" t where sub_category = 'Eatoing';

select * from category c where rules like '%haresies%';
select * from category c where rules like '%atch%';

select * from category c where category = 'Insurance';

select * from "transaction" t 
where category  = 'Insurance';

update "transaction" 
set category  = null, sub_category = null where category  = 'Insurance';


create table temp_weekly_summary as (
select date_trunc('week', date)::date as week_beginning, category, sub_category, count(*) as transactions, sum(amount)::numeric::float8
from "transaction" t
group by week_beginning, category, sub_category
order by week_beginning, category, sub_category);

select * from temp_weekly_summary;

select * from "transaction" t  where account_id = 3 and transaction_type  = 'C' order by date desc;

update "transaction" t set amount = -amount::numeric where account_id = 3 and transaction_type  = 'C' and amount::numeric  < 0;

insert into transaction (account_id, date, amount, payee, category, sub_category) values (4, '2021-03-19', 2665, 'Central Trails', 'Holiday','Rail Trail');
insert into transaction (account_id, date, amount, payee, category, sub_category) values (4, '2021-04-01', 10000, 'Hatch', 'Shares','Hatch');
insert into transaction (account_id, date, amount, payee, category, sub_category) values (4, '2020-12-31', 1000, 'Hatch', 'Shares','Hatch');
insert into transaction (account_id, date, amount, payee, category, sub_category) values (4, '2020-12-31', 1000, 'Sharesies', 'Shares','Hatch');
insert into transaction (account_id, date, amount, payee, category, sub_category) values (4, '2021-01-26', 2000, 'Sharesies', 'Shares','Sharesies');
insert into transaction (account_id, date, amount, payee, category, sub_category) values (4, '2021-01-24', 8000, 'Sharesies', 'Shares','Sharesies');
insert into transaction (account_id, date, amount, payee, category, sub_category) values (4, '2021-01-13', 1000, 'Jardin', 'Shares','Jardin');
insert into transaction (account_id, date, amount, payee, category, sub_category) values (4, '2020-12-23', 70.68, 'GSI Direct', 'Work','Insurance');