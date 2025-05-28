from flask import Flask, make_response, jsonify, request
from flask import Response as Flask_Response

from searchbar import getSearchOptions
from leadertables import getLeaderTables
from singleassetdata import getAssetData
from article_cards import getArticleCards

import ipaddress, sys, json, os
from backend_util.db_connect import db_connect
from zipfile import ZipFile
from backend_util.oci_connect import oci_get_from_bucket
from backend_util.redis_util import cache_connect
from wsgi_util import \
    make_backend_response_cache_hit, \
    make_backend_response_cache_miss

# NOTE: Run all builds from pwd back-end

# Get the db credentials in the form of a wallet

# Finding build env
build_env = os.environ.get('BUILD_ENV')
if not build_env:
    raise KeyError('No build env specified.')

# Making the name string from the build env
db_wallet_name = 'Wallet-' + build_env + '.zip'

# Streaming the wallet from oci bucket
oci_get_from_bucket(db_wallet_name)

# Now unzipping the wallet and giving it a new name, Database-Wallet
db_wallet_file = ZipFile(db_wallet_name)
os.remove(db_wallet_name)
db_wallet_file.extractall('Database-Wallet')

# instantiate cache client caching
redis_client = cache_connect('redis-cache', 6379)
allowed_subnet = ipaddress.ip_network('10.0.10.0/24')

# THE APP
app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    print(f"404 Error: Path '{request.path}' not found. Method: {request.method}")
    return make_response("This route does not exist on sentiments back-end.\n", 404)

# Routed to the root URL of this server
# This route will not do anything and has
# no reroute
@app.route("/api")
def root_request():
    response = make_response(
        "Bad request to root.\n", 404
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# This route attemps to build a sentiment
# report for a certain stock ticker
@app.route("/api/sentiment/<type_asset>/<id>", methods=["GET"])
def sentiment_request(type_asset, id):
    db_conn = db_connect()

    response = make_response(
        jsonify(getAssetData(type_asset, id, db_conn)), 200
    )

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/api/articles/<type_asset>/<id>/<score>")
def article_request(type_asset, id, score): 
    db_conn = db_connect()

    response = make_response(
        jsonify(getArticleCards(type_asset, id, score, db_conn)), 200
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# This route is when a request is made
# to call for an action. Hopefully I can
# figure out how to make this auth'd to
# only certain sources
@app.route("/api/action/<id>")
def do_action(id):
    response = make_response(
        "Do action " + id + "\n", 200
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# This route helps the front-end show
# the ticker values according to a first
# character that is provided in the request
@app.route("/api/searchoptions", methods=["GET"])
def get_searchable_tickers():
    if redis_client and redis_client.exists('searchoptions'):
        data_string =redis_client.get('searchoptions')

        if data_string:
            data_dict = json.loads(data_string)
            response = make_response(jsonify(data_dict), 200)
        else:
            response = make_response("No cached data for searchoptions", 500)
    else:
        response = make_backend_response_cache_miss(getSearchOptions)
    
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# This route provides the data
# for the leader tables
@app.route("/api/leadertables", methods=["GET"])
def leader_tables():
    # raise Exception("Test exception 00")
    # data_string = redis_client.get("leadertables")
    # data_dict = {}
    if redis_client and redis_client.exists('leadertables'):
        data_string = redis_client.get('leadertables')

        if data_string:
            data_dict = json.loads(data_string)
            response = make_response(jsonify(data_dict), 200)
        else:
            response = make_response("No cached data found for leadertables", 500)
            
    else:
        response = make_backend_response_cache_miss(getLeaderTables)

    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/api/cache/<data_type>", methods=["POST"])
def cache_data(data_type):
    if data_type not in ["leadertables", "searchoptions"]:
        return make_response("Invalid datatype passed to API: " + data_type), 500

    cachee: str

    if request.remote_addr not in allowed_subnet:
        return make_response("Forbidden!", 400)
    
    db_conn = db_connect()

    if data_type == "leadertables":
        cachee = getLeaderTables(db_conn)
    
    if data_type == "searchoptions":
        cachee = getSearchOptions(db_conn)

    redis_client.setex(data_type, 800, json.dumps(cachee))

# local development environment
if len(sys.argv) == 1:
    app.run(port=3131, host='0.0.0.0')