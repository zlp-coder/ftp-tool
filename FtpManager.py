#coding=utf-8
# encoding=utf8
from enum import Enum
from ftplib import FTP
import paramiko
import json
import datetime
import os.path
import os
import shutil

class FtpManager():
    '''Ftp 服务封装'''

    def __init__(self, parent):
        self.pw=parent

        self.ftpId=""
        self.type="ftpport"
        self.ftpHost = ""
        self.ftpPort = "21"
        self.ftpUser = ""
        self.ftpPsw = ""

        self.status = ""

        self.noopLastData = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.noopStep = 5 #s

    def CheckConn(self):
        try:
            if (self.type == "ftppasv"):
                self.ftpsrv = ftp = FTP()
                ftp.set_pasv(True)
                ftp.set_debuglevel(2)
                ftp.connect(self.ftpHost, str(self.ftpPort))
                ftp.login(self.ftpUser, self.ftpPsw)
                ftp.encoding = 'utf-8'

            if (self.type == "ftpport"):
                self.ftpsrv = ftp = FTP()
                ftp.connect(self.ftpHost, str(self.ftpPort))
                ftp.login(self.ftpUser, self.ftpPsw)
                ftp.encoding = 'utf-8'
                ftp.set_debuglevel(2)
                print ftp.getwelcome()

            if (self.type == "sftp"):
                transport = paramiko.Transport((self.ftpHost, int(self.ftpPort)))
                transport.connect(username=self.ftpUser, password=self.ftpPsw)
                self.ftpsrv = sftp = paramiko.SFTPClient.from_transport(transport)

            self.status = "ready"
        except Exception as ex:
            self.status = "error" + ex.message

    def CLose(self):
        if self.type == "ftpport" or self.type == "ftppasv":
            self.ftpsrv.close()
            self.ftpsrv.quit()

        if self.type == "sftp":
            self.ftpsrv.close()

    def CheckPath(self, strPath):
        if self.type == "ftpport" or self.type == "ftppasv":
            if self.ftpsrv > 0:
               print(self.ftpsrv.cwd(strPath))

        if self.type == "sftp":
            if self.ftpsrv > 0:
                print(self.ftpsrv.listdir(strPath))

    def Noop(self):
        d1 = datetime.datetime.strptime(self.noopLastData, "%Y-%m-%d %H:%M:%S") if len(self.noopLastData) > 0 else datetime.datetime(1900, 1, 1)
        d2 = datetime.datetime.now()
        step = self.noopStep

        if (d2 - d1).seconds > step:
            try:
                self.noopLastData = datetime.datetime. now().strftime("%Y-%m-%d %H:%M:%S")

                if self.type == "ftpport" or self.type == "ftppasv":
                    self.pw.ShowMsg(u"FTP连接维持：" + self.ftpId)
                    print(self.ftpsrv.voidcmd('NOOP'))

                if self.type == "sftp":
                    self.pw.ShowMsg(u"SFTP连接维持：" + self.ftpId)
                    print(self.ftpsrv.get_channel())
            except Exception as ex:
                self.CheckConn()

    def UploadTask(self, item):
        try:
            item["lastDate"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item["runningState"] = u"运行中"
            self.pw.RefreshUploadList()
            self.pw.cfgManager.saveConfigFile()

            if os.path.exists(item["localPath"]) == False:
                raise Exception( u"目录不存在:" + item["localPath"])

            for root, dirs, files in os.walk(item["localPath"]):
                for f in files:
                    if self.type == "ftpport" or self.type == "ftppasv":
                        bufsize = 1024

                        self.ftpsrv.cwd(item["srvPath"])
                        with open(os.path.join(root, f), 'rb') as fbyte:
                            self.ftpsrv.storbinary("STOR %s" % f.encode("utf-8"), fbyte, bufsize)

                        if item["afterOprt"] == "cc":
                            self.ftpsrv.cwd(item["ccsrvPath"])
                            with open(os.path.join(root, f), 'rb') as fbyte:
                                self.ftpsrv.storbinary("STOR %s" % f.encode("utf-8"), fbyte, bufsize)

                    if self.type == "sftp":
                        self.ftpsrv.put(os.path.join(root, f), item["srvPath"] + "/" + f)

                    shutil.move(os.path.join(root, f) , os.path.join(item["bakPath"], f))
                    self.pw.ShowMsg(u"任务：" + item["taskName"] + u"上传文件成功：" + f)

            item["runningState"] = u"等候"
            self.pw.RefreshUploadList()

        except Exception as ex:
            print ex
            item["runningState"] = u"等候"
            if self.pw != 0:
                self.pw.RefreshUploadList()
                self.pw.cfgManager.saveConfigFile()
                self.pw.ShowMsg(u"[ERROR] 任务异常：(" + item["taskName"] + u") 运行异常:"  + ex.message)

    def DownTask(self, item):
        try:
            item["lastDate"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item["runningState"] = u"运行中"
            self.pw.RefreshUploadList()
            self.pw.cfgManager.saveConfigFile()

            if self.type == "ftpport" or self.type == "ftppasv":
                self.ftpsrv.cwd(item["srvPath"])
                for file in self.ftpsrv.nlst():
                    f =  os.path.join(item["localPath"] , unicode(file,"utf-8"))
                    f2 = item["srvPath"]+ u"/" + unicode(file,"utf-8")

                    with open(f , "wb") as fdown:
                        self.ftpsrv.retrbinary("RETR " +  f2, fdown.write , 10240)
                        fdown.close()

                    self.ftpsrv.delete(f2)
                    self.pw.ShowMsg(u"任务：" + item["taskName"] + u"下载文件成功：" + file)

                    if "cc" in item["afterOprt"]:
                        if os.path.exists(item["ccsrvPath"]) == False:
                            os.mkdir(item["ccsrvPath"])

                        shutil.copy( os.path.join(item["localPath"],file), os.path.join(item["ccsrvPath"], file ))

                    if "temp" in item["afterOprt"]:
                        if os.path.exists(item["tempsrvPath"]) == False:
                            os.mkdir(item["tempsrvPath"])
                        shutil.move( os.path.join(item["localPath"],file), os.path.join(item["tempsrvPath"], file ))

            if self.type == "sftp":
                for file in self.ftpsrv.listdir(item["srvPath"]):
                    remoteDirTmp = item["srvPath"] + "/" + file
                    localDirTmp = os.path.join(item["localPath"], file)

                    print remoteDirTmp
                    print localDirTmp

                    self.ftpsrv.get(remoteDirTmp , localDirTmp)
                    self.ftpsrv.remove(remoteDirTmp)

                    self.pw.ShowMsg(u"任务：" + item["taskName"] + u"下载文件成功：" + file)

                    if "cc" in item["afterOprt"]:
                        shutil.copy( os.path.join(item["localPath"],file), os.path.join(item["ccsrvPath"], file ))

                    if "temp" in item["afterOprt"]:
                        shutil.move( os.path.join(item["localPath"],file), os.path.join(item["tempsrvPath"], file ))


        except Exception as ex:
            print ex
            item["runningState"] = u"等候"
            if self.pw != 0:
                self.pw.RefreshUploadList()
                self.pw.cfgManager.saveConfigFile()
                self.pw.ShowMsg(u"[ERROR] 任务异常：(" + item["taskName"] + u") 运行异常:"  + ex.message)


#
# try:
#     t =FtpManager(0)
#     t.ftpHost = "192.168.245.128"
#     t.type=FtpType.sftp
#     t.ftpPort=22
#     t.ftpUser = "g30psftp"
#     t.ftpPsw = "111111"
#     t.CheckConn()
#     t.CheckPath("/")
# except Exception as e:
#     print(e)
