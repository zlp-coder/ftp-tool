# coding=utf-8
import wx
from FrmUpTaskEdit import *
import wx.dataview as dvlib

class FrmUpTask(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent)

        self.pw = parent
        self.Title = "上传任务管理"
        self.SetSize(800, 600)
        self.Center()

        p = wx.Panel(self)
        gbs = self.gbs = wx.GridBagSizer(vgap=5, hgap=5)
        p.SetSizer(gbs)

        gbs.Add(wx.StaticText(p, -1, "任务名称:") , pos=(0,0), span = (1, 1), flag = wx.EXPAND|wx.ALL, border = 5 )

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

        gbs.Add(wx.StaticText(p, - 1, "* 执行顺序按从大到小顺序执行"), pos = (1,0), span=(1,9), flag=wx.EXPAND | wx.ALL, border=5)

        self.dv = dvlc = dvlib.DataViewListCtrl(p)
        gbs.Add(dvlc, pos=(2, 0), span=(1, 9), flag=wx.EXPAND | wx.ALL, border=5)
        gbs.AddGrowableRow(2)

        self.lbSave = wx.Button(p, wx.ID_OK, "保存")
        gbs.Add(self.lbSave, pos=(3, 7), span=(1,1), flag=wx.ALL, border=5)

        self.lbClose = wx.Button(p, wx.ID_CLOSE, "关闭")
        gbs.Add(self.lbClose, pos=(3, 8), span=(1,1), flag=wx.ALL, border=5)

        w=self.GetSize().GetWidth() / 10 * 0.95
        dvlc.AppendTextColumn("执行顺序" , width=int(w * 1))
        dvlc.AppendTextColumn("任务名称" , width=int(w * 2))
        dvlc.AppendTextColumn("任务备注" , width=int(w * 4))
        dvlc.AppendTextColumn("状态" , width=int(w * 1))
        dvlc.AppendTextColumn("最后运行时间" , width=int(w * 2))

        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind( dvlib.EVT_DATAVIEW_ITEM_ACTIVATED, self.OnDoubleClick)

        self.Init();

    def Init(self):
        self.idList = []
        self.LoadData()

    def OnDoubleClick(self, event):
        if self.dv.GetSelection().IsOk():
            wedit = FrmUpTaskEdit(self.pw, seq=self.idList[self.dv.GetSelectedRow()])
            wedit.ShowModal()
            self.LoadData()

    def OnButtonClicked(self, event):
        id = event.GetId()
        print(id)

        if id == wx.ID_CLOSE:
            self.Close(True)

        if id == wx.ID_ADD:
            wedit = FrmUpTaskEdit(self.pw)
            wedit.ShowModal()
            self.LoadData()

        if id == wx.ID_EDIT:
            if self.dv.GetSelection().IsOk():
                wedit = FrmUpTaskEdit(self.pw, seq = self.idList[self.dv.GetSelectedRow()])
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
            dlg = wx.MessageDialog(self, '确定需要删除指定的任务吗？', '提示', wx.YES_NO | wx.ICON_INFORMATION)
            lr = dlg.ShowModal()

            if lr == wx.ID_YES:
                self.pw.cfgManager.delUpTaskList(self.idList[self.dv.GetSelectedRow()])
                self.LoadData()

    def OnCloseWindow(self,event):
        self.Destroy()

    def LoadData(self ):
        self.dv.DeleteAllItems()

        l = self.pw.cfgManager.readUploadList()
        qFtpHost = self.tqFtpHost.GetValue()
        data = []

        if len(qFtpHost) >0:
            for i, item in enumerate(l):
                if qFtpHost in item["taskName"]:
                    data.append(item)
        else:
            data = l

        self.idList = []
        for i,item in enumerate(data):
            data = []
            data.append(item["order"])
            data.append(item["taskName"])
            data.append(item["taskDesc"])
            data.append("有效" if item["status"] == "1" else "无效")
            data.append(item["lastDate"])
            self.dv.AppendItem(data)
            self.idList.append(item["seq"])

