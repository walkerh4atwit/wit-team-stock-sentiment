import oracledb

def getLeaderTable():
    connection=oracledb.connect(
        config_dir="Wallet_database1",
        user="backend",
        password="Password123@",
        dsn="database1_low",
        wallet_location="Wallet_database1",
        wallet_password="Password1"
    )

    cursor = connection.cursor()

    # first query
    # TICKER, SCORE
    query_file = open("queries/LeaderTablesByTicker.sql", "r")
    query_string = query_file.read()
    cursor.execute(query_string)

    data = cursor.fetchall()
    count = 0

    # if there needs to be a tie handling
    if data[4][1] == data[5][1]:
        query_file = open("queries/LeaderTablesTieHandler.sql", "r")

        query_string = query_file.read()
        query_string = query_string.replace(":1", "ADMIN.TICKERS")

        cursor.execute(query_string, (data[4][1],))

        count = cursor.fetchone()[0]

    data_push = []

    rank = 0

    for i, row in enumerate(data):
        if i == 4 and count:
            data_push.append([str(count) + " STOCKS TIED", data[4][1], rank+1])
            continue
        data_push.append([*list(row), rank + 1])
        if i:
            if data[i][1] != data[i-1][1]:
                rank += 1

    #print(data_push)

    return data_push[:5]

#getLeaderTable()
