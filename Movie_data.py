# !/usr/bin/python
# -*- coding: utf-8 -*-
import json, urllib
from urllib.parse import urlencode
import urllib.request


# ----------------------------------
# 影视影讯检索调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/94
# ----------------------------------

def main():
    # 配置您申请的APPKey
    appkey = "eed0f5e86182a5e15ceb8534ef8d54b3"

    # 1.影视搜索
    request1(appkey, "GET")

    # 2.最近影讯
    request2(appkey, "GET")


# 影视搜索
def request1(appkey, m="GET"):
    url = "http://v.juhe.cn/movie/index"
    params = {
        "title": "爱",
        "key": appkey,  # 应用APPKEY(应用详细页查询)
        "dtype": "json",  # 返回数据的格式,xml或json，默认json
        "q": "",  # 影视搜索名称

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        print("request api error")


# 最近影讯
def request2(appkey, m="GET"):
    url = "http://op.juhe.cn/onebox/movie/pmovie"
    params = {
        "key": appkey,  # 应用APPKEY(应用详细页查询)
        "dtype": "",  # 返回数据的格式,xml或json，默认json
        "city": "",  # 城市名称

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.request.urlopen(url, params)

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print(res["result"])
        else:
            print("%s:%s" % (res["error_code"], res["reason"]))
    else:
        print("request api error")


if __name__ == '__main__':
    main()