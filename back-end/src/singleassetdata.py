import oracledb

def getAssetData(asset_type: str, id: int, cnx: oracledb.Connection):
    cursor = cnx.cursor()
    result = {}

    if asset_type == 'sector':
        query_string = "SELECT * FROM ADMIN.SECTORS WHERE ID = :1"
    elif asset_type == 'stock':
        query_file = open("queries/SingleStockData.sql", "r")
        query_string = query_file.read()
        query_file.close()
    else:
        raise Exception("Invalid asset type specified for single asset data, must be sector or stock")

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