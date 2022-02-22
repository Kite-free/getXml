import requests
import json
#发送get请求，json格式的文件自动转成列表
def get(url):
    headers = {    # 模拟浏览器头部信息，向服务器发送消息
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    res = requests.get(url,headers=headers)
    res.encoding = "utf-8"
    isJson = True if "application/json" in res.headers["Content-Type"] else False
    if isJson:
        return json.loads(res.text)
    else:
        return res.text