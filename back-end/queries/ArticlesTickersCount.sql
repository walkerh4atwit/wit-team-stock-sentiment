WITH COUNT_ARTICLES AS (
    SELECT
        COUNT(ARTICLETICKERS.TICKER_ID) AS ARTICLECOUNT,
        ARTICLETICKERS.TICKER_ID
    FROM
        ARTICLETICKERS
    GROUP BY
        ARTICLETICKERS.TICKER_ID
    ORDER BY
        ARTICLECOUNT DESC
)
SELECT
    ID,
    TICKER,
    COMPANY_NAME,
    ARTICLECOUNT
FROM
         TICKERS
    INNER JOIN COUNT_ARTICLES ON TICKERS.ID = COUNT_ARTICLES.TICKER_ID
WHERE
    TICKER <> 'nan'
ORDER BY
    ARTICLECOUNT DESC