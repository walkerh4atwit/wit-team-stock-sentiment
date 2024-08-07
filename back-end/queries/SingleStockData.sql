WITH TICKER_INFORMATION AS (
    SELECT
        *
    FROM
        ADMIN.TICKERS
    WHERE
        ID = :1
)
SELECT
    TICKER_INFORMATION.*,
    SECTORS.NAME
FROM
         TICKER_INFORMATION
    LEFT JOIN ADMIN.SECTORS ON TICKER_INFORMATION.SECTOR_ID = SECTORS.ID