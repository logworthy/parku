drop table all_signs;

create table all_signs as
select distinct sign from parking_events;

 -- We make a copy of the sign data, because we are unable to update
 -- the all_signs table while performing a subquery on it.

create table sign_base as
select * from all_signs;


 -- First order of business, try and figure out what type of sign it is.
 -- This could be:
 --  * "P" for "Parking"
 --  * "LZ" for "Loading Zone"
 --  * "CW" for "Clear Way"
 --  * "PZ" for "Permit Zone" or
 --  * "U" for "Unknown"

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

 -- Almighty regex to figure oeut the start day and end day that a particular rule applies. 
 -- See the first regex to get an idea for the types of formats that require parsing in the 
 -- original dataset, and the rest of the query is taking the captured groups from that regex
 -- and transforming them into integers between 0 and 6 representing the day of the week.
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
  ),
  temp_table3 as (
    select 
      sign,
      case
        when day_of_week_start in ('M', 'Mon', 'Mon ') then 0
        when day_of_week_start in ('Tue') then 1
        when day_of_week_start in ('Wed') then 2
        when day_of_week_start in ('Thu') then 3
        when day_of_week_start in ('Fri') then 4
        when day_of_week_start in ('Sat', 'SAT') then 5
        when day_of_week_start in ('Sun') then 6
        when day_of_week_start = 'S' and day_of_week_end = 'S' then 5
      end as day_of_week_start,
      case 
        when day_of_week_end in ('M', 'Mon', 'Mon ') then 0 
        when day_of_week_end in ('Tue') then 1
        when day_of_week_end in ('Wed') then 2
        when day_of_week_end in ('Thu', 'THU') then 3
        when day_of_week_end in ('Fri','F') then 4
        when day_of_week_end in ('Sat', 'SAT', ' Sat') then 5
        when day_of_week_end in ('Sun', 'SUN') then 6
        when day_of_week_start = 'S' and day_of_week_end = 'S' then 5
      end as day_of_week_end
    from temp_table2
  )
  update all_signs as a set day_of_week_start = b.day_of_week_start , day_of_week_end = b.day_of_week_end
  from temp_table3 as b
  where a.sign=b.sign;

select * from all_signs where day_of_week_start is null or day_of_week_end is null

 -- For the records which didn't get anything useful out of the monster query above,
 -- we set them to apply for the entire week. This is a guess, but the best guess we
 -- think we can make about them, without having to discard them.

update all_signs 
set day_of_week_start = 0,
day_of_week_end = 6
where day_of_week_start is null and day_of_week_end is null;


 -- Each sign archetype applies for a certain amount of time. 
 -- This query extracts the various types of durations one could
 -- expect, and stores them as an integer representing number of
 -- minutes.

alter table all_signs add column duration integer;

with temp_table as (
  select sign,
  (regexp_matches(sign,'((\dP)|(\d/\dP)|(P ?\d?\d)|(^P )|(LZ  ?\d\dM)|(S/ No Stop)|(P \(Parking\))|(P/ ?\d\d?)|(P/ ?\(No Parking\))|(Temp Sign Plate)|(\d/\d))'))[1] as sign_type
  from all_signs)
  , temp_table2 as (
    select sign, sign_type,
      case 
       when sign_type = '2P' then 120
       when sign_type = '1P' then 60
       when sign_type = '3P' then 180
       when sign_type = '4P' then 240
       when sign_type = '1/2P' then 30
       when sign_type = 'LZ 15M' then 15
       when sign_type = 'LZ 30M' then 30
       when sign_type = 'P/ 10' then 30
       when sign_type = 'P 5' then 5
       when sign_type = 'P10' then 10
       when sign_type = '1/4P' then 15
       when sign_type = 'LZ  15M' then 15
       when sign_type = 'P15' then 15
       when sign_type = 'P/ 15' then 15
       when sign_type = 'P/15' then 15
       when sign_type = 'P/ 5' then 5
       when sign_type = 'P5' then 5
       when sign_type = '1/2' then 30
       else 0 end as duration
    from temp_table
  )
   update all_signs as a set duration = b.duration
   from temp_table2 as b
   where a.sign=b.sign;

update all_signs set duration = 0
where duration is null;

select * from all_signs;
