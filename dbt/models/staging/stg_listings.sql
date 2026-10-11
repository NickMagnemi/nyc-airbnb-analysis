-- One typed, cleaned row per listing per snapshot.
-- Personal fields (host names, profile text, review comments) are deliberately left out.

select
    try_cast(id as bigint) as listing_id,
    try_cast(host_id as bigint) as host_id,
    try_cast(snapshot_date as date) as snapshot_date,  -- the not_null test catches bad file names
    neighbourhood_group_cleansed as borough,
    neighbourhood_cleansed as neighbourhood,
    room_type,
    try_cast(replace(replace(price, '$', ''), ',', '') as decimal(10, 2)) as price_usd,
    try_cast(minimum_nights as integer) as minimum_nights
    -- TODO: add the other columns your business questions need, for example
    --       availability_365, number_of_reviews, review_scores_rating and
    --       host_is_superhost = 't' as host_is_superhost.
from {{ source('raw', 'raw_listings') }}
where try_cast(id as bigint) is not null
