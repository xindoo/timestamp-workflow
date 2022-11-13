前两天换了新款的macbook，也不知道是不是因为m1芯片的原因，系统没有自带php，导致我之前使用的时间戳转换workflow失效了。作为一个后端工程师，时间戳互转的功能还是非常常用了，于是还折腾修复了下，手动安装php后可能是因为php版本的原因，依旧无法使用，心想还是算了 不折腾了，原来那个也不是很好用，干脆自己用python写一个。   

先说下我这个workflow实现的几个功能：
1. 可以获取当前的时间，支持获取秒级时间戳，毫秒级时间戳，以及`yyyy-MM-dd`和`yyyy-MM-dd HH:mm:ss`的日期格式。 
![在这里插入图片描述](https://img-blog.csdnimg.cn/a2f51e67db1f493d85a8f561331c230b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAeGluZG9v,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
2. 可以将秒级或者毫秒级的时间戳转为`yyyy-MM-dd`和`yyyy-MM-dd HH:mm:ss`的日期格式。![在这里插入图片描述](https://img-blog.csdnimg.cn/4b0dee644258499b894855a9c64c302b.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAeGluZG9v,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)
3. 当然也可以将`yyyy-MM-dd`和`yyyy-MM-dd HH:mm:ss`格式的日期转为秒级和毫秒级的时间戳。
![在这里插入图片描述](https://img-blog.csdnimg.cn/f4b8afcd4ef74245b91a822cecd27a42.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAeGluZG9v,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center)

下文将很具体的教授大家如何实现上述功能，相信以大家的学习能力，很快也能写出其他。如果不想写，文末附上了下载链接，你可以直接拿去使用。 

我们首先来看下Alfred workflow所要求的输出数据格式，使用json或者xml都可以，其中title和subtitle字段用做展示，我这里只使用了title字段。arg字段是用来像下一级的workflow传递参数的，如果你的workflow单纯是为了展示，可以不需要这个。我这里经常需要将结果复制到粘贴板中，所以在后面接了一个Copy to clipboard模块，所以arg参数就是必要的了。  

```json
{
  "items": [
    {
      "arg": 1645346653,
      "valid": true,
      "subtitle": "",
      "uid": "s",
      "title": "\u79d2: 1645346653"
    },
    {
      "arg": "1645346653000",
      "valid": true,
      "subtitle": "",
      "uid": "ms",
      "title": "\u6beb\u79d2: 1645346653000"
    },
    {
      "arg": "2022-02-20",
      "valid": true,
      "subtitle": "",
      "uid": "date",
      "title": "\u65e5\u671f: 2022-02-20"
    },
    {
      "arg": "2022-02-20 16:44:13",
      "valid": true,
      "subtitle": "",
      "uid": "datetime",
      "title": "\u65f6\u95f4: 2022-02-20 16:44:13"
    }
  ]
}
```
实际上，你用任何方式生成上面格式的json串，都可以用来实现一个新的workflow，不限于任何语言。 所以你可以看到alfred的workflow可以使用各种语言去写。

关于时间戳转化的workflow逻辑就很简单了，就是根据入参生成各种格式的日期数据，然后将起以上文的json格式输出，完整代码如下：
```python
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
    elif re.match(r"\d+-\d+-\d+", query):
        ts = time.mktime(time.strptime(query, '%Y-%m-%d'))
        getTime(int(ts))
    elif re.match(r"\d+", query):
        ts = int(query)
        if ts > 253402185600:
            ts = ts/1000 
        getTime(ts)
```
在Alfred的配置如下：
![在这里插入图片描述](https://img-blog.csdnimg.cn/5513e5ce5dda44f2a642244c9a248138.png?x-oss-process=image/watermark,type_d3F5LXplbmhlaQ,shadow_50,text_Q1NETiBAeGluZG9v,size_20,color_FFFFFF,t_70,g_se,x_16#pic_center =700x)
最后附上Workflow的下载链接: [https://pan.baidu.com/s/1PVS9XvKe-2fle2ZrreCWPA?pwd=ukd8](https://pan.baidu.com/s/1PVS9XvKe-2fle2ZrreCWPA?pwd=ukd8 ) 提取码: ukd8 

### 2022-10-30补充
因为我在workflow里写死了python的路径，所以大家下载后可能无法使用，需要手动更改为你自己电脑上的python安装路径，如下图：
![在这里插入图片描述](https://img-blog.csdnimg.cn/b4c7e4e9816642d483ff92c445677216.jpeg#pic_center)  

代码已开源到github [https://github.com/xindoo/timestamp-workflow](https://github.com/xindoo/timestamp-workflow)