import sys
reload(sys)
sys.setdefaultencoding('utf8')

from google.appengine.ext import db

class NewsModel(db.Model):
    title = db.StringProperty(required=True)
    content = db.StringProperty()
    populatiry = db.IntegerProperty()
    news_datetime = db.DateTimeProperty()
    news_url = db.StringProperty(required=True)
    news_first_image_url = db.StringProperty()
    news_source = db.StringProperty()
    download_datetime = db.DateTimeProperty(auto_now_add=True)
