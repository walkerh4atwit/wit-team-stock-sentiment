SELECT
    :3,
    SENTIMENT_SCORE
FROM
    ADMIN.:2
WHERE
        :3 <> 'nan'
    AND SENTIMENT_SCORE IS NOT NULL
    AND SENTIMENT_SCORE <= 4
    AND SENTIMENT_SCORE >= 0
ORDER BY
    SENTIMENT_SCORE :1
FETCH FIRST 6 ROWS ONLY