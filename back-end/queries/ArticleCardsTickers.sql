SELECT title, url
FROM 
    (SELECT article_id 
    FROM ArticleTickers 
    WHERE sentiment_score = :1
    AND ticker_id = :2) scored_arttic 
JOIN Articles
ON scored_arttic.article_id = Articles.id
ORDER BY date_published DESC
FETCH FIRST 3 ROWS ONLY