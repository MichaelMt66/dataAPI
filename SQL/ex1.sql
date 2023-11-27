
with sq as (
	select d.department , j.job ,  date_part('quarter', TO_TIMESTAMP(he.datetime,'YYYY-MM-DDTHH24:MI:SSZ') ) as quarter
	from hired_employees he
	join departments d
	on he.department_id = d.id
	join jobs j
	on he.job_id = j.id
	where date_part('year', TO_TIMESTAMP(he.datetime,'YYYY-MM-DDTHH24:MI:SSZ') ) = 2021
)

select department, job,
COUNT(CASE WHEN quarter = 1 THEN 1 END) AS "Q1",
COUNT(CASE WHEN quarter = 2 THEN 1 END) AS "Q2",
COUNT(CASE WHEN quarter = 3 THEN 1 END) AS "Q3",
COUNT(CASE WHEN quarter = 4 THEN 1 END) AS "Q4"
from sq
group by department,job
order by 1,2

