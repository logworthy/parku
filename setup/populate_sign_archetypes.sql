insert into api_signarchetype (
  start_time,
  end_time,
  start_day_id,
  end_day_id,
  any_other_time,
  allow_permit_override,
  requires_pay_ticket,
  requires_pay_meter,
  requires_disability_permit,
  duration_mins,
  type_id,
  raw_sign_text
)
select 
  start_time,
  end_time,
  day_of_week_start,
  day_of_week_end,
  all_other_times,
  allow_permit_override,
  requires_pay_ticket,
  requires_pay_meter,
  requires_disability_permit,
  duration,
  case 
  	when sign_type = 'P' then 1
  	when sign_type = 'LZ' then 2
  	when sign_type = 'N' then 3
  	when sign_type = 'CW' then 4
  	when sign_type = 'PZ' then 5
  	when sign_type = 'U' then 6
  	end as type_id,
  sign
  from all_signs;

  insert into api_parkingbay (street_marker, geom)
    select distinct streetmarker, geom from parking_bays;

    insert into api_parkingevent (parking_bay_id, arrival_time, departure_time)
      select (select id from api_parkingbay where api_parkingbay.street_marker = parking_events.streetmarker),
      arrivaltime, departuretime
      from parking_events
      where (select id from api_parkingbay where api_parkingbay.street_marker = parking_events.streetmarker) is not null;