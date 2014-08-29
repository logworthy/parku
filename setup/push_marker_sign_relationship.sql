
insert into api_parkingbaysignarchetyperelationship (parking_bay_id, sign_archetype_id, last_seen)
select 
bay.id,
sgn.id,
max
from 
marker_sign_relationship msr,
api_parkingbay bay,
api_signarchetype sgn
where
msr.streetmarker = bay.street_marker
and msr.sign = sgn.raw_sign_text;