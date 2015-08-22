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
from time import strftime
from bs4 import BeautifulSoup

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
@app.route('/testNews')
def testNews():
    result = news.loadfromdb("URL")
    return_str = str(news.title) + str(news.content)
    return "Result: " + result + "<br>" + return_str

@app.route('/addTestNews')
def addTestNews():
    return "Do nothing"

def do_parsing():
	today = strftime('%Y%m%d')
	    print today
	    section = ["life","local"]
	    
	    for index in section :
	        for day in range(0,7):
	            for article_num in range(350,1000):
	                url = 'http://www.appledaily.com.tw/realtimenews/article/%s/%d/675%03d' % (index,int(today)-day,article_num)
	                print url
	                content = urllib2.urlopen(url).read()
	                if "該則即時新聞不存在 !" in content:
	                    continue
	                else:
	                    soup = BeautifulSoup(content, from_encoding='utf-8',)
	                    title = soup.find("h1", {"id":"h1"})
	                    print title.string
	                    contents = soup.find("p", {"id":"summary"}) 
	                    while "</iframe>" in contents.renderContents():
	                        contents.iframe.decompose()
	                    desc_contents = contents.renderContents()
	                    print desc_contents
	                    popularity = soup.find("a", attrs={"class":"function_icon clicked"})
	                    if popularity == None:
	                        print popularity 
	                    else:
	                        print popularity.string
	                    news_datetime = soup.find("time")
	                    print news_datetime.string
	                    news_url = soup.find("meta",{"property":"og:url"})
	                    print news_url['content']
	                    news_source = soup.find("meta", {"property":"og:site_name"})
	                    print news_source['content']
	                    parse_date = strftime('%Y-%m-%d %H:%M:%S')
	                    print parse_date
	                    os.system("pause")
                    	news = News(news_url, title, desc_contents, popularity, news_datetime,"", news_source)
    					result = news.writetodb()

@app.route('/trigger_background_parsing')
def parserWorker():
    taskqueue.add(queue_name='default', url='/perform_parsing', params={})
    return "Recieve: "

@app.route('/perform_parsing', methods=['POST'])
def perform_parsing():
    logging.info("perform_parsing start")
    # TODO put looping parsing code here.
    logging.info("perform_parsing end")
    return "Performing background parsing end"

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
