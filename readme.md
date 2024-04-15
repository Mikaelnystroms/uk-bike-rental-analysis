








CREATE OR REPLACE TABLE `uk_bike_rentals.trips_data_partitioned`
PARTITION BY DATE(start_datetime)
AS
SELECT
    journey_id,
    start_datetime,
    start_station_id,
    start_station_name,
    end_datetime,
    end_station_id,
    end_station_name,
    bike_id,
    bike_model,
    duration_str,
    duration_ms,
    start_date,
    start_day,
    start_hour,
    end_day,
    end_hour
FROM
    `uk_bike_rentals.trips_data`;
