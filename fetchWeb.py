# coding=UTF-8
# import sys
import os
import urllib2
from time import strftime
from bs4 import BeautifulSoup
# import chardet
today = strftime('%Y%m%d')
print today
section = ["life","property","finance","local","entertainment","sports"]

for index in section:
	for day in range(0,7):
		for article_num in range(350,1000):
			url = 'http://www.appledaily.com.tw/realtimenews/article/%s/%d/675%03d/' % (index,int(today)-day,article_num) 
			print url
			content = urllib2.urlopen(url).read()
			if "該則即時新聞不存在 !" in content :
				continue
			else:
				#print content
		#charset = chardet.detect(content)	
				soup = BeautifulSoup(content, from_encoding='utf-8',)
		#print soup
		#print content
				title = soup.find("h1", {"id":"h1"})
				print title.string
				contents = soup.find("p", {"id":"summary"})
				#print "</iframe>" in contents.renderContents()
				while ("</iframe>" in contents.renderContents()):
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
				news_url = soup.find("meta", {"property":"og:url"})
				print news_url['content']
				news_source = soup.find("meta", {"property":"og:site_name"})
				print news_source['content']
				parse_date = strftime('%Y-%m-%d %H:%M:%S')
				print parse_date
				os.system("pause")

				#抓第一張圖片


#content_str = str(soup.findAll("div", {'class':'articulum'}))
#print content_str.encode('utf-8')

#for article in soup.findAll("div", {'class':'articulum'}):
#    print "Title: " + article.a.contents[0]

    #print "Link: " + article.a['href']
    #print ""