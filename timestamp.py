# -*- coding: utf-8 -*-  
import sys
import time
import datetime
import re

from workflow import Workflow3

def getTime(ts):
    wf = Workflow3()
    s = ts
    timeArray = time.localtime(ts)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    ms = str(ts*1000)
    wf.add_item(uid = "s", title = "秒: "+str(s), arg=s, valid = True)
    wf.add_item(uid = "ms", title = "毫秒: "+str(ms), arg=ms,  valid = True)
    wf.add_item(uid = "date", title = "日期: "+time.strftime("%Y-%m-%d", timeArray), arg=time.strftime("%Y-%m-%d", timeArray),  valid = True)
    wf.add_item(uid = "datetime", title = "时间: "+time.strftime("%Y-%m-%d %H:%M:%S", timeArray), arg=time.strftime("%Y-%m-%d %H:%M:%S", timeArray),  valid = True)
    wf.send_feedback()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        ts = time.time()
        getTime(int(ts)) 
        exit(0)

    query = sys.argv[1]
    # print(query) 
    if query == 'now':
        ts = time.time()
        getTime(int(ts))
    elif re.match(r"\d+-\d+-\d+ \d+:\d+:\d+", query):
        ts = time.mktime(time.strptime(query, '%Y-%m-%d %H:%M:%S'))
        getTime(int(ts))
    elif re.match(r"\d+:\d+:\d+", query):
        ts = time.mktime(time.strptime(query, '%H:%M:%S'))
        getTime(int(ts))
    elif re.match(r"\d+-\d+-\d+", query):
        ts = time.mktime(time.strptime(query, '%Y-%m-%d'))
        getTime(int(ts))
    elif re.match(r"\d+", query):
        ts = int(query)
        if ts > 253402185600:
            ts = ts/1000 
        getTime(ts)
     
