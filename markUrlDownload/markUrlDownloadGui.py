import tkinter.filedialog
import tkinter.messagebox
from tkinter import *    #注意模块导入方式，否则代码会有差别
import tkinter.scrolledtext as ScrolledText
import threading
from configobj import ConfigObj
import os
from markUrlDownload.markWebDownload import MarkWebDownload

import datetime

class MarkUrlDownloadGui(object):
    def __init__(self, tkFrame):
        self.downloading = False
        self.downloadType = 'url'
        self.paramInit()
        #先画出容器
        subFm00 = tkinter.Frame(tkFrame)
        subFm01 = tkinter.Frame(tkFrame)
        subFm02 = tkinter.Frame(tkFrame)
        subFm03 = tkinter.Frame(tkFrame)
        # subFm04 = tkinter.Frame(tkFrame)
        subFm05 = tkinter.Frame(tkFrame, background='white')

        subFm00.grid(row=0, column=1,padx=1,pady=3,sticky=W)
        subFm01.grid(row=1, column=1,padx=1,pady=3,sticky=W)
        subFm02.grid(row=2, column=1,padx=1,pady=15,sticky=W)
        subFm03.grid(row=3, column=1,padx=1,pady=0,sticky=W)
        # subFm04.grid(row=4, column=1,padx=1,pady=0,sticky=W)
        subFm05.grid(row=0, column=0,padx=10,pady=5,rowspan=5,columnspan=1,sticky=W+E+N+S)

        #subFm00
        tkinter.Label(subFm00, text='请输入您想要下载的网址，每个网址换行输入，一次最多可输入30个网址：', font=("楷体", 13, "bold")).grid()

        #subFm01
        self.tWebSites = ScrolledText.ScrolledText(subFm01, height=42, width=140,wrap="none")
        hbar = tkinter.Scrollbar(subFm01, orient=HORIZONTAL, command=self.tWebSites.xview)
        self.tWebSites.configure(xscrollcommand=hbar.set)
        self.tWebSites.grid(padx=5)
        hbar.grid(sticky=EW)

        #subFm02
        tkinter.Button(subFm02, text='开始下载', bg="#BC8F8F", font=('宋体', 14), command=lambda : self.thread_it(self.startDownload)).grid(row=2, column=0, stick=W)
        self.lDldProcess = tkinter.Label(subFm02, text='', font=("宋体", 10))
        self.lDldProcess.grid(row=2, column=1, padx=8, sticky=W)

        #subFm03
        self.lSaveDir = tkinter.Label(subFm03, text="保存路径："+self.saveDir, font=("宋体", 10, "bold"))
        self.lSaveDir.grid(row=3, column=0, sticky=W)
        tkinter.Button(subFm03, text='打开', font=('宋体', 10), command=lambda : self.thread_it(self.openDir, self.saveDir)).grid(row=3, column=1, padx=10)
        tkinter.Button(subFm03, text='修改', font=('宋体', 10), command=self.setSaveDir).grid(row=3, column=2, sticky=W)

        #subFm04
        # self.lWkhtmlPath = tkinter.Label(subFm04, text="wkhtmltopdf.exe路径：" + self.wkhtmltopdfExe, font=("宋体", 10, "bold"))
        # self.lWkhtmlPath.grid(row=4, column=0, sticky=W)
        # tkinter.Button(subFm04, text='修改', font=('宋体', 10), command=self.getWkhtmlPath).grid(row=4, column=1, padx=10, stick=E)

        #subFm05
        tkinter.Label(subFm05, text='配置栏', font=("楷体", 13, "bold"), background='white').grid(pady=6)

        v = tkinter.IntVar()
        v.set(1) # set函数是设置单选框中的初始值，set的参数和Radiobutton组件中的value比较，如果存在相同的情况，则为初始值
        tkinter.Radiobutton(subFm05, variable=v ,value=1, command=lambda : self.radioBtCmd('url'), background='white', text="普通非注册网页下载").grid(sticky=W, padx=3,pady=6)
        tkinter.Radiobutton(subFm05, variable=v ,value=2, command=lambda : self.radioBtCmd('zhihu'), background='white', text="知乎问题图片/视频下载").grid(sticky=W, padx=3,pady=6)
        tkinter.Radiobutton(subFm05, variable=v ,value=3, command=lambda : self.radioBtCmd('video'), background='white', text="全网视频下载").grid(sticky=W, padx=3,pady=6)

    def paramInit(self):
        self.curDir =  os.getcwd().replace("\\",'/')
        self.wkhtmltopdfExe = os.path.join(self.curDir,'config/sub01.exe')
        self.annieExe = 'config/sub02.exe'
        self.saveDir = self.curDir

        if(os.path.exists("config/config.ini")):
            config = ConfigObj("config/config.ini",encoding='UTF8')
            self.saveDir = config['PATH_PRRA']['saveDir'].replace("\\",'/')
            print(self.saveDir)
            if(self.wkhtmltopdfExe == '' or self.saveDir == ''):
                print('get para failed')
            else:
                print('get para succeed')

    def startDownload(self):
        if(self.downloading == True):
            tkinter.messagebox.showinfo("MarkTool", "正在下载中...")
            return

        if(os.path.exists(self.wkhtmltopdfExe)):
            pass
        else:
            tkinter.messagebox.showinfo('配置丢失','配置文件丢失，请勿删除config文件夹!')
            return False

        urls = self.tWebSites.get("1.0", "30.end").split('\n')
        urls = [i for i in urls if i != ''] # 删除所有空元素
        self.downloading = True

        if (self.downloadType == 'url'):
            self.urlDwnldFunc(urls)
        elif (self.downloadType == 'zhihu'):
            self.zhihuDwnldFunc(urls)
        elif (self.downloadType == 'video'):
            self.videoDwnldFunc(urls)

        self.lDldProcess.config(text="下载完成！", font=("宋体", 12))
        self.downloading = False

    def urlDwnldFunc(self, urls):
        dld = MarkWebDownload()
        options = {
            'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            # 'orientation':'Landscape',#横向
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-plugins': None,
            'stop-slow-scripts': None,
            'footer-right':'[page]' ,
        }

        webSaveDir = os.path.join(self.saveDir , 'webSite')
        if(os.path.exists(os.path.join(webSaveDir) == False)):
            os.makedirs(webSaveDir)

        for idx,url in enumerate(urls):
            process = "正在下载：{}/{}".format(idx+1,len(urls))
            self.lDldProcess.config(text=process, font=("宋体", 12))
            pdfPath = os.path.join(webSaveDir ,datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.pdf')
            dld.url2pdf(url, self.wkhtmltopdfExe, pdfPath, options)

    def zhihuDwnldFunc(self, urls):
        print(urls)

    def videoDwnldFunc(self, urls):
        print(urls)

    def thread_it(self, func, *args):
        '''将函数打包进线程'''
        # 创建
        t = threading.Thread(target=func, args=args)
        # 守护 !!!
        t.setDaemon(True)
        # 启动
        t.start()
        # 阻塞--卡死界面！
        # t.join()

    def openDir(self, path):
        try:
            os.system("start explorer {}".format(path.replace('/','\\')))
        except:
            print('打开{}失败'.format(path))
            return

    def getWkhtmlPath(self):
        ret = tkinter.filedialog.askopenfilename(filetypes=[("EXE",".exe")])
        if(ret != ""):
            self.wkhtmltopdfExe = ret.replace("\\",'/')
            print(self.wkhtmltopdfExe)
            self.lWkhtmlPath.config(text="wkhtmltopdf.exe路径：" + self.wkhtmltopdfExe, font=("宋体", 10, "bold"))
            self.paramSet()

    def setSaveDir(self):
        ret = tkinter.filedialog.askdirectory()
        if(ret != ""):
            self.saveDir = ret.replace("\\",'/')
            print(self.saveDir)
            self.lSaveDir.config(text="保存路径："+self.saveDir, font=("宋体", 10, "bold"))
            self.paramSet()

    def paramSet(self):
        f= open("config/config.ini","w+")
        f.close()
        config = ConfigObj("config/config.ini",encoding='UTF8')
        config['PATH_PRRA'] = {}
        # config['PATH_PRRA']['wkhtmltopdfExe'] = self.wkhtmltopdfExe
        config['PATH_PRRA']['saveDir'] = self.saveDir
        config.write()

    def radioBtCmd(self, type):
        self.downloadType = type
        print(self.downloadType)