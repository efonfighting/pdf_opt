# -*- coding:utf-8*-
import os
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter.scrolledtext as ScrolledText
import time
import glob
import tkinter.filedialog
import tkinter.messagebox
from tkinter import *    #注意模块导入方式，否则代码会有差别
from tkinter import ttk
import base64
import webbrowser
from PIL import Image, ImageTk
from pdfMerge.pdfMerge import PdfMerge
import threading
import external.ToolTip as tt
import subprocess 

class PdfMergeGui(object):
    def __init__(self, tkFrame):
        print("PdfMergeGui init")
        self.saveDir = "C:/Users"

        subFm00 = Frame(tkFrame)
        subFm01 = Frame(tkFrame)
        subFm02 = Frame(tkFrame)
        subFm03 = tkinter.Frame(tkFrame)
        subFm04 = ttk.LabelFrame(tkFrame, text='说明')

        subFm00.grid(row=0, column=0,padx=1,pady=3,sticky=W)
        subFm01.grid(row=1, column=0,padx=1,pady=3,sticky=W)
        subFm02.grid(row=2, column=0,padx=1,pady=15,sticky=W)
        subFm03.grid(row=3, column=0,padx=1,pady=0,sticky=W)
        subFm04.grid(row=0, column=1,pady=5,rowspan=2,columnspan=1,sticky=W+E+N+S)        

        #subFm00
        tkinter.Button(subFm00, text='选择要合并的PDF文档', bg="#BC8F8F", font=('宋体', 14), command=self.getNameFiles).grid()
        # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高

        #subFm01
        self.t1 = ScrolledText.ScrolledText(subFm01, height=41, width=125,wrap="none")
        hbar = tkinter.Scrollbar(subFm01, orient=HORIZONTAL, command=self.t1.xview)
        self.t1.configure(xscrollcommand=hbar.set)
        self.t1.grid(padx=5)
        hbar.grid(sticky=EW)

        #subFm02
        b2 = tkinter.Button(subFm02, text='开始合并', bg="#BC8F8F", font=('宋体', 14), command=lambda : self.thread_it(self.startMerge)).grid(row=2, column=0, stick=W)

        self.lmergeProcess = ttk.Progressbar(subFm02, orient='horizontal', length=500, mode='determinate')
        self.lmergeProcess.grid(row=2, column=2, padx=8, sticky=W)

        self.lmergeProcessText = tkinter.Label(subFm02, text='', font=("宋体", 10))
        self.lmergeProcessText.grid(row=2, column=3, padx=8, sticky=W)

        #subFm03
        self.lSaveDir = tkinter.Label(subFm03, text="保存路径："+self.saveDir, font=("宋体", 10, "bold"),cursor="hand2", anchor = NW, width = 100)
        self.lSaveDir.grid(row=3, column=0, sticky=W)
        self.lSaveDir.bind("<Button-1>", lambda event:self.openDir(self.saveDir))
        tt.create_ToolTip(self.lSaveDir, "点击打开")

        instructText = \
        "▶ 功能说明：\
        \n      1.合并后的文档带目录。\
        \n      2.最多支持400个文档的合并。\
        \n      3.如有损坏文件，将自动跳过。\
        \n\
        \n▶ 使用说明:\
        \n      1.点击“选择要合并的文档”。\
        \n      2.如需调整顺序，在文本框内直接编辑。\
        \n      3.保证路径的完整性，一个文件一行。\
        \n      4.点击“开始合并”。\
        \n      5.选择保存路径并输入保存名称。\
        "
        ttk.Label(subFm04, text = instructText).grid(sticky=W, padx=12,pady=6)

    # 获取路径和命名
    def getNameFiles(self):
        pdfFiles = tkinter.filedialog.askopenfilenames()
        print(pdfFiles)
        for index in range(0, len(pdfFiles), 1):
            self.t1.insert('insert', pdfFiles[index]+'\n')
        print(self.t1.get("1.0", "400.end"))

    def startMerge(self):
        mergeIns = PdfMerge(self.lmergeProcess, self.lmergeProcessText)
        mergedName = tkinter.filedialog.asksaveasfilename(filetypes=[("PDF",".pdf")])
        self.saveDir = os.path.dirname(mergedName)
        self.lSaveDir.config(text="保存路径："+self.saveDir, font=("宋体", 10, "bold"))
        print(mergedName)

         # 获取列表并去除空元素
        fileList = self.t1.get("1.0", "400.end").split('\n') # 最多400个
        def stripList(x):
            return x and x.strip()
        fileList = list(filter(stripList, fileList))

        mergeIns.MergePDF(os.path.dirname(fileList[0]), fileList, mergedName+'.pdf')

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
            # os.system("start explorer {}".format(path.replace('/','\\')))
            subprocess.call(["start", "explorer", path.replace('/','\\')],shell=True)
        except:
            print('打开{}失败'.format(path))
            return
