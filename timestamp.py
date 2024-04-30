# -*- coding: utf-8 -*-  
import sys
import time
import re
import json


class AlfredItems:
    def __init__(self):
        self.items = []

    def add_item(self, uid = '', title = '', subtitle = '', arg = '', valid = True, icon_path = ''):
        """添加一个新的条目到项目列表中"""
        item = {
            "uid": uid,
            "title": title,
            "subtitle": subtitle,
            "arg": arg,
            "icon": {
                "path": icon_path
            }
        }
        self.items.append(item)

    def to_json(self):
        """生成包含所有条目的 JSON 字符串"""
        return json.dumps({"items": self.items}, indent=4)

def getTime(ts, delta=None):
    wf = AlfredItems()
    s = ts
    timeArray = time.localtime(ts)
    
    if delta:
        ts += delta
        timeArray = time.localtime(ts)
    ts = int(ts)
    ms = str(ts*1000)
    wf.add_item(uid = "s", title = "秒: "+str(s), arg=s, valid = True)
    wf.add_item(uid = "ms", title = "毫秒: "+str(ms), arg=ms,  valid = True)
    wf.add_item(uid = "date", title = "日期: "+time.strftime("%Y-%m-%d", timeArray), arg=time.strftime("%Y-%m-%d", timeArray),  valid = True)
    wf.add_item(uid = "datetime", title = "时间: "+time.strftime("%Y-%m-%d %H:%M:%S", timeArray), arg=time.strftime("%Y-%m-%d %H:%M:%S", timeArray),  valid = True)
    print(wf.to_json())


if __name__ == '__main__':
    if len(sys.argv) == 1:
        ts = time.time()
        getTime(int(ts)) 
        exit(0)

    query = sys.argv[1]
    delta = 0
    
    if query.endswith('d'):
        days = int(query[:-1])
        delta = days * 24 * 60 * 60
        query = query[:-2].strip()
    elif query.endswith('h'):
        hours = int(query[:-1])
        delta = hours * 60 * 60
        query = query[:-2].strip()
    elif query.endswith('m'):
        minutes = int(query[:-1])
        delta = minutes * 60
        query = query[:-2].strip()
    elif query.endswith('w'):
        weeks = int(query[:-1])
        delta = weeks * 7 * 24 * 60 * 60
        query = query[:-2].strip()
    
    if query == 'now':
        ts = time.time()
        getTime(int(ts))
    elif re.match(r"\d+-\d+-\d+ \d+:\d+:\d+", query):
        ts = time.mktime(time.strptime(query, '%Y-%m-%d %H:%M:%S'))
        getTime(int(ts))
    elif re.match(r"\d+:\d+:\d+", query):
        ts = time.mktime(time.strptime(query, '%Y-%m-%d %H:%M:%S'))
        getTime(int(ts))
    elif re.match(r"\d+-\d+-\d+", query):
        ts = time.mktime(time.strptime(query, '%Y-%m-%d'))
        getTime(int(ts))
    elif re.match(r"\d+", query):
        ts = int(query)
        if ts > 253402271999: 
            ts = ts/1000 
        getTime(ts)
    elif delta != 0:
        ts = time.time()
        getTime(ts, delta)
