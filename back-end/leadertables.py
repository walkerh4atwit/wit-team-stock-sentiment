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
    rank = 0
    data_push = []

    for i, row in enumerate(data):
        rankstring = str(rank + 1)
        if row[1] == data[i - 1][1] and i:
            rankstring = ""
        else:
            rank += 1
        if i==4 and count:
            data_push.append([str(count) + " TIED", row[1], rankstring])
            continue
        data_push.append([*list(row), rankstring])

    return data_push

def getLeaderTables(connection: oracledb.Connection):
    cursor = connection.cursor()

    data_in = []
    data_out = {}

    # first query
    # TICKER, SCORE
    query_file = open("queries/LeaderTables.sql", "r")
    query_string = query_file.read()
    query_file.close()

    for i, table in enumerate([
        {"order": "asc","table": "Tickers","field":"ticker"},
        {"order": "desc","table": "Tickers","field":"ticker"},
        {"order": "asc","table": "Sectors","field":"name"},
        {"order": "desc","table": "Sectors","field":"name"}
    ]):
        
        param_query_string = query_string

        param_query_string = param_query_string.replace(":TABLE", table['table'])
        param_query_string = param_query_string.replace(":ORDER", table['order'])
        param_query_string = param_query_string.replace(":FIELD", table['field'])

        cursor.execute(param_query_string)
        
        data_in.append(cursor.fetchall())

        count = countTies(data_in[i], cursor, type_table = table['table'])
        data_out[table["order"] + table["table"]] = handleTies(data_in[i], count)[:5]

    return data_out

    # print(data_out)

# getLeaderTables()