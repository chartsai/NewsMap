import logging

from flask import Flask
from flask import request

app = Flask(__name__)
app.config['DEBUG'] = True

from google.appengine.api import taskqueue
from news import News

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
@app.route('/testNews')
def testNews():
    result = news.loadfromdb("URL")
    return_str = str(news.title) + str(news.content)
    return "Result: " + result + "<br>" + return_str

@app.route('/addTestNews')
def addTestNews():
    news = News("URL", title="MyNews", content="Some content")
    result = news.writetodb()
    return "Write News(URL) to db, result is: " + result

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
