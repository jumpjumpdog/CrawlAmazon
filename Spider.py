# -*- coding: utf-8 -*-
import requests, redis,pickle
import config, random, csv
from threadTest import getProxyList
from config import get_header
from collections import namedtuple
from bs4 import BeautifulSoup
import time

# def spider(url):
#     payload = {'key1': 'value1', 'key2': 'value2'}
#     r = requests.post(url, data=payload)
#     soup = BeautifulSoup(r.text ,"lxml")
#     title = soup.find("span", attrs={"id":"productTitle"}).string
#     title = title.replace("\n","")
#     title = title.replace(" ","")
#     print title
#
#
# def readFromFile(fileName):
#     fileNameSet = set()
#     with open(fileName, "rb") as fread:
#         for index, line in enumerate(fread):
#             with open() as fwrite:
#                 if index > 200:
#                     break;
#     return fileNameSet

proxyList = []
cookieSet = {}

class spiderWithProxy():
    def __init__(self):
        self.con = redis.Redis(host="192.168.1.100",port=6379,db=1)
        self.redis_pipline = self.con.pipeline()
        self.dbsize = 0
        self.baseUrl = "https://www.amazon.com/dp/"

    def get_db_size(self):
        self.redis_pipline.dbsize()
        self.dbsize = self.redis_pipline.execute()[0]
        print self.dbsize

    def getHtml(self):
        for i in range(0, 1):
            print i
            self.redis_pipline.smembers(i)
            resSet = self.redis_pipline.execute()[0]
            with open("data/" + str(i)+".csv" , "wb+") as f:
                csvHeader = ["id", "html"]
                f_csv = csv.writer(f)
                f_csv.writerow(csvHeader)
                for j, productID in enumerate(resSet):
                    if j == 500:
                        break
                    url = self.baseUrl + productID
                    flag = True
                    while flag:
                        try:
                            proxy = self.getProxy()
                            print "current ip" + proxy
                            res = requests.get(url, headers=get_header(), proxies={"http": proxy})
                            print res.status_code
                            if res.status_code != 200 or self.checkRobot(res.content):
                                deleteIP(proxy)
                                print proxy+"has been deleted"
                                continue
                            row = []
                            row.append(productID)
                            row.append(res.content)
                            f_csv.writerow(row)
                            flag = False
                        except Exception as e:
                            print "here"+str(e.message)
                            break




    def checkRobot(self, text):
        soup = BeautifulSoup(text,"lxml")
        title = soup.find("title",attrs={"dir":"ltr"})
        if title is None:
            return False
        else:
            return True



    def getProxy(self):
        return random.choice(proxyList)

    def initProxyList(self):
        global proxyList
        proxyTempList = getProxyList("0","100","国内")
        for item in proxyTempList:
            proxyList.append("http://"+item[0]+":"+item[1])
        for item in proxyList:
            print item

    def deleteIP(self,ip):
        proxyList.remove(ip)
        ip = ""+ip
        ip = ip.split(r"//")[1]
        ip = ip.split(":")[0]
        requests.get("http://127.0.0.1:8000/delete?ip="+ip)





def deleteIP():
    proxyTemp = getProxyList("0","100","国内")
    print "删除前"
    print len(proxyTemp)
    for item in proxyTemp:
        print item[0]
    # for item in proxyTemp:
    #     s = requests.session()
    #     s.keep_alive = False
    #     s.get("http://127.0.0.1:8000/delete?id="+item[0])
    # proxyTemp = getProxyList("0", "100", "国内")
    # print "新获取"
    # for item in proxyTemp:
    #     print item[0]


# def piderWithProxy():
#     con = redis.Redis(host="192.168.1.100",port=6379,db=1)
#     redis_pipline = con.pipeline()
#     redis_pipline.smembers("0")
#     resSet = redis_pipline.execute()
    # for index, key in enumerate(keys):
    #     print key,"\r\n"
    #     if index >10:
    #         break
    # r =requests.get(url="http://ip111.cn/",headers = config.get_header(),proxies=proxy )
    # print r.content
def getRandCookie():
    global cookieSet
    length = len(cookieSet)
    print "cookie len"+str(length)
    choice = random.randint(0,length)
    for i, item in cookieSet:
        if i == choice:
            return item



if __name__ == "__main__":
    spider = spiderWithProxy()
    spider.get_db_size()
    spider.initProxyList()
    spider.getHtml()
    #deleteIP()

