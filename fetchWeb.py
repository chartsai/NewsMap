# coding=UTF-8
import os
import urllib2
from time import strftime
from bs4 import BeautifulSoup

today = strftime('%Y%m%d')
print today
section = ["life","property","finance","local","entertainment","sports"]

def test_parse_url():
    # TODO call parse_one_url(...) with a exist news.
    # please remove pass after parse_one_url(...) complete
    pass

def parse_one_url(index, day, article_num):
    url = 'http://www.appledaily.com.tw/realtimenews/article/%s/%d/675%03d/' % (index, day, article_num)
    content = urllib2.urlopen(url).read()
    if "該則即時新聞不存在" in content:
        return
    else:
        soup = BeautifulSoup(content, from_encoding='utf-8',)
        title = soup.find("h1", {"id":"h1"})
        contents = soup.find("p", {"id":"summary"})
        while ("</iframe>" in contents.renderContents()):
            contents.iframe.decompose()
        desc_contents = contents.renderContents()
        popularity = soup.find("a", attrs={"class":"function_icon clicked"})
        if popularity == None:
            popularity = "0"
        news_datetime = soup.find("time")
        news_url = soup.find("meta", {"property":"og:url"})
        news_source = soup.find("meta", {"property":"og:site_name"})
        parse_date = strftime('%Y-%m-%d %H:%M:%S')
        os.system("pause")
        #抓第一張圖片
        content_str = str(soup.findAll("div", {'class':'articulum'}))
        if content_str == None:
            content_str = ""
        content_str = content_str.encode('utf-8')
        news = News(news_url=news_url,
                    title=title,
                    content=desc_contents,
                    popularity=popularity,
                    news_datetime=news_datetime,
                    news_first_image_url=content_str,
                    news_source=news_source)
        news.writetodb()
        logging.info("Prase: " + (str(news)))

def parse_all_url():
    for index in section:
        for day in range(0,7):
            for article_num in range(0,1000):
                parse_one_url(index, int(today)-day, article_num)
