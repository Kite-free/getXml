import sys
from lib.getBilibiliXmlFile import GetBilibiliXml

def parseArgs(argv):
    argvLength = (len(argv)-1)
    print(argvLength)
    if argvLength%2 != 0:
        print("The command line input is incorrect!")
        print("example: python xx.py -i input_path -o output_path")
        sys.exit()
    print(argvLength)
    List = argv[1:]
    argList = {}
    for i in range(int(argvLength/2)):
        List[2*i] = List[2*i].replace("-","")
        argList[List[2*i]] = List[2*i+1]
    return argList

if __name__ == "__main__":
    argList = parseArgs(sys.argv)
    try:
        if len(argList)==0:
           inputFile = input("请输入需要加载的链接文件路径：")
           outputFile = input("请输入下载的弹幕文件夹路径：")        
        elif "i" in argList and "o" not in argList:
            #下载文件默认输出文件夹
            outputFile = "./xmls/" 
        else:
            inputFile = argList["i"]
            outputFile = argList["o"]
    except:
        print("The command line input is incorrect!")
        print("example: python xx.py -i input_path -o output_path")
        sys.exit()
    else:
        if outputFile[-1] != "/":
            outputFile +="/"
            print(f"outputFile:{outputFile}")

    downloadXml = GetBilibiliXml().readListToDownload
    fileInputPath = inputFile
    xmlOutputPath = outputFile
    downloadXml(fileInputPath,outputFile)
