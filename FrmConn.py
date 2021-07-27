# coding=utf-8
import wx
from FrmConnEdit import *
import wx.dataview as dvlib

class FrmConn(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.pw = parent
        self.Title = "连接管理"
        self.SetSize(800, 600)
        self.Center()

        p = wx.Panel(self)
        gbs = self.gbs = wx.GridBagSizer(vgap=5, hgap=5)
        p.SetSizer(gbs)

        gbs.Add(wx.StaticText(p, -1, "服务器地址:") , pos = (0,0), span = (1, 1), flag = wx.EXPAND|wx.ALL, border = 5 )

        self.tqFtpHost = wx.TextCtrl(p)
        gbs.Add(self.tqFtpHost, pos=(0,1), span=(1, 1), flag = wx.EXPAND|wx.ALL, border=5 )
        gbs.AddGrowableCol(1)

        self.lbQuery = wx.Button(p, wx.ID_FIND, "查询")
        gbs.Add(self.lbQuery, pos=(0, 2), span=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

        self.lbAdd = wx.Button(p,wx.ID_ADD, "新增")
        gbs.Add(self.lbAdd, pos=(0, 6), span=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

        self.lbDel = wx.Button(p, wx.ID_DELETE,"删除")
        gbs.Add(self.lbDel, pos=(0, 7), span=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

        self.lbEdit = wx.Button(p,wx.ID_EDIT,"编辑")
        gbs.Add(self.lbEdit, pos=(0, 8), span=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

        self.dv = dvlc = dataview.DataViewListCtrl(p)
        gbs.Add(dvlc, pos=(1, 0), span=(1, 9), flag=wx.EXPAND | wx.ALL, border=5)
        gbs.AddGrowableRow(1)

        self.lbSave = wx.Button(p, wx.ID_OK, "保存")
        gbs.Add(self.lbSave, pos=(2, 7), span=(1,1), flag=wx.ALL, border=5)

        self.lbClose = wx.Button(p, wx.ID_CLOSE, "关闭")
        gbs.Add(self.lbClose, pos=(2, 8), span=(1,1), flag=wx.ALL, border=5)

        w=self.GetSize().GetWidth() / 10
        dvlc.AppendTextColumn("序号" , width=int(w * 2))
        dvlc.AppendTextColumn("服务器地址" , width=int(w * 3.5))
        dvlc.AppendTextColumn("上传目录" , width=int(w * 2))
        dvlc.AppendTextColumn("下载目录" , width=int(w * 2))

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind( dvlib.EVT_DATAVIEW_ITEM_ACTIVATED, self.OnDoubleClick)

        self.Init();

    def Init(self):
        self.LoadData()

    def OnDoubleClick(self, event):
        if self.dv.GetSelection().IsOk():
            wedit = FrmConnEdit(self.pw, ftpid=self.dv.GetValue(self.dv.GetSelectedRow(), 0))
            wedit.ShowModal()
            self.LoadData()

    def OnButtonClicked(self, event):
        id = event.GetId()
        print(id)

        if id == wx.ID_CLOSE:
            self.Close(True)

        if id == wx.ID_ADD:
            wedit = FrmConnEdit(self.pw)
            wedit.ShowModal()
            self.LoadData()

        if id == wx.ID_EDIT:
            if self.dv.GetSelection().IsOk():
                wedit = FrmConnEdit(self.pw, ftpid=self.dv.GetValue(self.dv.GetSelectedRow(), 0))
                wedit.ShowModal()
                self.LoadData()

        if id == wx.ID_DELETE:
            self.OnlbDeleteClicked()

        if id == wx.ID_FIND:
            self.OnlnFindClicked()

    def OnlnFindClicked(self):
        self.LoadData()


    def OnlbDeleteClicked(self):
        if self.dv.SelectedRow >= 0:
            dlg = wx.MessageDialog(self, '确定需要删除指定的连接吗？', '提示', wx.YES_NO | wx.ICON_INFORMATION)
            lr = dlg.ShowModal()

            if lr == wx.ID_YES:
                self.pw.cfgManager.delFtpFormList(self.dv.GetValue(self.dv.GetSelectedRow(), 0))
                self.LoadData()

    def OnCloseWindow(self,event):
        self.Destroy()

    def LoadData(self ):
        self.dv.DeleteAllItems()

        l = self.pw.cfgManager.readFtpList()
        qFtpHost = self.tqFtpHost.GetValue()
        data = []

        if len(qFtpHost) >0:
            for i, item in enumerate(l):
                if qFtpHost in str(item["ftpHost"]):
                    data.append(item)
        else:
            data = l

        for i,item in enumerate(data):
            data = []
            data.append(item["ftpId"])
            data.append(item["ftpType"] + "://" + item["ftpUser"] + "@" + item["ftpHost"] + ":" + item["ftpPort"])

            uplist = item["upload"]
            s = ""
            for i, upitem in enumerate(uplist):
                s = s + upitem["localPath"] +  "=>" + upitem["srvPath"] + "; "
            data.append(s)

            downlist = item["download"]
            ss = ""
            for i, upitem in enumerate(downlist):
                ss = ss + upitem["srvPath"] + "=>" + upitem["localPath"] + "; "
            data.append(ss)

            self.dv.AppendItem(data)

