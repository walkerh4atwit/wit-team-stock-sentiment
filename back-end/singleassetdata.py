import oracledb

def getAssetData(connection: oracledb.Connection, asset_type: str, id: int):
    cursor = connection.cursor()
    result = {}

    if asset_type == 'sector':
        query_string = "SELECT * FROM ADMIN.SECTORS WHERE ID = :1"
    elif asset_type == 'stock':
        query_string = open("queries/SingleStockData.sql", "r").read()
    else:
        return "Invalid asset type"

    cursor.execute(query_string, (id,))

    data_in = cursor.fetchone()

    if not data_in:
        return {
            'sector': '',
            'score': 0,
            'name': '',
            'ticker': ''
        }

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