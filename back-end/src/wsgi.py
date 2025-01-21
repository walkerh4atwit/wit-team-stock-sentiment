from flask import Flask, make_response, jsonify, request, Response
from searchbar import getSearchOptions
from leadertables import getLeaderTables
from singleassetdata import getAssetData
from article_cards import getArticleCards
from db_connect import db_connect
from oci_connect import oci_util
import ipaddress, redis, sys, json

# that's all's we need here
oci_util()

# for the caching
redis_client = redis.StrictRedis(host="redis-cache", port="6379", decode_responses=True)
allowed_subnet = ipaddress.ip_network('10.0.10.0/24')

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    print(f"404 Error: Path '{request.path}' not found. Method: {request.method}")
    return jsonify(error="This route does not exist on sentiments."), 404

# Routed to the root URL of this server
# This route will not do anything and has
# no reroute
@app.route("/api")
def root_request():
    response = make_response(
        "Bad request to root\n"
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 404
    return response

# This route attemps to build a sentiment
# report for a certain stock ticker
@app.route("/api/sentiment/<type_asset>/<id>")
def sentiment_request(type_asset, id):
    db_conn = db_connect()

    response = make_response(
        getAssetData(db_conn, type_asset, id)
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response

@app.route("/api/articles/<type_asset>/<id>/<score>")
def article_request(type_asset, id, score):
    db_conn = db_connect()

    response = make_response(
        jsonify(getArticleCards(type_asset, id, score, db_conn))
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response

# This route is when a request is made
# to call for an action. Hopefully I can
# figure out how to make this auth'd to
# only certain sources
@app.route("/api/action/<id>")
def do_action(id):
    response = make_response(
        "Do action " + id + "\n"
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response

# This route helps the front-end show
# the ticker values according to a first
# character that is provided in the request
@app.route("/api/searchoptions")
def get_tickers():
    data_string = redis_client.get("searchoptions")
    data_dict = {}

    if data_string is None:
        db_conn = db_connect()
        data_dict = getSearchOptions(db_conn)
        redis_client.setex("searchoptions", 800, json.dumps(data_dict))
    else:
        data_dict = json.loads(data_string)

    response = make_response(
        jsonify(data_dict)
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response

# This route provides the data
# for the leader tables
@app.route("/api/leadertables")
def leaderTables():
    data_string = redis_client.get("leadertables")
    data_dict = {}

    if data_string is None:
        db_conn = db_connect()
        data_dict = getLeaderTables(db_conn)
        redis_client.setex("leadertables", 800, json.dumps(data_dict))
    else:
        data_dict = json.loads(data_string)

    response = make_response(
        jsonify(data_dict)
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response

@app.route("/api/cache/<data_type>", methods=['POST'])
def cache_data(data_type):
    if data_type not in ["leadertables", "searchoptions"]:
        return(make_response("Invalid datatype passed to API: " + data_type + "\n"))

    cachee: str

    if request.remote_addr not in allowed_subnet:
        return(make_response("Forbidden!\n"))
    
    db_conn = db_connect()

    if data_type == "leadertables":
        cachee = getLeaderTables(db_conn)
    
    if data_type == "searchoptions":
        cachee = getSearchOptions(db_conn)

    redis_client.setex(data_type, 800, json.dumps(cachee))

# development environment
if len(sys.argv) == 1:
    app.run(port=3131, host='0.0.0.0')