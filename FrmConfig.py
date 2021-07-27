#coding=utf-8
#
import os
import wx
import json
import appglobal

class FrmConfig(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.pw = parent

        self.SetTitle(u"配置管理")
        self.SetSize(650, 400)
        self.Center()

        gbs = self.gbs = wx.GridBagSizer(vgap=5,hgap=5)
        p = wx.Panel(self)
        p.SetSizer(gbs)

        row = 0
        gbs.Add(wx.StaticText(p, -1 , "客户端ID") , pos=(row, 0) , span=(1,1) , flag=wx.ALL, border=5)
        self.mid = wx.TextCtrl(p, -1)
        gbs.Add( self.mid , pos=(row, 1) , span=(1,3), flag=wx.ALL|wx.EXPAND, border=5)

        row+=1
        gbs.Add(wx.StaticText(p, -1 , "安装地址") , pos=(row, 0) , span=(1,1) , flag=wx.ALL, border=5)
        self.maddress = wx.TextCtrl(p, -1)
        gbs.Add( self.maddress , pos=(row, 1) , span=(1,3), flag=wx.ALL|wx.EXPAND, border=5)

        row+=1
        gbs.Add(wx.StaticText(p, -1 , "状态报文间隔（秒）") , pos=(row, 0) , span=(1,1) , flag=wx.ALL, border=5)
        self.mstatusReport = wx.TextCtrl(p, -1)
        gbs.Add( self.mstatusReport , pos=(row, 1) , span=(1,3), flag=wx.ALL|wx.EXPAND, border=5)

        row+=1
        gbs.Add(wx.StaticText(p, -1 , "定期重启") , pos=(row, 0) , span=(1,1) , flag=wx.ALL, border=5)
        self.mrunReboot = wx.CheckBox(p,-1 ,"控制台程序，每天[")
        gbs.Add( self.mrunReboot , pos=(row, 1) , span=(1,1), flag=wx.ALL, border=5)
        self.mrunReboottime = wx.TextCtrl(p)
        gbs.Add(self.mrunReboottime, pos=(row, 2), span=(1, 1), flag=wx.ALL, border=5)
        gbs.Add(wx.StaticText(p, -1, "]重启"), pos=(row, 3), span=(1, 1), flag=wx.ALL, border=5)

        row+=1
        gbs.Add(wx.StaticText(p, -1 , "定长重启") , pos=(row, 0) , span=(1,1) , flag=wx.ALL, border=5)
        self.mrunRebootDuring = wx.CheckBox(p,-1 ,"控制台程序，运行[")
        gbs.Add( self.mrunRebootDuring , pos=(row, 1) , span=(1,1), flag=wx.ALL, border=5)
        self.mrunRebootDuringHours = wx.TextCtrl(p)
        gbs.Add(self.mrunRebootDuringHours, pos=(row, 2), span=(1, 1), flag=wx.ALL, border=5)
        gbs.Add(wx.StaticText(p, -1, "]小时后，自动重启。"), pos=(row, 3), span=(1, 1), flag=wx.ALL, border=5)

        row+=1
        gbs.Add(wx.StaticText(p, -1 , "异常重启") , pos=(row, 0) , span=(1,1) , flag=wx.ALL, border=5)
        self.mrunRebootOnError = wx.CheckBox(p,-1 ," 控制台程序，ERROR日志内容中包含[")
        gbs.Add( self.mrunRebootOnError , pos=(row, 1) , span=(1,1), flag=wx.ALL, border=5)
        self.mrunRebootOnErrorList = wx.TextCtrl(p)
        gbs.Add(self.mrunRebootOnErrorList, pos=(row, 2), span=(1, 1), flag=wx.ALL, border=5)
        gbs.Add(wx.StaticText(p, -1, "] 时，自动重启"), pos=(row, 3), span=(1, 1), flag=wx.ALL, border=5)

        row+=1
        gbs.Add(wx.StaticText(p, -1 , "状态报文通道") , pos=(row, 0) , span=(1,1) , flag=wx.ALL, border=5)
        self.mpip = wx.StaticText(p)
        gbs.Add( self.mpip , pos=(row, 1) , span=(1,3), flag=wx.ALL, border=5)

        row+=1
        gbs.Add(wx.StaticText(p, -1 , "日志文件位置") , pos=(row, 0) , span=(1,1) , flag=wx.ALL, border=5)
        self.mlogpath = wx.StaticText(p)
        gbs.Add( self.mlogpath , pos=(row, 1) , span=(1,3), flag=wx.ALL, border=5)

        row+=1
        gbs.Add(wx.Button(p, wx.ID_EXECUTE, "导出") , pos=(row, 1) , span=(1,1), flag=wx.ALL, border=5)
        gbs.Add(wx.Button(p, wx.ID_SAVE, "保存") , pos=(row, 2) , span=(1,1), flag=wx.ALL, border=5)
        gbs.Add(wx.Button(p, wx.ID_CLOSE, "关闭") , pos=(row, 3) , span=(1,1), flag=wx.ALL, border=5)

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.LoadData()

    def OnButtonClicked(self, event):
        id = event.GetId()

        if id == wx.ID_CLOSE:
            self.Close(True)

        if id == wx.ID_SAVE:
            self.SaveData()

        if id ==wx.ID_EXECUTE:
            dlg = wx.TextEntryDialog(self, '配置文档的数据：','导出', '')
            dlg.SetValue(json.dumps(self.pw.cfgManager.cfg))

            dlg.ShowModal()
            dlg.Destroy()

    def OnCloseWindow(self,event):
        self.Destroy()

    def LoadData(self):
        data = self.pw.cfgManager.cfg

        self.mid.SetValue(data["id"])
        self.maddress.SetValue(data["address"])
        self.mstatusReport.SetValue(data["statusReport"])

        self.mrunReboottime.SetValue(data["runReboottime"])
        if data["runReboot"] == "true":
            self.mrunReboot.SetValue(1)

        self.mrunRebootDuringHours.SetValue( data["runRebootDuringHours"])
        if data["runRebootDuring"] == "true":
            self.mrunRebootDuring.SetValue(1)

        self.mrunRebootOnErrorList .SetValue( data["runRebootOnErrorList"])
        if data["runRebootOnError"] == "true":
            self.mrunRebootOnError.SetValue(1)

        s = ""
        for i, item in enumerate(self.pw.cfgManager.readUploadList()):
            if item["isPsd"] == "1" :
              s += item["taskName"] + ";"

        if len(s) >0 :
            self.mpip.SetLabel(s)
            self.mpip.SetBackgroundColour('White')
        else:
            self.mpip.SetLabel("!尚未设置状态报文通道")
            self.mpip.SetBackgroundColour('Yellow')

        self.mlogpath.SetLabel(os.getcwd() + "log.txt")


    def SaveData(self):
        data = self.pw.cfgManager.cfg

        data["id"] = self.mid.GetValue()
        data["address"] = self.maddress.GetValue()
        data["statusReport"] = self.mstatusReport.GetValue()

        data["runReboottime"] = self.mrunReboottime.GetValue()
        if self.mrunReboot.GetValue() == 1:
            data["runReboot"] = "true"
        else:
            data["runReboot"] = "false"

        data["runRebootDuringHours"] = self.mrunRebootDuringHours.GetValue()
        if self.mrunRebootDuring.GetValue() == 1:
            data["runRebootDuring"] = "true"
        else:
            data["runRebootDuring"] = "false"


        data["runRebootOnErrorList"] = self.mrunRebootOnErrorList.GetValue()
        if self.mrunRebootOnError.GetValue() == 1:
            data["runRebootOnError"] = "true"
        else:
            data["runRebootOnError"] = "false"

        try:
            self.pw.cfgManager.saveConfigFile()
            dlg =wx.MessageBox("保存成功","提示",wx.OK)
        except Exception as ex:
            appglobal.logger.info(ex)
            dlg =wx.MessageBox("保存失败:" + ex.message,"提示",wx.OK)