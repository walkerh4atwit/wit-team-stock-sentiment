from oracledb import Connection

def getArticleCards(asset_type: str, id: int, score: int, cnx: Connection):
    csr = cnx.cursor()

    querystring: str
    if asset_type == "stock":
        with open("queries/ArticleCardsTickers.sql", "r") as file:
            querystring = file.read()
    elif asset_type == "sector":
        with open("queries/ArticleCardsSectors.sql", "r") as file:
            querystring = file.read()
    else:
        raise Exception("Invalid asset type specified for article cards, must be sector or stock")
     
    csr.execute(querystring, (score, id))
    return csr.fetchall()