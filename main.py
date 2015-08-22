#coding=UTF-8
import logging

from flask import Flask
from flask import request

app = Flask(__name__)
app.config['DEBUG'] = True

import os
import urllib2

from google.appengine.api import taskqueue

from news import News
import fetchWeb
from time import strftime
from bs4 import BeautifulSoup

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
@app.route('/testNews')
def testNews():
    # Try to add test url
    fetchWeb.test_parse_url()

    news = News()
    testurl = 'http://www.appledaily.com.tw/realtimenews/article/new/20150822/675760/'
    result = news.loadfromdb(testurl)
    return "Result: " + str(news)

@app.route('/trigger_background_parsing')
def parserWorker():
    taskqueue.add(queue_name='default', url='/perform_parsing', params={})
    return "Trigger the background parsing... done."

@app.route('/perform_parsing', methods=['POST'])
def perform_parsing():
    logging.info("perform_parsing start")
    fetchWeb.parse_all_url()
    logging.info("perform_parsing end")
    return "Performing background parsing end"

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
