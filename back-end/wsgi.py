from flask import Flask, make_response, jsonify

app = Flask(__name__)

# Routed to the root URL of this server
# This route will not do anything and has
# no reroute
@app.route("/")
def root_request():
    response = make_response(
        "Bad request to root\n"
    )
    response.status_code = 404
    return response

# This route attemps to build a sentiment
# report for a certain stock ticker
@app.route("/sentiment/<ticker>")
def sentiment_request(ticker):
    response = make_response(
        "Sentiment with " + ticker + "\n"
    )
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
    response.status_code = 200
    return response

# This route helps the front-end show
# the ticker values according to a first
# character that is provided in the request
@app.route("/tickers")
def get_tickers(fst):
    response = make_response(
        jsonify({
            "tickers": "AAPL"
        })
    )
    response.status_code = 200
    return response

app.run()