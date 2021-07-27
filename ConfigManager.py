#coding=utf-8

import json
import codecs
import os.path
import uuid

from FtpManager import *


class ConfigManager:
    '''配置文件的读写管理类'''

    mPath = ""
    mConfigFileName = "ftpclient_cfg.json"
    mfileDatetime = ""

    def __init__(self, pmainw):
        self.pw = pmainw
        self.loadConfigFile()
        self.mPath = os.getcwd() + "\\" + self.mConfigFileName

    def loadConfigFile(self):
        fPath = os.getcwd() + "\\" + self.mConfigFileName
        # if self.pw > 0:
        #     self.pw.ShowMsg("配置文件路径:" + fPath)

        if os.path.exists( fPath) == False :
            with open(fPath,'w') as ftmp:
                ftmp.write(self.getTemplat())
                if self.pw > 0:
                    self.pw.ShowMsg(u"找不到配置文件，使用默认模版重新创建一份新的配置文件......")

        with codecs.open(fPath, "r", encoding='utf-8') as f:
            self.cfg = json.loads(f.read())
            self.fileDatetime = os.path.getmtime(fPath)

    def saveConfigFile(self):
        fPath = os.getcwd() + "\\" + self.mConfigFileName
        with codecs.open(fPath, "w",  encoding='utf-8') as f:
            f.write(json.dumps(self.cfg))

    def readUploadList(self):
        '''获取上传任务列表'''
        if not self.cfg:
            return []
        return self.cfg["uploadtask"]

    def readDownloadList(self):
        '''获取下载任务列表'''
        if not self.cfg:
            return []
        return self.cfg["downloadtask"]

    def readFtpList(self):
        '''获取连接列表'''
        if not self.cfg:
            return []
        return self.cfg["ftpList"]

    def checkFtp(self, ftpObject):
        print(ftpObject["ftpId"])

    def delFtpFormList(self, ftpId):
        #todo: conn in using need check
        for i,item in enumerate(self.cfg["ftpList"]):
            if(item["ftpId"] == ftpId):
                del self.cfg["ftpList"][i]
                self.saveConfigFile()
                return

    def addFtpFormList(self,data):
        try:
            find = False
            for i,item in enumerate(self.cfg["ftpList"]):
                if item["ftpId"] == data["ftpId"]:
                    self.cfg["ftpList"][i] = data
                    find = True
                    break

            if find == False:
                self.cfg["ftpList"].append(data)
        except Exception as ex:
            print(ex.message)
        else:
            self.saveConfigFile()

    def delUpTaskList(self, seq):
        for i,item in enumerate(self.cfg["uploadtask"]):
            if(item["seq"] == seq):
                del self.cfg["uploadtask"][i]
                self.saveConfigFile()
                return

    def delDownTaskList(self, seq):
        for i,item in enumerate(self.cfg["downloadtask"]):
            if(item["seq"] == seq):
                del self.cfg["downloadtask"][i]
                self.saveConfigFile()
                return

    def addUpTaskList(self,data):
        try:
            find = False
            for i,item in enumerate(self.cfg["uploadtask"]):
                if item["seq"] == data["seq"]:
                    self.cfg["uploadtask"][i] = data
                    find = True
                    break

            if find == False:
                self.cfg["uploadtask"].append(data)
        except Exception as ex:
            print(ex.message)
        else:
            self.saveConfigFile()

    def delDonwTaskList(self, seq):
        for i,item in enumerate(self.cfg["downloadtask"]):
            if(item["seq"] == seq):
                del self.cfg["downloadtask"][i]
                self.saveConfigFile()
                return

    def addDownTaskList(self,data):
        try:
            find = False
            for i,item in enumerate(self.cfg["downloadtask"]):
                if item["seq"] == data["seq"]:
                    self.cfg["downloadtask"][i] = data
                    find = True
                    break

            if find == False:
                self.cfg["downloadtask"].append(data)
        except Exception as ex:
            print(ex.message)
        else:
            self.saveConfigFile()

    def getConnDropDownUpload(self):
        sampleList = []
        for i, item in enumerate(self.readFtpList()):
            for j, detail in enumerate(item["upload"]):
                s = item["ftpType"] + "://" + item["ftpUser"] + "@" + item["ftpHost"] + \
                    ":" + item["ftpPort"] + " (" +  detail["localPath"] + "=>" + detail["srvPath"] +\
                    ") #" + detail["bakPath"] + " [id=" + item["ftpId"] + "]"

                sampleList.append(s)

        return sampleList

    def getConnDropDownDownLoad(self):
        sampleList = []
        for i, item in enumerate(self.readFtpList()):
            for j, detail in enumerate(item["download"]):
                s = item["ftpType"] + "://" + item["ftpUser"] + "@" + item["ftpHost"] + \
                    ":" + item["ftpPort"] + " (" +  detail["srvPath"] + "=>" + detail["localPath"] +\
                    ") " + "[id=" + item["ftpId"] + "]"

                sampleList.append(s)

        return sampleList

    def checkConfigModify(self):
        if self.fileDatetime != os.path.getmtime(self.mPath):
            self.loadConfigFile()

    def getAllBufferConn(self):
        #获取所有的设置为需要缓存的连接
        conns ={}

        for i, item2 in enumerate(self.readUploadList()):
            for i, item in enumerate(self.readFtpList()):
                if  item2["ftpId"] == item["ftpId"] and item["usingPool"] == "true" :
                    obj = FtpManager(self.pw)
                    obj.ftpId = item["ftpId"]
                    obj.type = item["ftpType"]
                    obj.ftpHost = item["ftpHost"]
                    obj.ftpPort = item["ftpPort"]
                    obj.ftpUser = item["ftpUser"]
                    obj.ftpPsw = item["ftpPsw"]
                    obj.CheckConn()
                    conns[item["ftpId"]] = obj

        for i, item2 in enumerate(self.readDownloadList()):
            for i, item in enumerate(self.readFtpList()):
                if  item2["ftpId"] == item["ftpId"] and item["usingPool"] == "true" :
                    obj = FtpManager(self.pw)
                    obj.ftpId = item["ftpId"]
                    obj.type = item["ftpType"]
                    obj.ftpHost = item["ftpHost"]
                    obj.ftpPort = item["ftpPort"]
                    obj.ftpUser = item["ftpUser"]
                    obj.ftpPsw = item["ftpPsw"]
                    obj.CheckConn()
                    conns[item["ftpId"]] = obj

        return conns

    def getTemplat(self):
        return """{
   "id" : "Demo01",
   "address" : "演示连接192.168.25.26",
   "runReboot" : "false",
   "runReboottime" : "",
   "runRebootDuring" : "",
   "runRebootDuringHours" : "",
   "runRebootOnError" : "",
   "runRebootOnErrorList" : "",
   "statusReport" : "300",
   "statusReportLastTime" : "",
   "ftpList" : [
      {
         "ftpId" : "9f2d1b60-42d1-4b59-95e0-c6b54f1a6f96",
         "ftpType" : "ftpport",
         "ftpHost" : "127.0.0.1",
         "ftpPort" : "21",
         "ftpUser" : "root",
         "ftpPsw" : "111111",
         "usingPool" : "true",
         "upload" : [
            {
               "localPath" : "d:\\\\temp",
               "srvPath" : "/yict01",
               "bakPath" : "d:\\\\back"
            }
         ],
         "download" : [
            {
               "localPath" : "d:\\\\download",
               "srvPath" : "/yict02"
            }
         ]
      }
   ],
   "uploadtask" : [
      {
         "seq" : "21935ebd-0c48-477b-a5d6-4bb9af8dfa06",
         "order" : "10",
         "taskName" : "演示上传任务配置",
         "taskDesc" : "这是演示数据，请使用前删除或变更为正式配置",
         "localPath" : "d:\\\\temp",
         "filterFilename" : "",
         "filterContent" : "",
         "srvPath" : "/temp",
         "bakPath" : "d:\\\\back",
         "afterOprt" : "cc",
         "ccsrvPath" : "/temp001",
         "status" : "1",
         "ftpId" : "9f2d1b60-42d1-4b59-95e0-c6b54f1a6f96",
         "ftpIdDisp" : "",
         "transFiles" : "10000",
         "transRun" : "60",
         "isPsd" : "1",
         "runningState" : "等候",
         "lastDate" : ""
      }
   ],
   "downloadtask" : [
      {
         "seq" : "7022e37e-4ea3-4079-939a-ce28078a013d",
         "order" : "10",
         "taskName" : "演示下载任务配置",
         "taskDesc" : "这是演示数据，请使用前删除或变更为正式配置",
         "srvPath" : "/down",
         "filterFilename" : "",
         "filterContent" : "",
         "localPath" : "d:\\\\download",
         "afterOprt" : "cc|temp",
         "ccsrvPath" : "/download2",
         "tempsrvPath" : "d:\\\\download2",
         "status" : "1",
         "ftpId" : "9f2d1b60-42d1-4b59-95e0-c6b54f1a6f96",
         "ftpIdDisp" : "",
         "transFiles" : "10000",
         "transRun" : "60",
         "runningState" : "等候",
         "lastDate" : ""
      }
   ]
}"""

