#coding=UTF-8
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from google.appengine.ext import db

class LandmarkModel(db.Model):
    location = db.StringProperty(required=True)
    related_news = db.StringListProperty(str, default=[], required=True)
    parse_datetime = db.DateTimeProperty(auto_now=True)

class Landmark:
    def __init__(self, location="", related_news=[]):
        self.setlandmarkdata(location=location, related_news=related_news)

    def setlandmarkdata(self, location, related_news=[]):
        self.location = location
        self.related_news = related_news

    def __str__(self):
        str_args = (str(self.location), str(self.related_news))
        return "Location: %s, News Id: %s" % str_args

    def writetodb(self):
        news_entry = LandmarkModel.all().filter("location =", self.location).get()
        if news_entry == None:
            # create new entry
            key = LandmarkModel(location = self.location,
                                related_news = self.related_news)
            db.put(key)
            return "create new Landmark"
        else:
            # update exist entry
            news_entry.location = self.location
            news_entry.related_news = self.related_news
            return "Update exist Landmark"

    def loadfromdb(self, location):
        news_entry = LandmarkModel.all().filter("location =", location).get()
        if news_entry != None:
            self.location = news_entry.location
            self.related_news = news_entry.related_news
            return "Load Landmark from DB succeed"
        else:
            return "The loaded Landmark is not exist in DB"

str1 = '25.1347802,121.5324453'
str2 = '25.1023554,121.5484925'
str3 = '25.078304,121.526137'
str4 = '25.098493,121.5361083'
str5 = '25.1682468,121.5742471'
str6 = '25.0958292,121.5182994'
str7 = '25.112834,121.56488'
str8 = '25.076902,121.526809'
str9 = '25.0949147,121.5301283'
str10 = '25.103893,121.530267'
str11 = '25.0991799,121.5465894'
str12 = '25.096607,121.5308677'
str13 = '25.101139,121.549488'
str14 = '25.098593,121.537564'
str15 = '25.1516929,121.548373'
str16 = '25.1009681,121.5519764'
str17 = '25.0959028,121.529554'
str18 = '25.084873,121.525077'
str19 = '25.1095565,121.5469651'
str20 = '25.0861984,121.5281041'
str21 = '25.1156276,121.5769132'
str22 = '25.1669979,121.566164'
str23 = '25.10316,121.530785'
str23 = '25.10316,121.530785'
str24 = '25.087793,121.5242251'
str25 = '25.1668446,121.5633701'
str26 = '25.1023449,121.5536577'
str27 = '25.1033289,121.5311337'
str28 = '25.0957569,121.5166018'
str29 = '25.097094,121.51471,17'
str30 = '25.0645028,121.5133148'

LANDMARK_KEYWORDS = {
 str1: ['士林區'],
 str2: ['國立故宮博物院','故宮','故宮博物院'],
 str3: ['圓山大飯店','圓山飯店','台北圓山飯店','臺北圓山飯店'],
 str4: ['雙溪公園'],
 str5: ['擎天崗'],
 str6: ['台北市立天文科學教育館'],
 str7: ['明德樂園'],
 str8: ['北安公園'],
 str9: ['士林官邸'],
 str10: ['芝山岩'],
 str11: ['至德園'],
 str12: ['志成公園'],
 str13: ['至善園'],
 str14: ['至善公園'],
 str15: ['前山公園'],
 str16: ['順益台灣原住民博物館'],
 str17: ['福林公園'],
 str18: ['劍潭公園'],
 str19: ['林語堂故居','林語堂先生紀念館'],
 str20: ['銘傳大學','銘傳大學臺北校區','銘傳大學台北校區'],
 str21: ['內雙溪森林自然公園'],
 str22: ['冷水坑遊憩區'],
 str23: ['芝山巖惠濟宮'],
 str24: ['士林夜市'],
 str25: ['冷水坑溫泉'],
 str26: ['張大千紀念館'],
 str27: ['芝山文化生態綠園'],
 str28: ['國立台灣科學教育館','科教館'],
 str29: ['台北市立兒童新樂園'],
 str30: ['大同區'],
}
g
