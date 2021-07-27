#coding=utf-8
import wx
import wx.grid
import datetime
import threading
import thread
import inspect
import ctypes

from FrmConn import *
from ConfigManager import *
from FrmUpTask import *
from FrmDownTask import *
from FrmConfig import *

class MainWindow(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self, parent, title=u"文件传输客户端" , size= (1280,800))

        self.SetWindowStyle(wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        menu = wx.Menu()
        menu.Append(9901, u"连接管理", u"管理客户端的连接")
        menu.AppendSeparator()
        menu.Append(9902, u"上传任务管理", u"创建上传任务，修改上传任务的定时，过滤和目录")
        menu.Append(9903, u"下载任务管理", u"创建下载任务，修改下载任务的定时，过滤和目录")
        menu.AppendSeparator()
        menu.Append(9905, u"暂停", u"", wx.ITEM_CHECK)
        menu.Append(9904, u"系统参数", u"设置系统参数")
        menu.AppendSeparator()
        menu.Append(wx.ID_EXIT, u"退出", u"退出系统")

        menubar = wx.MenuBar()
        menubar.Append(menu,"文件传输")
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnMenu)
        #self.Bind(wx.EVT_MENU, self.OnAbout, menubar)
        self.CreateStatusBar()

        self.Center()

        #Window UI
        panel = wx.Panel(self)

        panel1 = wx.Panel(panel,  size=(0, wx.EXPAND))
        #self.txtMsg = wx.TextCtrl(panel1, style=wx.TE_MULTILINE, size=(wx.EXPAND, wx.EXPAND))
        self.txtMsg = wx.TextCtrl(panel1, style=wx.TE_MULTILINE, size=(635,720))
        self.txtMsg.SetEditable(True)

        panel2 = wx.Panel(panel, size=(0, wx.EXPAND))
        self.gridUpload = wx.grid.Grid(panel2 ,size =(wx.EXPAND, 0))
        self.gridUpload.CreateGrid(1, 4)
        self.gridUpload.HideColLabels()
        self.gridUpload.HideRowLabels()
        self.gridUpload.EnableEditing(False)


        w1 =  self.gridUpload.GetSize().GetWidth() / 12 * 0.71
        self.gridUpload.SetColSize(0, w1 * 0.1 )
        self.gridUpload.SetColSize(1, w1 * 0.4)
        self.gridUpload.SetColSize(2, w1 * 0.2)
        self.gridUpload.SetColSize(3, w1 * 0.5)

        self.gridDownLoad = wx.grid.Grid(panel2,size =(wx.EXPAND, 0))
        self.gridDownLoad.CreateGrid(0, 4)
        self.gridDownLoad.HideColLabels()
        self.gridDownLoad.HideRowLabels()
        self.gridDownLoad.EnableEditing(False)

        self.gridDownLoad.SetColSize(0, w1 * 0.1 )
        self.gridDownLoad.SetColSize(1, w1 * 0.4)
        self.gridDownLoad.SetColSize(2, w1 * 0.2)
        self.gridDownLoad.SetColSize(3, w1 * 0.5)

        panel2box = wx.FlexGridSizer(2,1,5,0)

        panel2box.Add(self.gridUpload, 0 ,wx.EXPAND)
        panel2box.Add(self.gridDownLoad,0 ,wx.EXPAND)
        panel2box.AddGrowableRow(0, 5)
        panel2box.AddGrowableRow(1, 5)

        panel2.SetSizer(panel2box)

        fgs = wx.FlexGridSizer(1, 2, 0, 5)  # 设置为1行，2列，列间距为5
        fgs.Add(panel1, 0, wx.EXPAND)
        fgs.Add(panel2, 0, wx.EXPAND)
        fgs.AddGrowableCol(0, 1)  # 指定第一列占1/3的宽度
        fgs.AddGrowableCol(1, 1)  # 指定第二列占2/3的宽度
        panel.SetSizer(fgs)

        self.Show(True)
        self.LoadData()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)

        self.threadTimer = {}
        self.pauseTask = False

    def OnMenu(self, event):
        id = event.GetId()

        if id == wx.ID_EXIT:
            self.Close()

        if id == 9901:
            wconn = FrmConn(self)
            wconn.ShowModal()
            self.ShowMsg(u"连接管理完成配置")

        if id == 9902:
            dlg = FrmUpTask(self)
            dlg.ShowModal()

            self.ShowMsg(u"上传任务编辑完成，重新加载上传任务列表")
            self.RefreshUploadList()

        if id == 9903:
            dlg = FrmDownTask(self)
            dlg.ShowModal()
            self.ShowMsg("下载任务编辑完成，重新加载上传任务列表")

            self.gridDownLoad.ClearGrid()
            for i, item in enumerate(self.cfgManager.readDownloadList()):
                if item["status"] == "1":
                    self.gridDownLoad.InsertRows()
                    self.gridDownLoad.SetCellValue(i, 0, item["order"])
                    self.gridDownLoad.SetCellValue(i, 1, item["taskName"])
                    self.gridDownLoad.SetCellValue(i, 2, item["runningState"])
                    self.gridDownLoad.SetCellValue(i, 3, item["lastDate"])

        if id == 9904:
            dlg = FrmConfig(self)
            lr = dlg.ShowModal()
            self.ShowMsg("配置已变更")

        if id == 9905:
            if self.pauseTask == False:
                self.pauseTask = True
                self.ShowMsg("任务调度已暂停")
                #item = self.GetMenuBar().FindItemById(id)

            else:
                self.pauseTask = False
                self.ShowMsg("任务调度已开启")



    def LoadData(self):
        self.ShowMsg("===========>客户端启动")

        self.cfgManager = ConfigManager(self)

        self.ShowMsg("加载上传任务列表")
        self.RefreshUploadList()


        self.ShowMsg("加载下载任务列表")
        for i, item in enumerate(self.cfgManager.readDownloadList()):
            if item["status"] == "1" :
                self.gridDownLoad.InsertRows(numRows=1)
                self.gridDownLoad.SetCellValue(i, 0, item["order"])
                self.gridDownLoad.SetCellValue(i, 1, item["taskName"])
                self.gridDownLoad.SetCellValue(i, 2, item["runningState"])
                self.gridDownLoad.SetCellValue(i, 3, item["lastDate"])



    def ShowMsg(self , msg):
        time_stamp = datetime.datetime.now()
        self.txtMsg.WriteText("[" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S') + "] " + msg + "\r\n")

        self.txtMsg.ShowPosition(self.txtMsg.GetLastPosition() )


    def RunUpload(self, conn, item):
        try:
            conn.UploadTask(item)
        except:
            thread.exit()

    def RunDownload(self, conn, item):
        try:
            conn.DownTask(item)
        except:
            thread.exit()

    def OnTimer(self,evt):

        if self.pauseTask:
            return

        try:
            #配置检查
            self.cfgManager.checkConfigModify()

            #连接池维护:一个ftp服务器只有一个连接，任务共用同一个连接
            if  hasattr( self, "conns") == False:
                self.conns = self.cfgManager.getAllBufferConn()

                for item in self.conns.keys():
                    self.ShowMsg(u"初始化连接,id (" + str(item)+") :" + str(self.conns[item].status))
            else:
                for key in self.conns.keys():
                    if self.conns[key].status == "ready":
                        self.conns[key].Noop()

            #线程列表
            tlist = threading.enumerate()

            for t in tlist:
                if self.threadTimer.has_key(t.getName()) == True:

                    d1 = datetime.datetime.strptime(self.threadTimer[t.getName()],"%Y-%m-%d %H:%M:%S") if len(self.threadTimer[t.getName()]) > 0 else datetime.datetime(1900,1,1)
                    d2 = datetime.datetime.now()

                    if (d2 -d1).seconds > 10 * 60:
                          self.stop_thread(t)

            #状态报文

            #上传任务
            for item in self.cfgManager.readUploadList():
                if item["status"] == "1":

                    d1 = datetime.datetime.strptime(item["lastDate"],"%Y-%m-%d %H:%M:%S") if len(item["lastDate"]) > 0 else datetime.datetime(1900,1,1)
                    d2 = datetime.datetime.now()
                    step = int( item["transRun"]) if len(item["transRun"]) > 0 else 60

                    hasRunning = False
                    for t in tlist:
                        if t.getName() == item["seq"]:
                            hasRunning = True
                            break

                    if (d2 - d1).seconds >= step:
                        if hasRunning:
                            self.ShowMsg( u"[WARRNING] 上传任务: (" + item["taskName"] +   u") 在运行中，跳过本次运行")
                        else:
                            if self.conns.has_key(item["ftpId"]):
                                conn = self.conns[item["ftpId"]]
                                if conn.status != "ready":
                                    self.ShowMsg(u"[ERROR] 上传任务: (" + item["taskName"] + u") 无法连接")
                                else:
                                    t = threading.Thread(target=self.RunUpload,name=item["seq"], args= (conn, item))
                                    t.start()
                                    self.threadTimer[item["seq"]] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            else:
                                conn = FtpManager(self)
                                if conn.status != "ready":
                                    self.ShowMsg(u"[ERROR] 上传任务: (" + item["taskName"] + u") 无法连接")
                                else:
                                    t = threading.Thread(target=self.RunUpload,name=item["seq"], args= (conn, item))
                                    t.start()
                                    self.threadTimer[item["seq"]] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    conn.CLose()

            #下载任务
            for item in self.cfgManager.readDownloadList():
                if item["status"] == "1":

                    d1 = datetime.datetime.strptime(item["lastDate"],"%Y-%m-%d %H:%M:%S") if len(item["lastDate"]) > 0 else datetime.datetime(1900,1,1)
                    d2 = datetime.datetime.now()
                    step = int( item["transRun"]) if len(item["transRun"]) > 0 else 60

                    hasRunning2 = False
                    for t in tlist:
                        if t.getName() == item["seq"]:
                            hasRunning2 = True
                            break

                    if (d2 - d1).seconds >= step:
                        if hasRunning2:
                            self.ShowMsg( u"[WARRNING] 下载任务: (" + item["taskName"] +   u") 在运行中，跳过本次运行")
                        else:
                            if self.conns.has_key(item["ftpId"]):
                                conn = self.conns[item["ftpId"]]
                                if conn.status != u"ready":
                                    self.ShowMsg(u"[ERROR] 下载任务: (" + item["taskName"] + u") 无法连接")
                                else:
                                    t = threading.Thread(target=self.RunDownload,name=item["seq"], args= (conn, item))
                                    t.start()
                                    self.threadTimer[item["seq"]] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            else:
                                conn = FtpManager(self)
                                if conn.status != "ready":
                                    self.ShowMsg(u"[ERROR] 下载任务: (" + item["taskName"] + u") 无法连接")
                                else:
                                    t = threading.Thread(target=self.RunDownload,name=item["seq"], args= (conn, item))
                                    t.start()
                                    self.threadTimer[item["seq"]] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    conn.CLose()

            #自启检查
        except Exception as ex:
            print ex
            self.ShowMsg(u"[ERROR] 定时任务异常:" + ex.message)
            self.pauseTask = True


    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)


    def RefreshUploadList(self):

        if self.gridUpload.GetNumberRows()  > 0:
            self.gridUpload.ClearGrid()
            self.gridUpload.DeleteRows(numRows= self.gridUpload.GetNumberRows() )

        rowindex = 0
        firstTmp = []

        for item in self.cfgManager.readUploadList():
            if item["status"] == "1":
                self.gridUpload.InsertRows(numRows=1)
                self.gridUpload.SetCellValue(rowindex, 0, item["order"])
                self.gridUpload.SetCellValue(rowindex, 1, item["taskName"])
                self.gridUpload.SetCellValue(rowindex, 2, item["runningState"])
                self.gridUpload.SetCellValue(rowindex, 3, item["lastDate"])

                if rowindex == 0:
                    firstTmp.append(item["order"])
                    firstTmp.append(item["taskName"])
                    firstTmp.append(item["runningState"])
                    firstTmp.append(item["lastDate"])

                rowindex +=1

        if len(firstTmp) > 0:
            self.gridUpload.SetCellValue(0, 0, firstTmp[0])
            self.gridUpload.SetCellValue(0, 1, firstTmp[1])
            self.gridUpload.SetCellValue(0, 2, firstTmp[2])
            self.gridUpload.SetCellValue(0, 3, firstTmp[3])