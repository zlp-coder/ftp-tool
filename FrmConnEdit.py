#coding=utf-8

import wx
import wx.dataview as dataview
import wx.grid as gridlib
import uuid

from MainWindow import *
from FtpManager import *

class FrmConnEdit(wx.Dialog):

    def __init__(self, parent, ftpid=0):
        wx.Dialog.__init__(self, parent)
        self.pw=parent
        self.id = ftpid

        self.Title = "新增或者编辑一个具体的连接"
        self.SetSize(900, 800)
        self.Center()

        p = wx.Panel(self)
        gbs = self.gbs = wx.GridBagSizer(vgap=5, hgap=5)
        p.SetSizer(gbs)

        gbs.Add(wx.StaticText(p, -1, "连接ID*"), pos=(0,0),span = (1, 1), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border=5)
        self.mFtpId = wx.TextCtrl(p)
        self.mFtpId.SetEditable(False)
        gbs.Add(self.mFtpId, pos=(0, 1), span=(1, 7), flag=wx.EXPAND|wx.ALL, border=5)
        self.lbTest=wx.Button(p, wx.ID_HELP,"测试")
        gbs.Add(self.lbTest, pos=(0, 8), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
        gbs.AddGrowableCol(1)

        gbs.Add(wx.StaticText(p, -1, "服务器类型:") , pos = (1,0), span = (1, 1), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border=5)
        typeList = ['FTP主动','FTP被动','SFTP']
        self.mFtpType = wx.RadioBox(p, -1, "", wx.DefaultPosition, wx.DefaultSize,typeList, 3, wx.RA_SPECIFY_COLS|wx.NO_BORDER)
        gbs.Add(self.mFtpType, pos = (1,1), span = (1, 8), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "服务器地址*") , pos = (2,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mFtpHost = wx.TextCtrl(p)
        gbs.Add(self.mFtpHost, pos = (2,1), span = (1, 8), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "服务器端口") , pos = (3,0), span = (1, 1), flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border = 5 )
        self.mFtpPort = wx.TextCtrl(p)
        gbs.Add(self.mFtpPort, pos = (3,1), span = (1, 8), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "帐户") , pos = (4,0), span = (1, 1), flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border = 5 )
        self.mFtpUser = wx.TextCtrl(p)
        gbs.Add(self.mFtpUser, pos = (4,1), span = (1, 8), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "密码") , pos = (5,0), span = (1, 1), flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border = 5 )
        self.mFtpPsw = wx.TextCtrl(p, style=wx.TE_PASSWORD)
        gbs.Add(self.mFtpPsw, pos = (5,1), span = (1, 8), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "保持FTP长连接") , pos = (6,0), span = (1, 1), flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border = 5 )
        self.mUsingPool = wx.CheckBox(p)
        gbs.Add(self.mUsingPool, pos = (6,1), span = (1, 8), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL|wx.TE_PASSWORD)

        gbs.Add(wx.StaticText(p, -1, "下载目录清单") , pos = (7,0), span = (4, 1), flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border = 5 )

        #>>>>
        gbs.Add(wx.StaticText(p, -1,"服务器目录"), pos=(7,1), span=(1,1), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border=5)
        self.mDownSrv = wx.TextCtrl(p)
        gbs.Add(self.mDownSrv, pos=(7,2), span=(1,1), flag=wx.ALL,border=5 )

        gbs.Add(wx.StaticText(p, -1,"本地目录"), pos=(7,3), span=(1,1), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border=5)
        self.mDownLocal = wx.TextCtrl(p)
        gbs.Add(self.mDownLocal, pos=(7,4), span=(1,1), flag=wx.ALL,border=5 )

        self.mDownAdd = wx.Button(p, 9010, "新增")
        gbs.Add(self.mDownAdd, pos=(7,7), span=(1,1), flag=wx.ALL,border=5 )

        self.mDownDel = wx.Button(p, 9011, "删除")
        gbs.Add(self.mDownDel, pos=(7,8), span=(1,1), flag=wx.ALL,border=5 )

        self.mDownList = gridlib.Grid(p, -1)
        self.mDownList.CreateGrid(1,3)
        self.mDownList.HideColLabels()
        self.mDownList.HideRowLabels()

        gbs.Add(self.mDownList, pos=(8,1), span=(3,8), flag=wx.EXPAND|wx.ALL,border=5 )

        wmDownList = (self.GetSize().GetWidth() -  90) /10
        self.mDownList.SetColSize(0, wmDownList * 3.2)
        self.mDownList.SetColSize(1, wmDownList * 3.2)
        self.mDownList.SetColSize(2, wmDownList * 3.2)

        gbs.AddGrowableRow(8)
        # <<<<<<

        gbs.Add(wx.StaticText(p, -1, "上传目录清单") , pos = (12,0), span = (4, 1), flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border = 5 )
        #>>>>
        gbs.Add(wx.StaticText(p, -1,"本地目录"), pos=(12,1), span=(1,1), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border=5)
        self.mUpLocal = wx.TextCtrl(p)
        gbs.Add(self.mUpLocal, pos=(12,2), span=(1,1), flag=wx.ALL,border=5 )

        gbs.Add(wx.StaticText(p, -1,"服务器目录"), pos=(12,3), span=(1,1), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border=5)
        self.mUpSrv = wx.TextCtrl(p)
        gbs.Add(self.mUpSrv, pos=(12,4), span=(1,1), flag=wx.ALL,border=5 )

        gbs.Add(wx.StaticText(p, -1,"备份目录"), pos=(12,5), span=(1,1), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border=5)
        self.mUpBak = wx.TextCtrl(p)
        gbs.Add(self.mUpBak, pos=(12,6), span=(1,1), flag=wx.ALL,border=5 )

        self.mUpAdd = wx.Button(p, 9020, "新增")
        gbs.Add(self.mUpAdd, pos=(12,7), span=(1,1), flag=wx.ALL,border=5 )

        self.mUpDel = wx.Button(p, 9021, "删除")
        gbs.Add(self.mUpDel, pos=(12,8), span=(1,1), flag=wx.ALL,border=5 )

        self.mUpList = gridlib.Grid(p, -1)
        self.mUpList.CreateGrid(1,3)
        self.mUpList.HideColLabels()
        self.mUpList.HideRowLabels()
        self.mUpList.EnableEditing(False)


        gbs.Add(self.mUpList, pos=(13,1), span=(3,8), flag=wx.EXPAND|wx.ALL,border=5 )

        wmUpList = (self.GetSize().GetWidth() -  90) /10
        self.mUpList.SetColSize(0, wmUpList * 3.2)
        self.mUpList.SetColSize(1, wmUpList * 3.2)
        self.mUpList.SetColSize(2, wmUpList * 3.2)

        gbs.AddGrowableRow(13)
        # <<<<<<

        self.lbSave = wx.Button(p, wx.ID_SAVE,"保存")
        gbs.Add(self.lbSave , pos=(16, 7),span=(1,1), flag=wx.ALL, border=5)

        self.lbClose = wx.Button(p, wx.ID_CLOSE, "关闭")
        gbs.Add(self.lbClose , pos=(16, 8),span=(1,1), flag=wx.ALL, border=5)

        w = self.GetSize().GetWidth() / 10

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.mUpList.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnUpGridSelected)
        self.mDownList.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnDownGridSelected)

        if self.id != 0 :
            self.LoadData()
        else:
            self.InitData()



    def OnButtonClicked(self, event):
        id = event.GetId()
        print("key event" + str(id))

        if id == wx.ID_CLOSE:
            self.Close(True)

        if id == wx.ID_HELP:
            self.CheckData()

        if id == wx.ID_SAVE:
            self.SaveData()

        if id == 9020: # up add
            data = {}
            data["localPath"] = self.mUpLocal.GetValue()
            data["srvPath"] = self.mUpSrv.GetValue()
            data["bakPath"] = self.mUpBak.GetValue()

            if len(data["localPath"]) >0 and len(data["srvPath"]) :
                self.lup.append(data)
                self.reLoadUpList()
                self.mUpLocal.Clear()
                self.mUpSrv.Clear()
                self.mUpBak.Clear()

        if id == 9010: # down add
            data = {}
            data["localPath"] = self.mDownLocal.GetValue()
            data["srvPath"] = self.mDownSrv.GetValue()

            if len(data["localPath"]) >0 and len(data["srvPath"]) :
                self.ldown.append(data)
                self.reLoadDownList()
                self.mDownLocal.Clear()
                self.mDownSrv.Clear()

        if id== 9021: #up del
            row = self.mUpList.GetGridCursorRow()
            col = self.mUpList.GetGridCursorCol()

            if row >= 0 and col >= 0 :
                index = row * 3 + col
                del self.lup[index]
                self.reLoadUpList()

        if id== 9011: #up del
            row = self.mDownList.GetGridCursorRow()
            col = self.mDownList.GetGridCursorCol()

            if row >= 0 and col >= 0 :
                index = row * 3 + col
                del self.ldown[index]
                self.reLoadDownList()

    def OnCloseWindow(self,event):
        self.Destroy()

    def LoadData(self):
        l = self.pw.cfgManager.readFtpList()

        for i, item in enumerate(l):
            if item["ftpId"] == self.id:
                self.mFtpId.SetValue(item["ftpId"])
                self.mFtpHost.SetValue(item["ftpHost"])

                if item["ftpType"] == "ftpport":
                    self.mFtpType.SetSelection(0)

                if item["ftpType"] == "ftppasv":
                    self.mFtpType.SetSelection(1)

                if item["ftpType"] == "sftp":
                    self.mFtpType.SetSelection(2)

                self.mFtpPort.SetValue(item["ftpPort"])

                self.mFtpUser.SetValue(item["ftpUser"])
                self.mFtpPsw.SetValue(item["ftpPsw"])

                if item["usingPool"] == "true":
                    self.mUsingPool.SetValue(1)
                else:
                    self.mUsingPool.SetValue(0)

                self.lup = item["upload"]
                self.reLoadUpList()

                self.ldown = item["download"]
                self.reLoadDownList()

                break

    def InitData(self):
        self.mFtpType.SetSelection(2)
        self.mFtpId.SetValue(str(uuid.uuid1()))
        self.lup = []
        self.ldown = []

    def CheckData(self):
        phyftp = FtpManager(self.pw)

        strMsg=[]
        if len(self.mFtpHost.GetValue()) >0 and self.mFtpHost.GetValue() != None:

            phyftp.ftpHost = self.mFtpHost.GetValue()

            if( self.mFtpType.GetSelection() == 0):
                phyftp.type = "ftpport"
                phyftp.ftpPort = self.mFtpPort.GetValue() if len(self.mFtpPort.GetValue()) > 0 else "21"
                strMsg.append("测试Ftp 主动模式 （{}:{}）".format( phyftp.ftpHost , phyftp.ftpPort))


            if( self.mFtpType.GetSelection() == 1):
                phyftp.type = "ftppasv"
                phyftp.ftpPort = self.mFtpPort.GetValue() if len(self.mFtpPort.GetValue()) > 0 else "21"
                strMsg.append("测试Ftp 被动模式 （{}:{}）".format( phyftp.ftpHost , phyftp.ftpPort))

            if( self.mFtpType.GetSelection() == 2):
                phyftp.type = "sftp"
                phyftp.ftpPort = self.mFtpPort.GetValue() if len(self.mFtpPort.GetValue()) > 0 else "22"
                strMsg.append("测试Sftp （{}:{}）".format( phyftp.ftpHost , phyftp.ftpPort))

            if len(self.mFtpUser.GetValue()) == 0 :
                phyftp.ftpUser = "anonymous"
                phyftp.ftpPsw = "whatever"
                strMsg.append("(匿名)")
            else:
                phyftp.ftpUser = self.mFtpUser.GetValue()
                phyftp.ftpPsw = self.mFtpPsw.GetValue()
                strMsg.append("({})".format( phyftp.ftpUser))

            print(vars(phyftp))

            try:
                phyftp.CheckConn()
                strMsg.append("===>成功\r\n")
            except Exception as ex:
                strMsg.append("===>失败：" + ex.message + "\r\n")

            dlg = wx.MessageDialog(self, "".join(strMsg),'连接测试',wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()


    def SaveData(self):
        # l = self.pw.cfgManager.readFtpList()
        #
        # for i, item in enumerate(l):
        #     if item["ftpId"] == self.id:


        data = {}
        data["ftpId"] = self.mFtpId.GetValue()
        data["ftpHost"] = self.mFtpHost.GetValue()

        if self.mFtpType.GetSelection() == 0:
            data["ftpType"] = "ftpport"
            data["ftpPort"] = self.mFtpPort.GetValue() if len(self.mFtpPort.GetValue()) > 0 else "21"

        if self.mFtpType.GetSelection() == 1:
            data["ftpType"] = "ftppasv"
            data["ftpPort"] = self.mFtpPort.GetValue() if len(self.mFtpPort.GetValue()) > 0 else "21"

        if self.mFtpType.GetSelection() == 2:
            data["ftpType"] = "sftp"
            data["ftpPort"] = self.mFtpPort.GetValue() if len(self.mFtpPort.GetValue()) > 0 else "22"

        if len(self.mFtpUser.GetValue()) == 0 :
            data["ftpUser"] = "anonymous"
            data["ftpPsw"]= "whatever"
        else:
            data["ftpUser"] = self.mFtpUser.GetValue()
            data["ftpPsw"]= self.mFtpPsw.GetValue()

        if self.mUsingPool.GetValue() == 0:
            data["usingPool"] = "false"
        if self.mUsingPool.GetValue() == 1:
            data["usingPool"] = "true"

        data["upload"] = self.lup
        data["download"] = self.ldown

        try:
            self.pw.cfgManager.addFtpFormList(data)

            dlg = wx.MessageDialog(self, "保存成功.", '保存', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        except  Exception as ex:
            dlg = wx.MessageDialog(self, ex.message, '保存失败', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def OnUpGridSelected(self, evt):
        evt.Skip()

    def OnDownGridSelected(self, evt):
        evt.Skip()

    def reLoadUpList(self):
        self.mUpList.ClearGrid()
        for i, itemup in enumerate(self.lup):
            r = i // 3
            c = i % 3
            if r > self.mUpList.GetNumberRows() - 1:
                self.mUpList.AppendRows(1)

            disp = itemup["localPath"] + "=>" + itemup["srvPath"] + " #" + itemup["bakPath"]
            self.mUpList.SetCellValue(r, c, disp)

    def reLoadDownList(self):
        self.mDownList.ClearGrid()
        for i, itemdown in enumerate(self.ldown):
            r = i // 3
            c = i % 3

            if r > self.mDownList.GetNumberRows() - 1:
                self.mDownList.AppendRows(1)

            disp = itemdown["srvPath"] + "=>" + itemdown["localPath"]
            self.mDownList.SetCellValue(r, c, disp)

