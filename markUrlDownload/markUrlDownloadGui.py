import tkinter.filedialog
import tkinter.messagebox
from tkinter import *    #注意模块导入方式，否则代码会有差别
import tkinter.scrolledtext as ScrolledText
import threading
from configobj import ConfigObj
import os
from markUrlDownload.markWebDownload import MarkWebDownload
from markUrlDownload.markVideoDownload import MarkVideoDownload
import external.ToolTip as tt

import datetime

class MarkUrlDownloadGui(object):
    def __init__(self, tkFrame):
        self.downloading = False
        self.downloadType = 'web'
        self.paramInit()
        #先画出容器
        subFm00 = tkinter.Frame(tkFrame)
        subFm01 = tkinter.Frame(tkFrame)
        subFm02 = tkinter.Frame(tkFrame)
        subFm03 = tkinter.Frame(tkFrame)
        subFm05 = ttk.LabelFrame(tkFrame, text='说明')

        subFm00.grid(row=0, column=0,padx=1,pady=3,sticky=W)
        subFm01.grid(row=1, column=0,padx=1,pady=3,sticky=W)
        subFm02.grid(row=2, column=0,padx=1,pady=15,sticky=W)
        subFm03.grid(row=3, column=0,padx=1,pady=0,sticky=W)
        subFm05.grid(row=0, column=1,pady=5,rowspan=2,columnspan=1,sticky=W+E+N+S)

        #subFm00
        tkinter.Label(subFm00, text='请输入您想要下载的网址，每个网址换行输入，一次最多可输入30个网址：', font=("楷体", 13, "bold")).grid()

        #subFm01
        self.tWebSites = ScrolledText.ScrolledText(subFm01, height=42, width=130,wrap="none")
        hbar = tkinter.Scrollbar(subFm01, orient=HORIZONTAL, command=self.tWebSites.xview)
        self.tWebSites.configure(xscrollcommand=hbar.set)
        self.tWebSites.grid(padx=5)
        hbar.grid(sticky=EW)

        #subFm02
        tkinter.Button(subFm02, text='开始下载', bg="#BC8F8F", font=('宋体', 14), command=lambda : self.thread_it(self.startDownload)).grid(row=2, column=0, stick=W)

        self.savePdfEn = IntVar()
        self.pdfCheckButton = Checkbutton(subFm02, text = "同时保存为PDF", variable = self.savePdfEn, onvalue = 1, offvalue = 0)
        self.pdfCheckButton.grid(row=2, column=1, padx=8, sticky=W)
        tt.create_ToolTip(self.pdfCheckButton, "保存为PDF会略微增加整体下载时间。")

        self.lDldProcess = ttk.Progressbar(subFm02, orient='horizontal', length=600, mode='determinate')
        self.lDldProcess.grid(row=2, column=2, padx=8, sticky=W)

        self.lDldProcessText = tkinter.Label(subFm02, text='', font=("宋体", 10))
        self.lDldProcessText.grid(row=2, column=3, padx=8, sticky=W)

        #subFm03
        self.lSaveDir = tkinter.Label(subFm03, text="保存路径："+self.saveDir, font=("宋体", 10, "bold"))
        self.lSaveDir.grid(row=3, column=0, sticky=W)
        tkinter.Button(subFm03, text='打开', font=('宋体', 10), command=lambda : self.thread_it(self.openDir, self.saveDir)).grid(row=3, column=1, padx=10)
        tkinter.Button(subFm03, text='修改', font=('宋体', 10), command=self.setSaveDir).grid(row=3, column=2, sticky=W)

        #subFm04


        #subFm05
        instructText = \
        "▶ 已适配网站:\
        \n      ◉ 微信公众号\
        \n\
        \n▶ 注意：\
        \n      ◉ 只针对可以公开访问的网站\
        \n      ◉ 无法下载需要登陆的网站\
        \n      ◉ 未适配网站可能存在格式异常\
        \n\
        \n▶ 保存名：下载时间_网页名\
        \n"
        ttk.Label(subFm05, text = instructText).grid(sticky=W, padx=12,pady=6)

    def paramInit(self):
        self.curDir =  os.getcwd().replace("\\",'/')
        self.wkhtmltopdfExe = os.path.join(self.curDir,'config/sub01.exe')
        self.annieExe = os.path.join(self.curDir,'config/sub02.exe')
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
        isSavePdf = self.savePdfEn.get()
        print("savePdfEn: " + str(isSavePdf))

        if(self.downloading == True):
            tkinter.messagebox.showinfo("MarkTool", "上次下载仍在进行中，请稍等...")
            return

        if(os.path.exists(self.wkhtmltopdfExe) and os.path.exists(self.annieExe)):
            pass
        else:
            tkinter.messagebox.showinfo('配置丢失','配置文件丢失，请勿删除config文件夹!')
            return False

        urls = self.tWebSites.get("1.0", "30.end").split('\n')
        urls = [i for i in urls if i != ''] # 删除所有空元素
        self.downloading = True

        try:
            self.webDwnldFunc(urls, isSavePdf)
        except Exception as e:
            print(e)
            print('download error:' + self.downloadType)

        self.lDldProcessText.config(text="下载完成！", font=("宋体", 12))
        self.downloading = False

    def run_progressbar(self, cur, max):
        self.lDldProcess["maximum"] = max
        self.lDldProcess["value"] = cur   # increment progressbar
        self.lDldProcess.update()       # have to call update() in loop

        process = "已下载：{}/{}".format(cur,max)
        self.lDldProcessText.config(text=process, font=("宋体", 12))

    def webDwnldFunc(self, urls, savePdfEn):
        dld = MarkWebDownload()
        options = {
            'margin-top': '0mm',
            'margin-bottom': '0mm',
            'encoding': "UTF-8",
            'enable-plugins': None,
            'enable-forms': None,
            'stop-slow-scripts': None,
        }

        webSaveDir = os.path.join(self.saveDir , 'webSite')
        if(os.path.exists(webSaveDir) == False):
            os.makedirs(webSaveDir)

        for idx,url in enumerate(urls):
            self.run_progressbar(idx, len(urls))
            dld.url2pdf(url, self.wkhtmltopdfExe, webSaveDir, options, savePdfEn)
        self.run_progressbar(len(urls), len(urls))

    def zhihuDwnldFunc(self, urls):
        print(urls)

    def videoDwnldFunc(self, urls):
        dld = MarkVideoDownload()
        videoSaveDir = os.path.join(self.saveDir , 'video')
        if(os.path.exists(videoSaveDir) == False):
            os.makedirs(videoSaveDir)

        for idx,url in enumerate(urls):
            process = "已下载：{}/{}".format(idx+1,len(urls))
            self.lDldProcess.config(text=process, font=("宋体", 12))
            dld.url2video(url, self.annieExe, videoSaveDir)

    def thread_it(self, func, *args):
        '''将函数打包进线程'''
        # 创建
        try:
            t = threading.Thread(target=func, args=args)
            # 守护 !!!
            t.setDaemon(True)
            # 启动
            t.start()
            # 阻塞--卡死界面！
            # t.join()
        except:
            self.downloading = False

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