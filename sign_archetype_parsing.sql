drop table all_signs;

create table all_signs as
select distinct sign from parking_events;

create table sign_base as
select * from all_signs;

alter table all_signs add column sign_type char(2);

update all_signs set sign_type =
case when sign in (select sign from
(
select sign,
(regexp_matches(sign,'((\dP)|(\d/\dP)|(P ?\d?\d)|(^P )|(P \(Parking\))|(P/ ?\d\d?))'))[1] as type
from sign_base
) a )  then 'P' 
when sign in (select sign from
(
select sign,
(regexp_matches(sign,'((LZ \d\dM)|(LZ ))'))[1] as type
from sign_base
) a )  then 'LZ' 
when sign in (select sign from
(
select sign,
(regexp_matches(sign,'((S/ No Stop)|(P/ ?\(No Parking\)))'))[1] as type
from sign_base
) a )  then 'N' 
when sign like '%CW%' then 'CW'
when sign like '%Permit Zone%' then 'PZ'
else 'U' end;

/*
select sign_type, count(*) from all_signs group by sign_type;
select * from all_signs where sign_type = 'U'
*/

alter table all_signs add column allow_permit_override boolean;
update all_signs set allow_permit_override =
case when sign like '%A%' or sign like '%RPA%' or sign like '%RPE%' then true else false end;

alter table all_signs add column requires_pay_ticket boolean;
update all_signs set requires_pay_ticket =
case when sign like '%TKT%' then true else false end;

alter table all_signs add column requires_pay_meter boolean;
update all_signs set requires_pay_meter =
case when sign like '%MTR%' then true else false end;

alter table all_signs add column requires_disability_permit boolean;
update all_signs set requires_disability_permit =
case when sign like '%DIS%' then true else false end;

alter table all_signs add column start_time time;
update all_signs set start_time =
(regexp_matches(replace(sign, '.', ':'),'(\d\d?:?\.?\d\d) ?- ?(\d\d?:?\.?\d\d)'))[1]::time;

alter table all_signs add column end_time time;
update all_signs set end_time =
(regexp_matches(replace(sign, '.', ':'),'(\d\d?:?\.?\d\d) ?- ?(\d\d?:?\.?\d\d)'))[2]::time;

alter table all_signs add column day_of_week_start integer;
alter table all_signs add column day_of_week_end integer;

-- M-S is dodgy!
with temp_table as (
select 
	sign,
	(regexp_matches(sign,'((M-F)|(M-SAT)|(M-SUN)|(M-THU)|(Mon - Sat)|(S-S)|(M-Sun)|(Sun-Sun)|(AOT)|(Sat)|(SAT)|(SUN)|(Fri)|(THU)|(M-S))'))[1] as day_of_week
from all_signs
),
temp_table2 as (
select sign, (regexp_matches(day_of_week,'(.*)-?(.*)'))[1] as day_of_week_start,
(regexp_matches(day_of_week,'(.*)-?(.*)'))[2] as day_of_week_end
from temp_table
)
, temp_table3 as (
select 
sign,
case when day_of_week_start in ('M', 'Mon', 'Mon ') then 0
when day_of_week_start in ('Tue') then 1
when day_of_week_start in ('Wed') then 2
when day_of_week_start in ('Thu') then 3
when day_of_week_start in ('Fri') then 4
when day_of_week_start in ('Sat', 'SAT') then 5
when day_of_week_start in ('Sun') then 6
when day_of_week_start = 'S' and day_of_week_end = 'S' then 5
else 999 end as day_of_week_start,
case when day_of_week_end in ('M', 'Mon', 'Mon ') then 0
when day_of_week_end in ('Tue') then 1
when day_of_week_end in ('Wed') then 2
when day_of_week_end in ('Thu', 'THU') then 3
when day_of_week_end in ('Fri','F') then 4
when day_of_week_end in ('Sat', 'SAT', ' Sat') then 5
when day_of_week_end in ('Sun', 'SUN') then 6
when day_of_week_start = 'S' and day_of_week_end = 'S' then 5
else 999 end as day_of_week_end
from temp_table2
)
update all_signs as a set day_of_week_start = b.day_of_week_start , day_of_week_end = b.day_of_week_end
from temp_table3 as b
where a.sign=b.sign;

select * from all_signs where day_of_week_start is null or day_of_week_end is null;

update all_signs 
set day_of_week_start = 0,
day_of_week_end = 6
where day_of_week_start is null and day_of_week_end is null;