WITH Count_Articles AS (
    SELECT
        COUNT(Articletickers.ticker_id) AS articlecount,
        Articletickers.ticker_id AS ticker_id
    FROM
        Articletickers
    GROUP BY
        Articletickers.ticker_id
    ORDER BY
        articlecount DESC
)

SELECT
    ticker,
    sentiment_score,
FROM
    Tickers JOIN Count_Articles ON
    Tickers.id = Count_Articles.ticker_id
WHERE
        ticker <> 'nan'
    AND sentiment_score IS NOT NULL
    AND sentiment_score <= 2
    AND sentiment_score >= 0
    AND article_count > 2
ORDER BY
    sentiment_score :ORDER
FETCH FIRST 6 ROWS ONLY