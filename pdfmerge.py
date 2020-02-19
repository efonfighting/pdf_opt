# -*- coding:utf-8*-

import os
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter
import time
import glob
import tkinter.filedialog
import tkinter.messagebox
from tkinter import *    #注意模块导入方式，否则代码会有差别
from tkinter import ttk
from asset.icon import Icon
from asset.efon import Efon
import base64
import webbrowser
from PIL import Image, ImageTk
import pdfkit


def getFileName(filepath):
    file_list = sorted(glob.glob("{}*.pdf".format(filepath) ),key=os.path.getmtime, reverse=False)
    # 默认安装字典序排序，也可以安装自定义的方式排序
    # file_list.sort()
    return file_list

if __name__ == "__main__":  #这里可以判断，当前文件是否是直接被python调用执行
    exeFile = ''
    # 获取路径和命名
    def getNameFile():
        global exeFile
        exeFile = tkinter.filedialog.askopenfilename(filetypes=[("EXE",".exe")])
        print(exeFile)
        L0.config(text=exeFile + '\n', font=("宋体", 12))

    # 获取保存路径
    def startDownload():
        print(exeFile)
        print(exeFile.find('wkhtmltopdf.exe'))
        if(exeFile.find('wkhtmltopdf.exe') == -1):
            tkinter.messagebox.showinfo(title,'请选择正确的wkhtmltopdf.exe路径')
            return False
        tkinter.messagebox.showinfo(title,'请选择下载文档所要保存的目录！')
        saveDir = tkinter.filedialog.askdirectory()
        print(saveDir)
        urls = t1.get("1.0", "20.end").split('\n')
        print(urls)
        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe')
        for idx,url in enumerate(urls):
            print(str(idx) + '.pdf : ' + url)
            pdfkit.from_url(url, saveDir + '{}.pdf'.format(idx), configuration=config)

    # 第1步，实例化object，建立窗口window
    window = tkinter.Tk()
    
    # 第2步，给窗口的可视化起名字
    version= 'V_0.0.1' #版本规则：框架改动.功能改动.问题修复
    title = '一番码客 - 批量网页转PDF - ' + version
    window.title(title)
    window.resizable(0, 0)# 设置窗口宽高固定，如果放到geometry后面会闪一下

    # 第3步，设定窗口的大小(长 * 宽)、图标
    winWidth = 800
    winHeight = 560
    # 获取屏幕分辨率
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = int((screenWidth - winWidth) / 2)
    y = int((screenHeight - winHeight) / 2)
    # 设置窗口初始位置在屏幕居中
    window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
    # 设置窗口图标
    with open('tmp.ico','wb') as tmp:
        tmp.write(base64.b64decode(Icon().img))
    window.iconbitmap('tmp.ico')
    os.remove('tmp.ico')
    # 设置分页
    tab = ttk.Notebook(window)

    frame1 = tkinter.Frame(tab)
    tab1 = tab.add(frame1, text = "主页面")
    
    frame2 = tkinter.Frame(tab)
    tab2 = tab.add(frame2, text = "使用说明")
    
    frame3 = tkinter.Frame(tab)
    tab3 = tab.add(frame3, text = "联系作者")
    
    frame4 = tkinter.Frame(tab)
    tab4 = tab.add(frame4, text = "版本说明")

    tab.pack(expand = True, fill = tkinter.BOTH)
    
    # 设置选中tab1
    tab.select(frame1)
    
    # ---------第1页---------
    fram1_fm0 = Frame(frame1)
    tkinter.Button(fram1_fm0, text='选择wkhtmltopdf.exe所在位置', bg="#BC8F8F", font=('Arial', 14), command=getNameFile).pack(side=LEFT)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    fram1_fm0.pack(side=TOP, fill=BOTH, expand=YES)

    fram1_fm01 = Frame(frame1)
    L0 = tkinter.Label(fram1_fm01, text='', font=("华文行楷", 13), fg='blue')
    L0.pack(side=LEFT)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    fram1_fm01.pack(side=TOP, fill=BOTH, expand=YES)

    fram1_fm1 = Frame(frame1)
    tkinter.Label(fram1_fm1, text='请输入你想要下载的网址，每个网址换行输入，最多一次输入20个网址：', font=("华文行楷", 13), fg='blue').pack(side=LEFT)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    fram1_fm1.pack(side=TOP, fill=BOTH, expand=YES)

    fram1_fm2 = Frame(frame1)
    t1 = tkinter.Text(fram1_fm2, height=30, width=110)
    t1.pack(side=LEFT)
    fram1_fm2.pack(side=TOP, fill=BOTH, expand=YES)

    fram1_fm3 = Frame(frame1)
    b2 = tkinter.Button(fram1_fm3, text='开始下载为PDF', bg="#BC8F8F", font=('宋体', 14), command=startDownload).pack(side=LEFT)
    fram1_fm3.pack(side=TOP, fill=BOTH, expand=YES)

    # ---------第2页---------
    funcDes =   '\n'\
                '功能说明：\n\n'\
                '1.合并后的文档带目录。\n\n'\
                '2.最多支持400个文档的合并。\n\n'\
                '3.如有损坏文件，将自动跳过\n\n'\
                 '\n'\
                '使用说明:\n\n'\
                '1.点击“选择要合并的文档”。\n\n'\
                '2.如果需要调整顺序，在文本框内直接编辑，请保证路径的完整性，一个文件一行。\n\n'\
                '3.点击“开始合并”，选择保存路径，输入合并后的文件名称。\n\n'

    fram2_fm1 = Frame(frame2)
    tkinter.Label(fram2_fm1, text=funcDes, font=("楷书", 14), justify = 'left').pack(anchor=N, side=LEFT)
    fram2_fm1.pack(side=TOP, fill=BOTH, expand=YES)

    # ---------第3页---------
    with open('tmp.jpg','wb') as tmp:
        tmp.write(base64.b64decode(Efon().img))

    fram3_fm1 = Frame(frame3)
    im = Image.open('tmp.jpg')
    tk_im = ImageTk.PhotoImage(im)
    tkinter.Label(fram3_fm1, image=tk_im).pack(side=LEFT)
    fram3_fm1.pack(side=TOP, fill=BOTH, expand=YES)

    os.remove('tmp.jpg')

    # ---------第4页---------
    versionDes =  '版本说明：\n'\
                '========================\n'\
                '* 2020-02-16 V_1.1.1\n'\
                '  1.完善pdf合并基本功能。\n'\
                '  2.添加多页选项\n'\
                '========================\n'

    fram4_fm1 = Frame(frame4)
    tkinter.Label(fram4_fm1, text=versionDes, font=("楷书", 12), justify = 'left').pack(anchor=N, side=LEFT)
    fram4_fm1.pack(side=TOP, fill=BOTH, expand=YES)

    # ---------底部声明---------
    def open_url(event):
        webbrowser.open_new("http://www.efonmark.com")

    bottomFram1 = Frame(window)
    tkinter.Label(bottomFram1, text='免费使用，欢迎分享，严禁倒卖！', font=("华文行楷", 12), fg='green').pack(side=LEFT)
    bottomFram1.pack(side=LEFT)

    bottomFram2 = Frame(window)
    link = tkinter.Label(bottomFram2, text='官方主页：一番码客', font=("华文行楷", 12), fg='red',cursor="hand2")
    link.pack(side=RIGHT)
    bottomFram2.pack(side=LEFT)

    link.bind("<Button-1>", open_url)

    # 主窗口循环显示
    window.mainloop()