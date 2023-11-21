#!/usr/bin/python3
from flask import Flask, render_template, Blueprint
from flask_caching import Cache
import feedparser

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
news_feeds_3 = [ 'https://www.annapolis.gov/RSSFeed.aspx?ModID=1&CID=Headlines-12', ]
news_feeds_2 = [ 'http://rss.cnn.com/rss/edition.rss', 'http://feeds.bbci.co.uk/news/world/rss.xml', 'https://www.reuters.com/tools/rss', ]
news_feeds_1 = [ 'https://www.darkreading.com/rss.xml', 'http://nakedsecurity.sophos.com/feed/', 'https://www.cisa.gov/news.xml', 'https://feeds.feedburner.com/TheHackersNews', 'http://krebsonsecurity.com/feed/', 'http://www.bleepingcomputer.com/feed/', 'http://cybermashup.com/feed/', ]

@cache.cached(timeout=3600)  # Cache for 1 hour
def fetch_news_feeds(news_feeds):
    feeds = []
    for url in news_feeds:
        feed = feedparser.parse(url)
        feeds.extend(feed.entries)
    return feeds

@app.route('/')
def default_page():
    return render_template('default.html')

app_1 = Blueprint('csn', __name__)
app_2 = Blueprint('nn', __name__)
app_3 = Blueprint('aln', __name__)

@app_1.route('/')
def display_news_1():
    feeds = fetch_news_feeds(news_feeds_1)
    return render_template('csn_news.html', feeds=feeds)

@app_2.route('/')
def display_news_2():
    feeds = fetch_news_feeds(news_feeds_2)
    return render_template('nn_news.html', feeds=feeds)

@app_3.route('/')
def display_news_3():
    feeds = fetch_news_feeds(news_feeds_3)
    return render_template('aln_news.html', feeds=feeds)


app.register_blueprint(app_1, url_prefix='/csn')
app.register_blueprint(app_2, url_prefix='/nn')
app.register_blueprint(app_3, url_prefix='/aln')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('/etc/letsencrypt/live/kungfulinux.com/fullchain.pem', '/etc/letsencrypt/live/kungfulinux.com/privkey.pem'))


