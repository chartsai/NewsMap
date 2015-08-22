import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from bs4 import BeautifulSoup

from google.appengine.ext import db

class NewsModel(db.Model):
    news_url = db.StringProperty(required=True)
    title = db.StringProperty()
    content = db.TextProperty()
    popularity = db.IntegerProperty()
    news_datetime = db.DateTimeProperty()
    news_first_image_url = db.StringProperty()
    news_source = db.StringProperty()
    parse_datetime = db.DateTimeProperty(auto_now=True)

class News:
    def __init__(self, news_url="", title="News", content="", popularity=0,
                 news_datetime="", news_first_image_url="", news_source="Unknown"):
        self.setnewsdata(news_url, title, content, popularity, news_datetime,
                         news_first_image_url, news_source)

    def __str__(self):
        str_args = (str(self.news_url), str(self.title), str(self.popularity),
                    str(self.news_source), str(self.news_datetime))
        return "URL: %s, title: %s, popularity: %s, source: %s, news_datetime: %s" % str_args

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
                            content = db.Text(self.content, encoding='utf-8'),
                            popularity = self.popularity,
                            news_datetime = self.news_datetime,
                            news_first_image_url = self.news_first_image_url,
                            news_source = self.news_source)
            db.put(key)
            return "create new News"
        else:
            # update exist entry
            news_entry.title = self.title
            news_entry.content = db.Text(self.content, encoding='utf-8')
            news_entry.popularity = self.popularity
            news_datetime = self.news_datetime
            news_entry.news_first_image_url = self.news_first_image_url
            news_entry.news_source = self.news_source
            db.put(news_entry)
            return "Update exist News"

    def loadfromdb(self, url):
        news_entry = NewsModel.all().filter("news_url =", url).get()
        if news_entry != None:
            self.news_url = news_entry.news_url
            self.title = news_entry.title
            self.content = str(news_entry.content)
            self.popularity = news_entry.popularity
            self.news_datetime = news_entry.news_datetime
            self.news_first_image_url = news_entry.news_first_image_url
            self.news_source = news_entry.news_source
            return "load DB succeed"
        else:
            return "The loaded News is not exist in DB"
