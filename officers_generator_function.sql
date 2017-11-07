CREATE FUNCTION get_most() RETURNS VOID AS $$
    DECLARE
        id_count INTEGER;
        race_out TEXT;
        gender_out CHAR(1);
    BEGIN
        FOR row in SELECT * FROM fl_stops
        LOOP
            SELECT officer_id INTO id_in;
            IF id_in NOT IN (SELECT officer_id FROM officers)
            THEN
                SELECT count(*) INTO id_count FROM fl_stops WHERE officer_id = id_in;
                IF id_count = 1
                THEN 
                    SELECT officer_gender INTO gender_out FROM officers WHERE officer_id = id_in;
                    SELECT office_race INTO gender_out FROM officers WHERE officer_id = id_in;
                ELSE
                    FOR ROW IN SELECT * FROM fl_stops WHERE officer_id = id_in
                    LOOP
                        IF officer_gender != '' AND officer_gender IS NOT NULL
                        THEN
                            SELECT officer_gender INTO gender_out;
                        END IF;
                        IF officer_race != '' AND officer_race IS NOT NULL
                        THEN
                            SELECT officer_race INTO gender_out;
                        END IF;
                    END LOOP;
                END IF;
                INSERT INTO officers (officer_id, officer_gender, officer_race) VALUES (id_in, gender_out, race_out);
            END IF;
        END LOOP;
    END; $$
LANGUAGE 'plpgsql';