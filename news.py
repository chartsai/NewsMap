import sys
reload(sys)
sys.setdefaultencoding('utf8')

from google.appengine.ext import db

class NewsModel(db.Model):
    news_url = db.StringProperty(required=True)
    title = db.StringProperty()
    content = db.StringProperty()
    popularity = db.IntegerProperty()
    news_datetime = db.DateTimeProperty()
    news_first_image_url = db.StringProperty()
    news_source = db.StringProperty()
    parse_datetime = db.DateTimeProperty(auto_now_add=True)

class News:
    def __init__(self, news_url="", title="News", content="", popularity=0,
                 news_datetime="", news_first_image_url="", news_source="Unknown"):
        self.setnewsdata(news_url, title, content, popularity, news_datetime,
                         news_first_image_url, news_source)


    def setnewsdata(self, news_url="", title="News", content="", popularity=0,
                    news_datetime="", news_first_image_url="", news_source="Unknown"):
        self.news_url = news_url
        self.title = title
        self.content = content
        self.popularity = popularity
        self.news_datetime = news_datetime
        self.news_first_image_url = news_first_image_url
        self.news_source = news_source

    def writetodb(self):
        news_entry = NewsModel.all().filter("news_url =", self.news_url).get()
        if news_entry == None:
            # create new entry
            key = NewsModel(news_url = self.news_url,
                            title = self.title,
                            content = self.content,
                            popularity = self.popularity,
                            news_datetime = self.news_datetime,
                            news_first_image_url = self.news_first_image_url,
                            news_source = self.news_source)
            db.put(key)
        else:
            # update exist entry
            news_entry.title = self.title
            news_entry.content = self.content
            news_entry.popularity = self.popularity
            news_datetime = self.news_datetime
            news_entry.news_first_image_url = self.news_first_image_url
            news_entry.news_source = self.news_source
            db.put(news_entry)

    def loadfromdb(self, url):
        news_entry = NewsModel.all().filter("news_url =", self.news_url).get()
        if news_entry != None:
            self.news_url = news_entry.news_url
            self.title = news_entry.title
            self.content = news_entry.content
            self.popularity = news_entry.popularity
            self.news_datetime = news_entry.news_datetime
            self.news_first_image_url = news_entry.news_first_image_url
            self.news_source = news_entry.news_source
