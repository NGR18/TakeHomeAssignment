with cte2 as(
with cte1 as (
select hourlytemp,item_name,sum(if(net_quantity=-1,0,net_quantity)) as number_sold
from morse
left join hourlyweather
on date(morse.local_created_at)=(hourlyweather.recorddate) 
and time(morse.local_created_at) between time(hourlyweather.starttime) 
and time(hourlyweather.endtime)
group by hourlytemp,item_name
order by hourlytemp,number_sold desc)
SELECT *, DENSE_RANK() OVER (PARTITION BY hourlytemp ORDER BY number_sold DESC) AS numbrank
FROM CTE1)
select hourlytemp, item_name as item, number_sold
from cte2
where numbrank=1;