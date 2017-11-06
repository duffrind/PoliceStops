Original columns: id,state,stop_date,stop_time,location_raw,county_name,county_fips,fine_grained_location,police_department,driver_gender,driver_age_raw,driver_age,driver_race_raw,driver_race,violation_raw,violation,search_conducted,search_type_raw,search_type,contraband_found,stop_outcome,is_arrested,officer_id,officer_gender,officer_age,officer_race,officer_rank,out_of_state

cols to skip:
2 state
8 fine_grained_location (mostly empty)
9 police_department (empty)
11 driver_age_raw (dupe)
13 driver_race_raw (dupe)
15 violation_raw (dupe)
18 search_type_raw (dupe)
20 contraband_found (empty)

result:
id,state,stop_date,stop_time,location_raw,county_name,county_fips,driver_gender,driver_age,driver_race,violation,search_conducted,search_type,stop_outcome,is_arrested,officer_id,officer_gender,officer_age,officer_race,officer_rank,out_of_state

CREATE TEMP TABLE FL_stopsplus (
    id TEXT,
    state TEXT,
    stop_date DATE,
    stop_time TIME,
    location_raw TEXT,
    county_name  TEXT,
    county_fips INTEGER,
    fine_grained_location TEXT,
    police_department TEXT,
    driver_gender CHAR(1),
    driver_age_raw TEXT,
    driver_age FLOAT,
    driver_race_raw TEXT,
    driver_race TEXT,
    violation_raw TEXT,
    violation TEXT,
    search_conducted BOOL,
    search_type_raw TEXT,
    search_type TEXT,
    contraband_found TEXT,
    stop_outcome TEXT,
    is_arrested BOOL,
    officer_id TEXT,
    officer_gender CHAR(1),
    officer_age INT,
    officer_race TEXT,
    officer_rank TEXT,
    out_of_state BOOL
);

CREATE TABLE FL_stops AS (SELECT id,stop_date,stop_time,location_raw,county_name,county_fips,driver_gender,driver_age,driver_race,violation,search_conducted,search_type,stop_outcome,is_arrested,officer_id,officer_gender,officer_age,officer_race,officer_rank,out_of_state from FL_stopsplus);




\copy FL_stops (id,stop_date,stop_time,location_raw,county_name,county_fips,driver_gender,driver_age,driver_race,violation,search_conducted,search_type,stop_outcome,is_arrested,officer_id,officer_gender,officer_age,officer_race,officer_rank,out_of_state) FROM 'FL-clean.csv' DELIMITERS ',' CSV HEADER;

CREATE TABLE stops AS SELECT id stop_id, officer_id, officer_age, stop_date, stop_time, county_fips, violation, driver_gender, cast(driver_age AS INTEGER) driver_age, driver_race, search_conducted, search_type, stop_outcome, is_arrested, out_of_state FROM fl_stops;

CREATE TABLE officers AS SELECT DISTINCT officer_id, officer_gender, officer_race FROM fl_stops;

CREATE TABLE counties AS SELECT DISTINCT county_fips, county_name FROM fl_stops;

ALTER TABLE stops ADD PRIMARY KEY (stop_id);

ALTER TABLE officers ADD PRIMARY KEY (officer_id);
###This command threw an error because of duplicate officer_ids. After inspection, I noticed that:
##1) The maximum number of instances of any ID was 2
##2) all duplications were missing either race, gender or both from one entry, but included extra (but not always all) information in the second entry
##I decided to recreate the officers table with the assumption that the records containing empty columns were simply clerical mistakes and did not 
##represent separate officers from their more complete counterparts

DROP TABLE officers;
CREATE TABLE officers AS SELECT DISTINCT officer_id, max(officer_gender), max(officer_race) FROM fl_stops;
###This command didn't work because max can't be called twice in one select query. This may be best addressed with temp tables:
##A table of all officers with all non-null columns
##A table of all officers with missing gender whose id is not in the previous table
##A table of all officers with missing race whose id is not in either previous table
##A table of all offices with missing race and gender whose id is not in any previous table
##Finally union all these temp tables to get the officer table wherein every id in the table contains maximum information about the given officer
##Actually this would still run into issues if one entry has race but not gender and the other has gender but not race...
##Maybe try using cases, ala

SELECT DISTINCT officer_id CASE IF a.offer_gender != '' THEN a.officer_gender ELSE b.officer_gender END CASE...
