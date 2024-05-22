from flask import Flask, make_response, jsonify

app = Flask(__name__)

@app.route("/")
def root_request():
    response = make_response(
        "Bad request to root\n"
    )
    response.status_code = 404
    return response

@app.route("/sentiment/<ticker>")
def sentiment_request(ticker):
    response = make_response(
        "Sentiment with " + ticker + "\n"
    )
    response.status_code = 200
    return response

@app.route("/action/<id>")
def do_action(id):
    response = make_response(
        "Do action " + id + "\n"
    )
    response.status_code = 200
    return response

@app.route("/ticker/<fst>")
def get_tickers(fst):
    response = make_response(
        jsonify({
            "ticker": "AAPL"
        })
    )
    response.status_code = 200
    return response

app.run()