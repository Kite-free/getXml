import json
import re
from get import get

ruleArr = ["BV[A-Za-z0-9]{10}/?$","ss[0-9]{5}/?$","ep[0-9]{6}/?$"]
class GetCid:
    def __init__(self,ruleArr):
        self.ruleArr = ruleArr
    #输入含有aid的Url获取该aid视频的标题
    def aidToTopic(self,aidUrl):
        res = get(aidUrl)
        res = res["data"]["title"].split(" ")[0]
        return res 

    #根据数字进行相应的正则匹配，返回需要的部分
    def reg(self,num,url):
        url = url.split("?")
        url = url[0]
        result = re.findall(self.ruleArr[num],url)
        return result[0].replace("/","") if result != [] else False

    # 核心函数：根据不同的Url种类获取cid和对应的title信息
    def getCid(self,url):
        if self.reg(0,url):
            bid = self.reg(0,url)
            getCidUrl = "https://api.bilibili.com/x/web-interface/view?bvid="+bid
            inform = get(getCidUrl)
            Obj = {"cid":[inform["data"]["cid"]],"title":[inform["data"]["title"]]}
            return Obj        
        elif self.reg(1,url):
            ss = self.reg(1,url)
            ss = ss.replace("ss","")
            getCidUrl = "https://api.bilibili.com/pgc/web/season/section?season_id="+ss
            inform = get(getCidUrl)
            inform = inform["result"]["main_section"]["episodes"]
            length = len(inform) 
            cidArr = []
            titleArr = []
            for i in range(length):
                cidArr.append(inform[i]["cid"])
                titleArr.append(inform[i]["long_title"])
            aid =  inform[0]["aid"]
            aidUrl = "https://api.bilibili.com/x/web-interface/view?aid="+str(aid)
            topic = self.aidToTopic(aidUrl)  
            Obj = {"cid":cidArr,"title":titleArr,"topic":topic}
            return Obj
        elif self.reg(2,url):
            ep = self.reg(2,url)
            ep = ep.replace("ep","")
            epUrl = "https://www.bilibili.com/bangumi/play/ep%s"%ep
            res = get(epUrl)
            #求解ep_id对应的cid
            res = re.findall(r'__INITIAL_STATE__=(.*?);\(function\(\)',res)[0]
            res = json.loads(res)
            cid = res["initEpList"]
            counter = 0
            for list in cid:
                if list["loaded"] == True:
                    break
                counter += 1
            cid = res["mediaInfo"]["episodes"][counter]["cid"]
            #抓取ep_id对应的title
            title = res["h1Title"]
            title = title.replace(" ","")
            Obj = {"cid":[cid],"title":[title]}  
            return Obj
        else:
            return False

    