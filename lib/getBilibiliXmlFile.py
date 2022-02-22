import json
import os
from get import get
import re
from readFileError import ReadFileError

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

#根据GetCid类获取视频对应的cid和title
class GetBilibiliXml:
    #输入b站视频的url链接获取对应的xml文件
    #输入链接包含多种情况： 
    # ep号：下载对应的番剧弹幕
    # Bv_id:下载对应的视频弹幕
    # ss_id:下载对应番剧全集的弹幕文件，并存储在单独文件夹中    
    def getXml(self,url,xmlPath):
        getCid = GetCid(ruleArr).getCid
        inform = getCid(url)
        if inform == False:
            print("****输入Url错误，无法解析出弹幕xml!****")
            return False
        # print(inform)
        length = len(inform["cid"])
        for i in range(length):
            cid = inform["cid"][i]
            title = inform["title"][i].replace(" ","")
            getXmlUrl = "https://comment.bilibili.com/"+str(cid)+".xml"
            xml_data = get(getXmlUrl)
            # byte = data.encode("iso-8859-1")
            # xml_data = byte.decode("utf-8")
            if length>1:
                file_dir = xmlPath+inform["topic"]+"/"
                file_path = file_dir+str(i+1)+"."+title+".xml"
            else:
                file_dir = xmlPath
                file_path = file_dir+title+".xml"
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            with open(file_path,"w",encoding="utf-8") as w:
                outputStart = str(i+1)+"."+"写入文件"+":《"+title+"》中..."
                outputEnd = str(i+1)+"."+"写入文件"+":《"+title+"》中...\n****************************************************"
                output = outputStart if i!=length-1 else outputEnd 
                print(output)
                w.write(xml_data)
                w.close()
    #解析输入的json文件路径为列表数据类型
    def parseJson(self,path):
        with open(path,'r') as load_f:
            load_dict = json.load(load_f) 
            load_f.close()
            return load_dict 
    #解析输入的txt文件路径为列表数据类型
    def parseTxt(self,path):
        with open(path,"r") as load_f:
            load_list = load_f.readlines()
            return load_list
    #获取输入路径字符串的文件类型
    def getFileType(self,path):
        if not os.path.exists(path):
            raise ReadFileError(0)
        if path[-1:]=='/':
            raise ReadFileError(1)
        fileType = path.split(".")
        fileType = fileType[-1]
        return fileType

    #输入文件路径字符串，逐行下载url对应视频的b站弹幕
    def readListToDownload(self,filePath,xmlPath):
        fileType = self.getFileType(filePath)
        if fileType == "json":
            lists = self.parseJson(filePath)
        elif fileType == "txt":
            lists = self.parseTxt(filePath)
        else:
            raise ReadFileError(2)
        for url in lists:
            self.getXml(url,xmlPath)
        return 
             

