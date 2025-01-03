SELECT 
    name, sentiment_score
FROM 
    Sectors 
ORDER BY 
    sentiment_score :ORDER
FETCH FIRST 6 ROWS ONLY