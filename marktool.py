# -*- coding:utf-8*-
import os, base64
import webbrowser,requests
import tkinter.filedialog
import tkinter.messagebox
from tkinter import *    #注意模块导入方式，否则代码会有差别
from tkinter import ttk
from asset import asset
from markUrlDownload.markUrlDownloadGui import MarkUrlDownloadGui
from pdfMerge.pdfMergeGui import PdfMergeGui
from about import About

class Application(object):
    def __init__(self):
        self.title = 'MarkTool - 互联网信息工作站'
        self.version= 'V_1.1.1' #版本规则：框架改动.功能改动.问题修复
        print("Application init")

    def setWin(self):
        # 第1步，实例化object，建立窗口window
        window = tkinter.Tk()
        
        # 第2步，给窗口的可视化起名字
        window.title(self.title)
        window.resizable(0, 0)# 设置窗口宽高固定，如果放到geometry后面会闪一下

        # 第3步，设定窗口的大小(长 * 宽)、图标
        winWidth = 1200
        winHeight = 750
        # 获取屏幕分辨率
        screenWidth = window.winfo_screenwidth()
        screenHeight = window.winfo_screenheight()
        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)
        # 设置窗口初始位置在屏幕居中
        window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        # 设置窗口图标
        with open('tmp.ico','wb') as tmp:
            tmp.write(base64.b64decode(asset.Icon().img))
        window.iconbitmap('tmp.ico')
        os.remove('tmp.ico')

        # 设置分页
        tab = ttk.Notebook(window)

        urlDownloadFram = tkinter.Frame(tab)
        tab.add(urlDownloadFram, text = "网页下载")

        pdfMergeFram = tkinter.Frame(tab)
        tab.add(pdfMergeFram, text = "PDF合并")

        # zhihuDownloadFram = tkinter.Frame(tab)
        # tab.add(zhihuDownloadFram, text = "知乎下载")

        # videoDownloadFram = tkinter.Frame(tab)
        # tab.add(videoDownloadFram, text = "视频下载")
        
        aboutFram = tkinter.Frame(tab)
        tab.add(aboutFram, text = "关于")
        
        tab.pack(expand = True, fill = tkinter.BOTH)
        
        # 设置选中urlDownloadFram
        tab.select(urlDownloadFram)
        
        # ---------底部声明---------
        bottomFram2 = Frame(window)
        link = tkinter.Label(bottomFram2, text='官方主页：一番码客    ', font=("华文行楷", 12), fg='red',cursor="hand2")
        link.pack(side=RIGHT)
        bottomFram2.pack(side=LEFT)
        def open_index(event):
            webbrowser.open_new("http://www.efonmark.com")
        link.bind("<Button-1>", open_index)

        bottomFram1 = Frame(window)
        tkinter.Label(bottomFram1, text='免费使用，欢迎分享，严禁倒卖！', font=("华文行楷", 12), fg='green').pack(side=LEFT)
        bottomFram1.pack(side=LEFT)

        bottomFram4 = Frame(window)
        link1 = tkinter.Label(bottomFram4, text='获取最新版本', font=("华文行楷", 12),fg='red',cursor="hand2")
        link1.pack(side=RIGHT)
        bottomFram4.pack(side=RIGHT)
        def getUpgrades(event):
            webbrowser.open_new("http://www.efonmark.com/efonmark-blog/efonmark_tools/")
        link1.bind("<Button-1>", getUpgrades)

        bottomFram3 = Frame(window)
        tkinter.Label(bottomFram3, text='当前版本:'+self.version+'   ', font=("宋体", 10,  "bold"), fg='green').pack(side=LEFT)
        bottomFram3.pack(side=RIGHT)

        # 拦截关闭事件
        def on_closing():
            if messagebox.askokcancel("退出", "确定退出吗？"):
                window.destroy()
        window.protocol("WM_DELETE_WINDOW", on_closing)

        MarkUrlDownloadGui(urlDownloadFram)
        PdfMergeGui(pdfMergeFram)
        About(aboutFram)

        # ---------主窗口循环显示---------
        window.mainloop()
        
if __name__ == "__main__":  #这里可以判断，当前文件是否是直接被python调用执行
    url2pdfObj = Application()
    url2pdfObj.setWin()