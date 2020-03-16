import tkinter.filedialog
import tkinter.messagebox
from tkinter import *    #注意模块导入方式，否则代码会有差别
import threading
from configobj import ConfigObj
import os
from markUrlDownload.markUrlDownload import MarkUrlDownload
import datetime

class MarkUrlDownloadGui(object):
    def __init__(self, tkFrame):
        self.downloading = False
        self.paramInit()
        #先画出容器
        subFm00 = tkinter.Frame(tkFrame)
        subFm01 = tkinter.Frame(tkFrame)
        subFm02 = tkinter.Frame(tkFrame)
        subFm03 = tkinter.Frame(tkFrame)
        subFm04 = tkinter.Frame(tkFrame)

        subFm00.grid(row=0, column=0,padx=1,pady=3,sticky=W)
        subFm01.grid(row=1, column=0,padx=1,pady=3,sticky=W)
        subFm02.grid(row=2, column=0,padx=1,pady=15,sticky=W)
        subFm03.grid(row=3, column=0,padx=1,pady=0,sticky=W)
        subFm04.grid(row=4, column=0,padx=1,pady=0,sticky=W)

        #subFm00
        tkinter.Label(subFm00, text='请输入您想要下载的网址，每个网址换行输入，一次最多可输入30个网址：', font=("华文行楷", 13), fg='blue').grid()

        #subFm01
        self.tWebSites = tkinter.Text(subFm01, height=30, width=125)
        # self.tWebSites['background'] = '#FFCCCC'
        self.tWebSites.grid()

        #subFm02
        tkinter.Button(subFm02, text='开始下载为PDF', bg="#BC8F8F", font=('宋体', 14), command=lambda : self.thread_it(self.startDownload)).grid(row=2, column=0, stick=W)
        self.lDldProcess = tkinter.Label(subFm02, text='', font=("宋体", 10))
        self.lDldProcess.grid(row=2, column=1, padx=8, sticky=W)

        #subFm03
        self.lSaveDir = tkinter.Label(subFm03, text="保存路径："+self.saveDir, font=("宋体", 10, "bold"))
        self.lSaveDir.grid(row=3, column=0, sticky=W)
        tkinter.Button(subFm03, text='打开', font=('宋体', 10), command=lambda : self.thread_it(self.openDir, self.saveDir)).grid(row=3, column=1, padx=10)
        tkinter.Button(subFm03, text='修改', font=('宋体', 10), command=self.setSaveDir).grid(row=3, column=2, sticky=W)

        #subFm04
        self.lWkhtmlPath = tkinter.Label(subFm04, text="wkhtmltopdf.exe路径：" + self.exeFile, font=("宋体", 10, "bold"))
        self.lWkhtmlPath.grid(row=4, column=0, sticky=W)
        tkinter.Button(subFm04, text='修改', font=('宋体', 10), command=self.getWkhtmlPath).grid(row=4, column=1, padx=10, stick=E)

    def paramInit(self):
        if(os.path.exists("pdfmerge_config.ini")):
            config = ConfigObj("pdfmerge_config.ini",encoding='UTF8')
            self.exeFile = config['PATH_PRRA']['exeFile'].replace("\\",'/')
            self.saveDir = config['PATH_PRRA']['saveDir'].replace("\\",'/')
            print(self.exeFile)
            print(self.saveDir)
            if(self.exeFile == '' or self.saveDir == ''):
                print('get para failed')
                pass
            else:
                print('get para succeed')
                return
            # # 读配置文件
            # print(config['PATH_PRRA'])
            # print(config['PATH_PRRA']['exeFile'])
            # print(config['PATH_PRRA']['saveDir'])
        
        self.exeFile = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
        self.saveDir = os.getcwd().replace("\\",'/')

    def startDownload(self):
        if(self.downloading == True):
            print("正在下载中")
            return

        self.downloading = True
        dld = MarkUrlDownload()
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

        urls = self.tWebSites.get("1.0", "30.end").split('\n')
        urls = [i for i in urls if i != ''] # 删除所有空元素
        for idx,url in enumerate(urls):
            process = "正在下载：{}/{}".format(idx+1,len(urls))
            self.lDldProcess.config(text=process, font=("宋体", 12))
            pdfPath = os.path.join(self.saveDir , datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '.pdf')
            dld.url2pdf(url, self.exeFile, pdfPath, options)
            
        self.lDldProcess.config(text="下载完成！", font=("宋体", 12))
        self.downloading = False

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
            self.exeFile = ret.replace("\\",'/')
            print(self.exeFile)
            self.lWkhtmlPath.config(text="wkhtmltopdf.exe路径：" + self.exeFile, font=("宋体", 10, "bold"))
            self.paramSet()

    def setSaveDir(self):
        ret = tkinter.filedialog.askdirectory()
        if(ret != ""):
            self.saveDir = ret.replace("\\",'/')
            print(self.saveDir)
            self.lSaveDir.config(text="保存路径："+self.saveDir, font=("宋体", 10, "bold"))
            self.paramSet()

    def paramSet(self):
        f= open("pdfmerge_config.ini","w+")
        f.close()
        config = ConfigObj("pdfmerge_config.ini",encoding='UTF8')
        config['PATH_PRRA'] = {}
        config['PATH_PRRA']['exeFile'] = self.exeFile
        config['PATH_PRRA']['saveDir'] = self.saveDir
        config.write()