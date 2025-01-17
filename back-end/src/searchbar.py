import oracledb

def getSearchOptions(connection: oracledb.Connection):
    cursor = connection.cursor()
    result = {}

    # ID, NAME, COMPANY, COUNT
    query_file = open('queries/ArticlesTickersCount.sql', 'r')
    query_string = query_file.read()
    query_file.close()

    cursor.execute(query_string)
    result['stock'] = cursor.fetchall()

    # ID, SECTOR, NULL, COUNT
    query_file = open('queries/ArticlesSectorsCount.sql', 'r')
    query_string = query_file.read()
    query_file.close()
    
    cursor.execute(query_string)
    result['sector'] = cursor.fetchall()

    return result