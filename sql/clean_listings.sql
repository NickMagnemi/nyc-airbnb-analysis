-- Turns raw_listings (all text, exactly as downloaded) into a typed, clean table.
-- This file is dataset-specific: it's where your knowledge of the data goes.
-- Personal fields (host names, profile text) are deliberately left out.

CREATE OR REPLACE TABLE listings AS
SELECT
    TRY_CAST(id AS BIGINT) AS listing_id,
    TRY_CAST(host_id AS BIGINT) AS host_id,
    CAST(snapshot_date AS DATE) AS snapshot_date,
    neighbourhood_group_cleansed AS borough,
    neighbourhood_cleansed AS neighbourhood,
    room_type,
    TRY_CAST(REPLACE(REPLACE(price, '$', ''), ',', '') AS DECIMAL(10, 2)) AS price_usd,
    TRY_CAST(minimum_nights AS INTEGER) AS minimum_nights
    -- TODO: add the other columns your business questions need, for example
    --       availability_365, number_of_reviews, review_scores_rating and
    --       host_is_superhost = 't' AS host_is_superhost.
FROM raw_listings
WHERE TRY_CAST(id AS BIGINT) IS NOT NULL;
