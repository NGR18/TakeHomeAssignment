#Report2
WITH CTE4 AS(
WITH CTE3 as(
WITH CTE1 as(
select distinct date(a.local_created_at) as recorddate, b.item_name as item, dailyweather.dailytemp as temp
from morse a
cross join morse b
left join dailyweather
on date(a.local_created_at)=dailyweather.recordtime),
CTE2 AS(
select date(local_created_at) as recorddate, item_name as item, 
sum(if(net_quantity=-1,0,net_quantity)) as sales
from morse
group by recorddate, item_name)
select CTE1.recorddate, CTE1.item, ifnull(CTE2.sales,0) as sales, CTE1.temp
from CTE1
left join 
CTE2
on CTE1.recorddate=CTE2.recorddate and CTE1.item=CTE2.item)
select next_sales.recorddate, next_sales.item,
(next_sales.sales-now_sales.sales) as salesdiff, 
CASE WHEN (next_sales.TEMP-now_sales.TEMP) >=2 THEN "warmer"
	 WHEN (next_sales.TEMP-now_sales.TEMP) <=-2 THEN "colder" END tempdiff
from CTE3 now_sales, CTE3 next_sales
where now_sales.recorddate=next_sales.recorddate-1 and now_sales.item=next_sales.item)
select cte4.item, 
avg(case when cte4.tempdiff="warmer" then cte4.salesdiff else null end) "Avg change in sales when warmer",
avg(case when cte4.tempdiff="colder" then cte4.salesdiff else null end) "Avg change in sales when colder"
from cte4
group by cte4.item;
