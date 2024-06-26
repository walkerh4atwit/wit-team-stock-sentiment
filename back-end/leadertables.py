import oracledb
from oracledb.cursor import Cursor

def countTies(data: list[any], cursor: Cursor):
        # if there needs to be a tie handling
        if len(data) < 6:
            return 0
        if data[4][1] == data[5][1]:
            query_file = open("queries/LeaderTablesCountTies.sql", "r")

            query_string = query_file.read()
            query_string = query_string.replace(":1", "ADMIN.TICKERS")

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
            data_push.append([str(count) + " TIED", rankstring])
            continue
        data_push.append([*list(row), rankstring])

    return data_push

def getLeaderTables():
    connection=oracledb.connect(
        config_dir="Wallet_database1",
        user="backend",
        password="Password123@",
        dsn="database1_low",
        wallet_location="Wallet_database1",
        wallet_password="Password1"
    )

    cursor = connection.cursor()

    data_in = []
    data_out = {}

    # first query
    # TICKER, SCORE
    query_file = open("queries/LeaderTables.sql", "r")
    query_string = query_file.read()

    for i, table in enumerate([
        {"order": "asc","table": "Tickers","id":"ticker"},
        {"order": "desc","table": "Tickers","id":"ticker"},
        {"order": "asc","table": "Sectors","id":"name"},
        {"order": "desc","table": "Sectors","id":"name"}
    ]):
        cursor.execute(query_string
                       .replace(":1", table['order'])
                       .replace(":2", table['table'])
                       .replace(":3", table['id']))
        
        data_in.append(cursor.fetchall())

        count = countTies(data_in[i], cursor)
        data_out[table["order"] + table["table"]] = handleTies(data_in[i], count)

    

    # print(data_push)

    print(data_out)

getLeaderTables()