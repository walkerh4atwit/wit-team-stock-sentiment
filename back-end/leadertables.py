import oracledb
from oracledb.cursor import Cursor

def countTies(data: list[any], cursor: Cursor, type_table: str):
    # if there needs to be a tie handling
    if len(data) < 6:
        return 0
    if data[4][1] == data[5][1]:
        query_file = open("queries/LeaderTablesCountTies.sql", "r")

        query_string = query_file.read()

        query_string = query_string.replace(":TABLE", type_table)

        cursor.execute(query_string, (data[4][1],))

        return cursor.fetchone()[0]
    else: 
        return 0
        
def handleTies(data: list[any], count: int):
    data_push = []

    for i, row in enumerate(data):
        name = row[0]
        score = row[1]
        rankstring = row[2]

        if i and score == data[i-1][1]:
            rankstring = ""

        if i==4 and count:
            name = str(count) + " TIED"

        data_push.append([name, score, rankstring])

    return data_push

def getLeaderTables(connection: oracledb.Connection):
    cursor = connection.cursor()

    data_in = []
    data_out = {}

    # first query
    # TICKER, SENTIMENT_SCORE
    tickers_query_file = open("queries/LeaderTablesTickers.sql", "r")
    tickers_query_string = tickers_query_file.read()
    tickers_query_file.close()

    # second query
    # NAME, SENTIMENT_SCORE
    sectors_query_file = open("queries/LeaderTablesSectors.sql", 'r')
    sectors_query_string = sectors_query_file.read()
    sectors_query_file.close()

    # third query
    # a number
    ties_query_file = open("queries/LeaderTablesCountTies.sql", 'r')
    ties_query_string = ties_query_file.read()
    ties_query_file.close()

    for order in ['asc', 'desc']:
        
        # setting up queries for getting top/worst scorers
        tickers_query_string = tickers_query_string.replace(":ORDER", order)
        sectors_query_string = sectors_query_string.replace(":ORDER", order)

        # for the sectors
        cursor.execute(sectors_query_string)
        result = cursor.fetchall()
        data_in.append(result)
        tie_count = 0

        # this happens only if there's enough data
        if len(result) == 6:
            ties_query_string = ties_query_string.replace(":TABLE", "Sectors")
            cursor.execute(ties_query_string, (result[4][1]))
            tie_count_result = cursor.fetchone()

            # probably won't happen
            if tie_count_result is None:
                word = "lowest" if order == "asc" else "highest"
                raise Exception("Error grabbing the sentiment score of the\
                                fifth-" + word + " sector.")
            
            tie_count = tie_count_result[0]

        # calling handleties to pretty up the results
        data_out[order + "Sectors"] = handleTies(result, tie_count)

        cursor.execute(tickers_query_string)
        result = cursor.fetchall()
        data_in.append(result)
        tie_count = 0

        # this happens only if there's enough data
        if len(result) == 6:
            ties_query_string = ties_query_string.replace(":TABLE", "Tickers")
            cursor.execute(ties_query_string, (result[4][1]))
            tie_count_result = cursor.fetchone()

            # probably won't happen
            if tie_count_result is None:
                word = "lowest" if order == "asc" else "highest"
                raise Exception("Error grabbing the sentiment score of the\
                                fifth-" + word + " ticker.")
            
            tie_count = tie_count_result[0]

        data_out[order + "Tickers"] = handleTies(result, tie_count)

    return data_out

    # print(data_out)

# getLeaderTables()