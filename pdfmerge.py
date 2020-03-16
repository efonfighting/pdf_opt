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


def getFileName(filepath):
    file_list = sorted(glob.glob("{}*.pdf".format(filepath) ),key=os.path.getmtime, reverse=False)
    # 默认安装字典序排序，也可以安装自定义的方式排序
    # file_list.sort()
    return file_list

##########################合并filepath文件夹下所有PDF文件########################
def MergePDF(filepath, fileNameList, outfile):
    output = PdfFileWriter()
    outputPages = 0

    for each_file in fileNameList:
        print("adding %s" % each_file)
        # 读取源pdf文件
        try:
            input = PdfFileReader(open(each_file, "rb"))
        except:
            print("{} is a bad pdf, skip it.".format(each_file))
            continue

        # 如果pdf文件已经加密，必须首先解密才能使用pyPdf
        if input.isEncrypted == True:
            input.decrypt("map")

        # print(each_file[:-4])

        # 获得源pdf文件中页面总数
        pageCount = input.getNumPages()
        outputPages += pageCount
        #print("%s has %d pages" % (each_file, pageCount))

        # 分别将page添加到输出output中
        for iPage in range(pageCount):
            output.addPage(input.getPage(iPage))

        # 添加书签
        output.addBookmark(
            title=each_file[:-3].replace(filepath+'/',''), pagenum=outputPages - pageCount)

    print("All Pages Number: " + str(outputPages))
    # 最后写pdf文件
    outputStream = open(outfile, "wb")
    output.write(outputStream)
    outputStream.close()
    print("finished")


def MergePDFWithStep(filepath, outfile, step):
    print('{}:{}:{}'.format(filepath, outfile, step))
    time1 = time.time()
    file_dir = '.'
    pdf_fileName = getFileName(filepath)
    fileCnt = len(pdf_fileName)
    mergeCnt = int(fileCnt / step)
    for i in range(mergeCnt):
        MergePDF(filepath, pdf_fileName[i*step:(i+1)*step],"{}_{}_{}.pdf".format(outfile,i*step+1,(i+1)*step))
    MergePDF(filepath, pdf_fileName[mergeCnt*step:],"{}_{}_{}.pdf".format(outfile,mergeCnt*step+1,fileCnt))
    time2 = time.time()
    print('总共耗时： %.4f s' % (time2 - time1))

if __name__ == "__main__":  #这里可以判断，当前文件是否是直接被python调用执行
    # 获取路径和命名
    def getNameFiles():
        pdfFiles = tkinter.filedialog.askopenfilenames()
        print(pdfFiles)
        for index in range(0, len(pdfFiles), 1):
            t1.insert('insert', pdfFiles[index]+'\n')
        print(t1.get("1.0", "400.end"))

    def startMerge():
        mergedName = tkinter.filedialog.asksaveasfilename(filetypes=[("PDF",".pdf")])
        print(mergedName)
        fileList = t1.get("1.0", "400.end").split('\n') # 最多400个
        filePath = os.path.dirname(fileList[0])
        MergePDF(filePath, fileList, mergedName+'.pdf')


    # 第1步，实例化object，建立窗口window
    window = tkinter.Tk()
    
    # 第2步，给窗口的可视化起名字
    version= 'V_1.1.1' #版本规则：框架改动.功能改动.问题修复
    title = '一番码客 - PDF合并软件 - ' + version
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
    fram1_fm1 = Frame(frame1)
    tkinter.Button(fram1_fm1, text='选择要合并的PDF文档', bg="#BC8F8F", font=('Arial', 14), command=getNameFiles).pack(side=LEFT)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    fram1_fm1.pack(side=TOP, fill=BOTH, expand=YES)

    fram1_fm2 = Frame(frame1)
    t1 = tkinter.Text(fram1_fm2, height=30, width=110)
    t1.pack(side=LEFT)
    fram1_fm2.pack(side=TOP, fill=BOTH, expand=YES)

    fram1_fm3 = Frame(frame1)
    b2 = tkinter.Button(fram1_fm3, text='开始合并', bg="#BC8F8F", font=('Arial', 14), command=startMerge).pack(side=LEFT)
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