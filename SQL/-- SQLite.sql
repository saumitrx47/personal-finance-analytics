-- SQLite
select count(distinct category) as unique_categories
from transactions;
select *
from transactions
where category = 'Food';