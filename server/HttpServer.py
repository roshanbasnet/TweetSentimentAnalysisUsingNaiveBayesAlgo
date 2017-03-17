import csv
import os
import tweepy
from flask import Flask, jsonify
from flask import json
from flask import render_template
from flask import request
import download_tweets
import process_tweets
import Sentiment2 as s1
import json
import re
from flask_cors import CORS
tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder='../templates', static_folder='../static')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/downloads', methods=["POST"])
def sentiment():
    sentiment_values = []
    search = json.loads(request.data)
    print(search)
    search = search["search"]
    #search = request.form.get("search")
    print(search)

    tweets = download_tweets.get_all_tweets(search,100)
    count = len(tweets)
    for data in tweets:
        sentiment_value, confidence = s1.sentimenttest(data)
        sentiment_values.append(sentiment_value)
    return jsonify({"sentiments":sentiment_values, "tweets":tweets, "username":search})

if __name__ == '__main__':
    app.run(debug=True)

