# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


headers =  {'User-Agent': "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate'}

def getContent(url):
    res = requests.get(url,headers=headers)
    return res

if __name__ == "__main__":
    result = ""
    for i in range(0,20):
        result = getContent("https://www.amazon.com/dp/B000QGE8ME")
        print result.status_code
        print result.content

    soup = BeautifulSoup(result.content,"lxml")
    print soup
