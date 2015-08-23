# coding=UTF-8
import logging

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
from time import strftime
from bs4 import BeautifulSoup

from news import News

import datetime

today = strftime('%Y%m%d')

SECTIONS = ["life","property","finance","local","entertainment","sports"]

def parse_string_to_popularity(stringpopularity):
    if stringpopularity == None:
        return 0

    index_of_left_bracket = stringpopularity.index("(")
    index_of_right_bracket = stringpopularity.index(")")
    popularity = stringpopularity[index_of_left_bracket + 1: index_of_right_bracket]
    return int(popularity)

def parse_string_to_datetime(stringtime):
    index_of_year = stringtime.index("年")
    index_of_month = stringtime.index("月")
    index_of_day = stringtime.index("日")
    index_of_hour = stringtime.index(":")

    year = int(stringtime[: index_of_year])
    month = int(stringtime[index_of_year+1: index_of_month])
    day = int(stringtime[index_of_month+1: index_of_day])
    hour = int(stringtime[index_of_day+1: index_of_hour])
    minute = int(stringtime[index_of_hour+1: ])
    second = 0

    return create_datetime(year=year, month=month, day=day, hour=hour,
                           minute=minute, second=second)

def create_datetime(year=2015, month=1, day=1, hour=0, minute=0, second=0):
    return datetime.datetime(year, month, day, hour, minute, second)

def test_parse_url():
    parse_one_url("fashion", 20150822, 760) # 760 = 675360
    logging.info("Test parse end")

def parse_one_url(category, day, article_num):
    url = 'http://www.appledaily.com.tw/realtimenews/article/%s/%d/675%03d/' % (category, day, article_num)
    parse_single_url(url)

def parse_single_url(url):
    content = urllib2.urlopen(url).read()
    if "該則即時新聞不存在" in content:
        return False
    else:
        soup = BeautifulSoup(content, from_encoding='utf-8',)
        title = str(soup.find("h1", {"id":"h1"}).string)
        contents = soup.find("p", {"id":"summary"})
        while "</iframe>" in contents.renderContents():
            if contents.iframe.decompose() == None :
               break
        desc_contents = contents.renderContents()
        popularity_data = soup.find("a", attrs={"class":"function_icon clicked"})
        if popularity_data == None:
            popularity = 0
        else:
            popularity = parse_string_to_popularity(popularity_data.string)
        news_datetime = parse_string_to_datetime(soup.find("time").string)
        news_url = soup.find("meta", {"property":"og:url"})['content']
        news_source = soup.find("meta", {"property":"og:site_name"})['content']
        img_url1 = soup.find("a",attrs={"class":"t1"})
        img_url2 = soup.find("figure", attrs={"class":"lbimg sgimg sglft"})

        if img_url1 != None:
            img_url = img_url1.img['src']
        elif img_url2 != None:
            img_url = img_url2.a.img['src']
        else:
            img_url = ""

        logging.debug("news_url: " + str(news_url))
        logging.debug("title: " + str(title))
        logging.debug("content: " + str(desc_contents))
        logging.debug("popularity: " + str(popularity))
        logging.debug("news_datetime: " + str(news_datetime))
        logging.debug("news_first_image_url: " + str(img_url))
        logging.debug("news_source: " + str(news_source))

        news = News(news_url=news_url,
                    title=title,
                    content=desc_contents,
                    popularity=popularity,
                    news_datetime=news_datetime,
                    news_first_image_url=img_url,
                    news_source=news_source)

        logging.info("Add news: " + str(news))
        news.writetodb()
        return True

def parse_all_url():
    for index in SECTIONS:
        for day in range(0,7): # parse from last 7 days to today.
            for article_num in range(0,1000):
                parse_one_url(index, int(today)-day, article_num)
