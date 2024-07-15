from flask import Flask, make_response, jsonify
from searchbar import getSearchOptions
from leadertables import getLeaderTables
from singleassetdata import getAssetData
import sys

app = Flask(__name__)

# Routed to the root URL of this server
# This route will not do anything and has
# no reroute
@app.route("/")
def root_request():
    response = make_response(
        "Bad request to root\n"
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 404
    return response

# This route attemps to build a sentiment
# report for a certain stock ticker
@app.route("/sentiment/<type_asset>/<id>")
def sentiment_request(type_asset, id):
    response = make_response(
        getAssetData(type_asset, id)
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response

# This route is when a request is made
# to call for an action. Hopefully I can
# figure out how to make this auth'd to
# only certain sources
@app.route("/action/<id>")
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
@app.route("/searchoptions")
def get_tickers():
    response = make_response(
        jsonify(getSearchOptions())
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# This route provides the data
# for the leader tables
@app.route("/leadertables")
def leaderTables():
    response = make_response(
        jsonify(getLeaderTables())
    )
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# development environment
if len(sys.argv) == 1:
    app.run(port=3131, host='0.0.0.0')