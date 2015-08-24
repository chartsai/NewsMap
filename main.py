#coding=UTF-8
import logging

from flask import Flask
from flask import request

app = Flask(__name__)
app.config['DEBUG'] = True

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from google.appengine.api import taskqueue
from google.appengine.ext import db

import json
from news import News
from news import NewsModel
import fetchWeb
import landmark

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

@app.route('/parse_hardcode_url')
def parseHardcodeUrl():
    url = "http://www.appledaily.com.tw/realtimenews/section/hot/"
    result = fetchWeb.parse_single_url(url)
    if result:
        return "Parse single url succeed: " + url
    else:
        return "Parse single url failed... " + url

@app.route('/parse_single_url')
def parseSingleUrl():
    url = request.args.get("url")
    if url == None or url == "":
        return "There is no URL to parse"
    result = fetchWeb.parse_single_url(url)
    if result:
        return "Parse single url succeed: " + url
    else:
        return "Parse single url failed... " + url

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


@app.route('/query_landmark')
def query_landmark():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    # if lat == None or lng == None:
    #     return '{}'
    #
    # latlng = str(lat) + "," + str(lng)
    #
    # if latlng not in landmark.LANDMARK_KEYWORDS:
    #     return '{}'

    lm = landmark.getlandmark(lat, lng)
    if lm == None:
        return '{}'

    first_keyword = landmark.LANDMARK_KEYWORDS[lm.location][0]
    related_news_ids = lm.related_news

    logging.info("Query position has " + str(len(related_news_ids)) + " news")

    return_dict = {'landmark_name': first_keyword}
    return_list = []
    for news_key in related_news_ids:
        key = db.Key(news_key)
        entry = NewsModel.all().filter('__key__ =', key).get()
        if entry != None:
            dic = {}
            dic['news_id'] = news_key
            dic['title'] = entry.title
            return_list.append(dic)
    return_dict['news_list'] = return_list

    return json.dumps(return_dict)

@app.route('/trigger_background_landmark')
def landmarkWorker():
    taskqueue.add(queue_name='default', url='/perform_create_landmark', params={})
    return "Trigger the creation of landmark in background... done."

def is_keyword_in_news(keywords, title, content):
    title_content = title + content
    for keyword in keywords:
        if keyword in title_content:
            return True
    return False

@app.route('/perform_create_landmark', methods=['POST'])
def perform_create_landmark():

    logging.info("Start to create landmark database")

    all_news = NewsModel.all()
    for latlng in landmark.LANDMARK_KEYWORDS:
        counter = 0
        keywords = landmark.LANDMARK_KEYWORDS[latlng]
        related_news_keys = []
        for news in all_news:
            result = is_keyword_in_news(keywords, news.title, news.content)
            if result == True:
                related_news_keys.append(str(news.key()))
                counter += 1

        ret = str(related_news_keys)

        lm = landmark.Landmark(latlng, related_news_keys)
        lm.writetodb()
        logging.info("Create database for " + str(latlng) + " completed, it has " + str(counter) + " news")

    logging.info("All database for landmark are completed")

    return "Write to db complete"

@app.route('/query_article')
def query_article():
    key = db.Key(request.args.get('news_key'))
    entry = NewsModel.all().filter('__key__ =', key).get()
    if entry != None:
        return json.dumps({"title"      : entry.title,
                           "datetime"   : str(entry.news_datetime),
                           "article"    : entry.content,
                           "popularity" : entry.popularity,
                           "image_url"  : entry.news_first_image_url,
                           "url"        : entry.news_url})
    else:
        return '{}'

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
