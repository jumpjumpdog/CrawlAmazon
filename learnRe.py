# -*- coding: utf-8 -*-
import re




def reFunc(str):
    matchObj = re.search(r'(.*?) *:(.*)' ,testStr)
    if matchObj:
        print matchObj.group(2)
    else:
        print "no match"+matchObj.group(0)

if __name__ == "__main__":
    reFunc(testStr)