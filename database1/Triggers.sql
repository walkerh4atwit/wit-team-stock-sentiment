-- Create Temporary Tables
CREATE GLOBAL TEMPORARY TABLE temp_ticker_ids (
    ticker_id NUMBER
) ON COMMIT DELETE ROWS;

CREATE GLOBAL TEMPORARY TABLE temp_sector_ids (
    sector_id NUMBER
) ON COMMIT DELETE ROWS;

-- Row-Level Trigger for Changes to ArticleTickers Table
CREATE OR REPLACE TRIGGER row_level_update_ticker_sentiment
AFTER INSERT OR UPDATE OR DELETE ON ArticleTickers
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO temp_ticker_ids (ticker_id) VALUES (:NEW.ticker_id);
    ELSIF UPDATING THEN
        INSERT INTO temp_ticker_ids (ticker_id) VALUES (:NEW.ticker_id);
        INSERT INTO temp_ticker_ids (ticker_id) VALUES (:OLD.ticker_id);
    ELSIF DELETING THEN
        INSERT INTO temp_ticker_ids (ticker_id) VALUES (:OLD.ticker_id);
    END IF;
END;
/

-- Statement-Level Trigger for Changes to ArticleTickers Table
CREATE OR REPLACE TRIGGER statement_level_update_ticker_sentiment
AFTER INSERT OR UPDATE OR DELETE ON ArticleTickers
DECLARE
    CURSOR c_tickers IS
        SELECT DISTINCT ticker_id FROM temp_ticker_ids;
    avg_sentiment FLOAT;
    sector_id NUMBER;
BEGIN
    FOR r IN c_tickers LOOP
        -- Calculate the new running average sentiment score for the specific ticker_id
        SELECT AVG(sentiment_score), sector_id INTO avg_sentiment, sector_id
        FROM ArticleTickers
        WHERE ticker_id = r.ticker_id
        GROUP BY sector_id;

        -- Update the sentiment_score in the Tickers table
        UPDATE Tickers
        SET sentiment_score = avg_sentiment
        WHERE id = r.ticker_id;

        -- Insert affected sector_id into temp_sector_ids
        INSERT INTO temp_sector_ids (sector_id) VALUES (sector_id);
    END LOOP;
END;
/

-- Row-Level Trigger for Changes in Tickers Table to Update Sectors Table
CREATE OR REPLACE TRIGGER row_level_update_sector_sentiment
AFTER INSERT OR UPDATE OR DELETE ON Tickers
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO temp_sector_ids (sector_id) VALUES (:NEW.sector_id);
    ELSIF UPDATING THEN
        INSERT INTO temp_sector_ids (sector_id) VALUES (:NEW.sector_id);
        INSERT INTO temp_sector_ids (sector_id) VALUES (:OLD.sector_id);
    ELSIF DELETING THEN
        INSERT INTO temp_sector_ids (sector_id) VALUES (:OLD.sector_id);
    END IF;
END;
/

-- Statement-Level Trigger for Changes in Tickers Table to Update Sectors Table
CREATE OR REPLACE TRIGGER statement_level_update_sector_sentiment
AFTER INSERT OR UPDATE OR DELETE ON Tickers
DECLARE
    CURSOR c_sectors IS
        SELECT DISTINCT sector_id FROM temp_sector_ids;
    avg_sentiment FLOAT;
BEGIN
    FOR r IN c_sectors LOOP
        -- Calculate the new running average sentiment score for the specific sector_id
        SELECT AVG(sentiment_score) INTO avg_sentiment
        FROM Tickers
        WHERE sector_id = r.sector_id;

        -- Update the sentiment_score in the Sectors table
        UPDATE Sectors
        SET sentiment_score = avg_sentiment
        WHERE id = r.sector_id;
    END LOOP;
END;
/
