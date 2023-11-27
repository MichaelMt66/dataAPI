
with sq1 as (
	select d.id, d.department, date_part('year', TO_TIMESTAMP(he.datetime,'YYYY-MM-DDTHH24:MI:SSZ') ) as year
	from hired_employees he
	join departments d
	on he.department_id = d.id
	where he.datetime <> ''
),
sq2 as (
	select year, count(*) / count(distinct(department) )  as average
	from sq1
	group by year
	having year = 2021
)

select id, department, count(*)
from sq1
group by id, department
having count(*) > (select average from sq2)
order by 3 desc
