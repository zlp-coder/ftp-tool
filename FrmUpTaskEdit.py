#coding=utf-8

import wx
import wx.dataview as dataview
import wx.grid as gridlib
import uuid
import re

from MainWindow import *
from FrmUpTask import *

class FrmUpTaskEdit(wx.Dialog):

    def __init__(self, parent, seq=0):
        wx.Dialog.__init__(self, parent)
        self.pw=parent
        self.id = seq

        self.Title = "新增或者编辑一个上传任务 " + str(seq)
        self.SetSize(900, 800)
        self.Center()

        p = wx.Panel(self)
        gbs = self.gbs = wx.GridBagSizer(vgap=5, hgap=5)
        p.SetSizer(gbs)

        gbs.Add(wx.StaticText(p, -1, "Seq*"), pos=(0,0),span = (1, 1), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border=5)
        self.mSeq = wx.TextCtrl(p)
        self.mSeq.SetEditable(False)
        gbs.Add(self.mSeq, pos=(0, 1), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
        self.mispsd=wx.CheckBox(p, -1, "状态报文通道")
        gbs.Add(self.mispsd, pos=(0, 2), span=(1, 1), flag=wx.EXPAND|wx.ALL, border=5)
        gbs.AddGrowableCol(1)

        gbs.Add(wx.StaticText(p, -1, "序号") , pos = (1,0), span = (1, 1), flag=wx.ALIGN_CENTRE_VERTICAL|wx.ALL, border=5)
        self.morder = wx.TextCtrl(p)
        gbs.Add(self.morder, pos = (1,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "任务名称") , pos = (2,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mtaskName = wx.TextCtrl(p)
        gbs.Add(self.mtaskName, pos = (2,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "任务备注") , pos = (3,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mtaskDesc = wx.TextCtrl(p)
        gbs.Add(self.mtaskDesc, pos = (3,1), span = (2, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)
        gbs.AddGrowableRow(3)

        gbs.Add(wx.StaticText(p, -1, "状态") , pos = (5,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mstatus = wx.CheckBox(p,-1, "启用")
        gbs.Add(self.mstatus, pos = (5,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "连接") , pos = (6,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        sampleList = self.pw.cfgManager.getConnDropDownUpload()
        self.mftpIdDisp = wx.ComboBox(p, -1, "", (90, 50), (160, -1), sampleList, wx.CB_DROPDOWN)

        gbs.Add(self.mftpIdDisp, pos = (6,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "本地目录") , pos = (7,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mlocalPath = wx.TextCtrl(p)
        gbs.Add(self.mlocalPath, pos = (7,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "上传服务器目录") , pos = (8,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.msrvPath = wx.TextCtrl(p)
        gbs.Add(self.msrvPath, pos = (8,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "文件名匹配（正则）") , pos = (9,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mfilterFilename = wx.TextCtrl(p)
        gbs.Add(self.mfilterFilename, pos = (9,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "文件内容匹配（正则）") , pos = (10,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mfilterContent = wx.TextCtrl(p)
        gbs.Add(self.mfilterContent, pos = (10,1), span = (2, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)
        gbs.AddGrowableRow(10)

        gbs.Add(wx.StaticText(p, -1, "执行周期（秒）") , pos = (12,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mtransRun = wx.TextCtrl(p)
        gbs.Add(self.mtransRun, pos = (12,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "每次最大文件处理数") , pos = (13,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mtransFiles = wx.TextCtrl(p)
        gbs.Add(self.mtransFiles, pos = (13,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "本地备份目录") , pos = (14,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mbakPath = wx.TextCtrl(p)
        gbs.Add(self.mbakPath, pos = (14,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "后续处理") , pos = (15,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mafterOprt = wx.CheckBox(p,-1,"抄送，同时抄送一份到同一个服务器的另外一个目录")
        gbs.Add(self.mafterOprt, pos = (15,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        gbs.Add(wx.StaticText(p, -1, "抄送服务器目录") , pos = (16,0), span = (1, 1),flag = wx.ALIGN_CENTRE_VERTICAL|wx.ALL,border = 5 )
        self.mccsrvPath = wx.TextCtrl(p)
        gbs.Add(self.mccsrvPath, pos = (16,1), span = (1, 2), flag=wx.EXPAND|wx.ALIGN_CENTRE_VERTICAL)

        self.lbSave = wx.Button(p, wx.ID_SAVE,"保存")
        gbs.Add(self.lbSave , pos=(17, 1),span=(1,1), flag=wx.ALL | wx.ALIGN_RIGHT, border=5)

        self.lbClose = wx.Button(p, wx.ID_CLOSE, "关闭")
        gbs.Add(self.lbClose , pos=(17, 2),span=(1,1), flag=wx.ALL|wx.ALIGN_RIGHT, border=5)

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.mftpIdDisp)

        if self.id != 0 :
            self.LoadData()
        else:
            self.InitData()

    def OnButtonClicked(self, event):
        id = event.GetId()
        print("key event" + str(id))

        if id == wx.ID_CLOSE:
            self.Close(True)

        if id == wx.ID_SAVE:
            self.SaveData()

    def OnCloseWindow(self,event):
        self.Destroy()

    def LoadData(self):
        l = self.pw.cfgManager.readUploadList()

        for i, item in enumerate(l):
            if item["seq"] == self.id:

                self.mSeq.SetValue(item["seq"])
                self.morder.SetValue(item["order"])

                if item["isPsd"] == "1":
                    self.mispsd.SetValue(True)
                else:
                    self.mispsd.SetValue(False)

                self.mtaskName.SetValue(item["taskName"])
                self.mtaskDesc.SetValue(item["taskDesc"])

                if item["status"] == "1":
                    self.mstatus.SetValue(True)
                else:
                    self.mstatus.SetValue(False)

                self.mftpId =item["ftpId"]
                self.mftpIdDisp.SetValue(item["ftpIdDisp"])

                self.mlocalPath.SetValue(item["localPath"])
                self.msrvPath.SetValue(item["srvPath"])
                self.mfilterFilename.SetValue(item["filterFilename"])
                self.mfilterContent.SetValue(item["filterContent"])
                self.mtransRun.SetValue(item["transRun"])
                self.mtransFiles.SetValue(item["transFiles"])
                self.mbakPath.SetValue(item["bakPath"])

                if item["afterOprt"] == "cc" :
                    self.mafterOprt.SetValue(1)

                self.mccsrvPath.SetValue(item["ccsrvPath"])

                break

    def InitData(self):
        self.mstatus.SetValue(1)
        self.mSeq.SetValue(str(uuid.uuid1()))
        self.mftpId = 0

    def SaveData(self):
        data = {}
        data["seq"] = self.mSeq.GetValue()
        data["order"] = self.morder.GetValue()
        data["isPsd"] = "1" if self.mispsd.GetValue() == True else "-1"
        data["taskName"] = self.mtaskName.GetValue()
        data["taskDesc"] = self.mtaskDesc.GetValue()
        data["status"] = "1" if self.mstatus.GetValue() == True else "-1"
        data["ftpId"] =  self.mftpId
        data["ftpIdDisp"] = self.mftpIdDisp.GetValue()
        data["localPath"] = self.mlocalPath.GetValue()
        data["srvPath"] = self.msrvPath.GetValue()
        data["filterFilename"] = self.mfilterFilename.GetValue()
        data["filterContent"] = self.mfilterContent.GetValue()
        data["transRun"] = self.mtransRun.GetValue()
        data["transFiles"] = self.mtransFiles.GetValue()
        data["bakPath"] = self.mbakPath.GetValue()
        data["afterOprt"] = "cc" if self.mafterOprt.GetValue() == True else "no"
        data["ccsrvPath"] = self.mccsrvPath.GetValue()

        data["runningState"] = "等候"
        data["lastDate"] = ""

        try:
            self.pw.cfgManager.addUpTaskList(data)

            dlg = wx.MessageDialog(self, "保存成功.", '保存', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        except  Exception as ex:
            dlg = wx.MessageDialog(self, ex.message, '保存失败', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()

        pattern = re.compile(r'.*?://.*?@.*?:.*?\((.*?)=>(.*?)\) #(.*?) \[id=(.*?)\]')
        m = pattern.match(cb.GetValue())

        try:
            self.mlocalPath.SetValue(m.groups()[0])
            self.msrvPath.SetValue(m.groups()[1])
            self.mbakPath.SetValue(m.groups()[2])
            self.mftpId = m.groups()[3]
        except Exception as ex:
            dlg = wx.MessageDialog(self, "连接选择失败." + ex.message, '选择', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
