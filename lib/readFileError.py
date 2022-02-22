class ReadFileError(Exception):
    def __init__(self,code):
        self.code = code
    def __str__(self):
        if self.code == 0:
            print("input path is not exist! error code is:%d"%(self.code))
        elif self.code == 1:
            print("Please enter a file path! error code is:%d"%(self.code))
        elif self.code == 2:
            print(f"The input file type is not supported. Only supported is json and txt,error code is:{self.code}")