ALTER TABLE sep_2015
DROP COLUMN Extra;

ALTER TABLE sep_2015
DROP COLUMN MTA_tax;

ALTER TABLE sep_2015
DROP COLUMN Tip_amount;

ALTER TABLE sep_2015
DROP COLUMN Tolls_amount;

ALTER TABLE sep_2015
DROP COLUMN Ehail_fee;

ALTER TABLE sep_2015
DROP COLUMN improvement_surcharge;

ALTER TABLE sep_2015
DROP COLUMN Total_amount;

ALTER TABLE sep_2015
DROP COLUMN Payment_type;

ALTER TABLE sep_2015
DROP COLUMN Trip_type;

ALTER TABLE proj.sep_2015
DROP COLUMN VendorID;
ALTER TABLE proj.sep_2015
DROP COLUMN Store_and_fwd_flag;
ALTER TABLE proj.sep_2015
DROP COLUMN RateCodeID;
ALTER TABLE proj.sep_2015
DROP COLUMN Fare_amount;
ALTER TABLE proj.sep_2015
DROP COLUMN resCol;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM proj.sep_2015
WHERE Trip_distance <= 0 OR Passenger_count > 2 OR Dropoff_longitude = 0 OR Passenger_count <= 0 OR Pickup_longitude = 0 OR lpep_pickup_datetime
 = Lpep_dropoff_datetime;


ALTER TABLE proj.sep_2015 ADD ID serial PRIMARY KEY;


ALTER TABLE proj.sep_2015
ADD Speed double;

UPDATE proj.sep_2015
SET Speed = (CAST(TIMESTAMPDIFF(second, lpep_pickup_datetime,Lpep_dropoff_datetime)  AS double) / Trip_distance);