import oracledb

def getAssetData(asset_type: str, id: int):
    connection=oracledb.connect(
        config_dir="Wallet_database1",
        user="backend",
        password="Password123@",
        dsn="database1_low",
        wallet_location="Wallet_database1",
        wallet_password="Password1"
    )

    cursor = connection.cursor()
    result = {}

    if asset_type == 'sector':
        query_string = "SELECT * FROM ADMIN.SECTORS WHERE ID = :1"
    elif asset_type == 'stock':
        query_string = open("queries/SingleStockData.sql", "r").read()
    else:
        return "Invalid asset type"

    cursor.execute(query_string.replace(':1', id))

    data_in = cursor.fetchall()[0]

    if asset_type == 'stock':
        result['sector'] = data_in[5]
        result['score'] = data_in[4]
        result['name'] = data_in[2]
        result['ticker'] = data_in[1]
    else:
        result['sector'] = id
        result['score'] = data_in[2]
        result['name'] = data_in[1]
        result['ticker'] = ""

    return result