# -*- coding: utf-8 -*-
from multiprocessing import Pool
import threading
import Queue
import requests
import time
import re

proxyList = []
# class reader(threading.Thread):
#     def __init__(self,queue):
#         threading.Thread.__init__(self)
#         self.thread_stop = False
#         self.q = queue
#
#     def run(self):
#         with open("D:\\tools\\test.txt", "rb") as f:
#             while not self.thread_stop:
#                 time.sleep(1)
#                 print "read"
#                 try:
#                     for line in f:
#                         self.q.put(line)
#                         print line
#                     self.thread_stop = True
#                     print "read end"
#                 except:
#                     print "read error"
#                     self.thread_stop = True
#
#     def stop(self):
#         self.thread_stop = True
#
#
# class writer(threading.Thread):
#     def __init__(self,queue):
#         threading.Thread.__init__(self)
#         self.q=queue
#         self.thread_stop = False
#         self.pos = 0
#
#     def run(self):
#         with open("D:\\tools\\movies_form.txt", "wb") as f:
#             while not self.thread_stop :
#                 time.sleep(1)
#                 print "write"
#                 try:
#                     task1 = self.q.get()
#                     task2 = self.q.get()
#                     print task1+"  "+task2
#                     f.write(task1+task2)
#                     if(q.task_done()):
#                         print "task done"
#                         self.thread_stop = True
#                 except:
#                     print "write error"
#                     self.thread_stop=True
#
#     def stop(self):
#         self.thread_stop = True
def trans(file1, file2):
    productId = re.compile(r'(product/productId *):(.*)')
    userId = re.compile(r'(review/userId *):(.*)')
    with open(file1, "rb") as fr:
        with open(file2, "wb") as fw:
            for index, line in enumerate(fr):
                objSearch = productId.search(line)
                # if index == 100:
                #     return
                if objSearch:
                    fw.write(objSearch.group(2)+'\r\n')
                else:
                    objSearch = userId.search(line)
                    if objSearch:
                        fw.write(objSearch.group(2)+'\r\n')





def lineCount(fileName):
    lineIndex = 0
    with open(fileName, "rb") as f:
        for index, line in enumerate(f):
            lineIndex = index
            #print index, line
        print lineIndex


def getProxy(url):
    res = requests.get(url)
    return res.text

def toList(proxyStr):
    pattern  = re.compile(r'"(\d*\.\d*\.\d*\.\d*)", (\d*), (\d*)')
    result = pattern.findall(proxyStr)
    for item in result:
        proxyList.append(item)
    return proxyList

def getProxyList(type,count,country):
    url = "http://127.0.0.1:8000/?type="+type+"&count="+count+"&country"+country;
    proxyStr = getProxy(url)
    proxyList = toList(proxyStr)
    return proxyList



if __name__ == "__main__":
    pass
    # proxyStr = getProxy("0","100","国内")
    # print proxyStr
    # proxyList = toList(proxyStr)
    # for item in proxyList:
    #     print item
