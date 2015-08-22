from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

from news import News

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
@app.route('/testNews')
def testNews():
    news = News()
    news.loadfromdb("URL")
    return_str = str(news.title) + str(news.content)
    return return_str

@app.route('/addTestNews')
def addTestNews():
    news = News("URL")
    news.writetodb()
    return "Write News(URL) to db"


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
