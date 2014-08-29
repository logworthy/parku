create table marker_sign_relationship as 
select streetmarker, sign, max(last_event)
from  marker_sign_series
group by streetmarker, sign
order by streetmarker
