-- Business question 1: did listings shift to 30+ night minimums after Local Law 18?
-- This is a worked example. Write one mart like it for each of the other questions.

select
    snapshot_date,
    count(*) as listings,
    round(100.0 * avg(case when minimum_nights >= 30 then 1 else 0 end), 1)
        as pct_30_plus_nights
from {{ ref('stg_listings') }}
group by snapshot_date
order by snapshot_date
