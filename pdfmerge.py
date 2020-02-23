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
import webbrowser,requests
from PIL import Image, ImageTk
import pdfkit


def saveUrl(url, picName):
    '''
    保存url内容
    :param url : 要保存的url
    :param picName : 保存文件路径
    :return : 获取到的url内容长度
    '''
    contLen = 0
    try:
        urlCont = requests.get(url, timeout=20).content
        contLen = len(urlCont)

        if (contLen == 0): # 第一次失败则再尝试一次
            print("get url failed,try again.")
            urlCont = requests.get(url, timeout=20).content
            contLen = len(urlCont)

        if (contLen != 0):
            open(picName, 'wb').write(urlCont)
            print("get url ok:", contLen)
        else:
            print("get url failed.")
    except Exception:
        print("get url Exception.")
    return contLen

def wkhUrl2pdfWindows(url, pdfName):
    '''
    通过(title , url)文档打印为pdf文档
        * 为了解决wkhtmltopdf部分图片失真的问题，把网页中所有的图片保存到本地并用convert转换格式，修改html img src路径为本地相对路径
        * 需要安装wkhtmltopdf工具，需要linux环境
    '''

    import urllib.request
    import os,sys
    os.chdir(sys.path[0])
    fileDir = os.path.dirname(pdfName) #获取目录的绝对路径
    title = pdfName.replace(fileDir + '/', '')

    htmlDir = fileDir + '/html/' + title.replace('.pdf', '')
    pdfDir = fileDir + '/pdf/'
    if not os.path.exists(htmlDir):
        os.mkdir(htmlDir)
    htmlName = '{}/essay.html'.format(htmlDir)

    for i in range(10): #防止访问时间过长造成假死
        try:
            html = open_url(url).decode("UTF-8") #read出的是bytes，使用前需要转换为str类型
        except Exception:
            if i >= 9:
                print("requests failed and return.")
                return
            else:
                time.sleep(1)
        else:
            break

    pattern = re.compile(r'data-src=\"http.*?\"')  # 用?来控制正则贪婪和非贪婪匹配;(.*?) 小括号来控制是否包含匹配的关键字
    result = pattern.findall(html)

    picCnt = 0
    for i in result:
        picCnt = picCnt + 1
        url = re.findall(r'\"(.*?)\"', i)[0]
        print(picCnt, " : ", url)
        if (len(re.findall("wx_fmt", url)) == 0): # 有可能是视频，判断是否是图片
            print("url is not a pic")
            continue

        picName = '{}/{}.png'.format(htmlDir, str(picCnt))
        picDir = os.path.dirname(picName)
        picNameOnly = picName.replace(picDir+'/', '') # 转换为相对路径
        html = html.replace(url, picNameOnly)
        if(saveUrl(url, picName) == 0):
            continue
        #os.system('wget {} -O {} > /dev/null 2>&1'.format(url, picName))
        #convertCmd = 'convert {}[0] {}'.format(picName, picName)
        #print(convertCmd)
        #os.system(convertCmd)
    html = html.replace('data-src','src').replace('quotes: none;','')
    html = html + '<a href>声明：pdf仅供学习使用，一切版权归原创公众号所有；建议持续关注原创公众号获取最新文章，学习愉快！</a>'
    fd = open(htmlName, 'w', encoding="utf-8")
    fd.write(html)
    fd.close()

    #os.system('wkhtmltopdf --enable-plugins --enable-forms --margin-bottom 0 --margin-top 0 {} {} > /dev/null 2>&1'.format(htmlName, pdfDir + '/' + title))
    #os.remove(htmlName)
    #os.system('rm {}/*.png'.format(fileDir))
    print("下载成功")


def getFileName(filepath):
    file_list = sorted(glob.glob("{}*.pdf".format(filepath) ),key=os.path.getmtime, reverse=False)
    # 默认安装字典序排序，也可以安装自定义的方式排序
    # file_list.sort()
    return file_list

if __name__ == "__main__":  #这里可以判断，当前文件是否是直接被python调用执行
    exeFile = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    
    saveDir = os.getcwd()
    # 获取wkhtmltopdf路径和命名
    def getWkhtmlPath():
        global exeFile
        exeFile = tkinter.filedialog.askopenfilename(filetypes=[("EXE",".exe")])
        print(exeFile)
        lWkhtmlPath.config(text=exeFile, font=("宋体", 12))

    def getSaveDir():
        global saveDir
        saveDir = tkinter.filedialog.askdirectory()
        print(saveDir)
        lSaveDir.config(text=saveDir, font=("宋体", 12))

    # 获取保存路径
    def startDownload():
        global saveDir
        print(exeFile)
        print(saveDir)
        if(os.path.exists(exeFile) and exeFile.find('wkhtmltopdf.exe')):
            pass
        else:
            tkinter.messagebox.showinfo(title,'请选择正确的wkhtmltopdf.exe路径')
            return False
        
        urls = tWebSites.get("1.0", "20.end").split('\n')
        urls = [i for i in urls if i != ''] # 删除所有空元素
        print(urls)
        config = pdfkit.configuration(wkhtmltopdf=exeFile)
        options = {
            #'page-size': 'A4',
            'margin-top': '0mm',
            'margin-right': '0mm',
            'margin-bottom': '0mm',
            'margin-left': '0mm',
            # 'orientation':'Landscape',#横向
            'encoding': "UTF-8",
            'no-outline': None,
            # 'footer-right':'[page]' 设置页码
        }
        for idx,url in enumerate(urls):
            print(url)
            pdfPath = saveDir + '/{}.pdf'.format(idx)
            print(pdfPath)
            #wkhUrl2pdfWindows(url, saveDir + '/{}.pdf'.format(idx))
            try:
                pdfkit.from_url(url, pdfPath, options=options, configuration=config)
            except:
                pass

        tkinter.messagebox.showinfo(title,'下载完成！')

    # 第1步，实例化object，建立窗口window
    window = tkinter.Tk()
    
    # 第2步，给窗口的可视化起名字
    version= 'V_0.0.1' #版本规则：框架改动.功能改动.问题修复
    title = '一番码客 - 网址保存为PDF - ' + version
    window.title(title)
    window.resizable(0, 0)# 设置窗口宽高固定，如果放到geometry后面会闪一下

    # 第3步，设定窗口的大小(长 * 宽)、图标
    winWidth = 900
    winHeight = 600
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
    tab.add(frame1, text = "主页面")
    
    frame2 = tkinter.Frame(tab)
    tab.add(frame2, text = "使用说明")
    
    frame3 = tkinter.Frame(tab)
    tab.add(frame3, text = "联系作者")
    
    frame4 = tkinter.Frame(tab)
    tab.add(frame4, text = "版本说明")

    tab.pack(expand = True, fill = tkinter.BOTH)
    
    # 设置选中frame1
    tab.select(frame1)
    
    # ---------第1页---------
    #先画出容器
    frame1_fm00 = tkinter.Frame(frame1)
    frame1_fm01 = tkinter.Frame(frame1)
    frame1_fm02 = tkinter.Frame(frame1)
    frame1_fm03 = tkinter.Frame(frame1)
    frame1_fm04 = tkinter.Frame(frame1)

    frame1_fm00.grid(row=0, column=0,padx=1,pady=3,sticky=W)
    frame1_fm01.grid(row=1, column=0,padx=1,pady=3,sticky=W)
    frame1_fm02.grid(row=2, column=0,padx=1,pady=15,sticky=W)
    frame1_fm03.grid(row=3, column=0,padx=1,pady=0,sticky=W)
    frame1_fm04.grid(row=4, column=0,padx=1,pady=0,sticky=W)

    #frame1_fm00
    tkinter.Label(frame1_fm00, text='请输入你想要下载的网址，每个网址换行输入，最多一次输入20个网址：', font=("华文行楷", 13), fg='blue').grid()

    #frame1_fm01
    tWebSites = tkinter.Text(frame1_fm01, height=30, width=125)
    tWebSites.grid()

    #frame1_fm02
    tkinter.Button(frame1_fm02, text='开始下载为PDF', bg="#BC8F8F", font=('宋体', 14), command=startDownload).grid(sticky=W)
    
    #frame1_fm03
    tkinter.Button(frame1_fm03, text='修改下载保存路径', bg="#BC8F8F", font=('宋体', 10), command=getSaveDir).grid(row=3, column=0, sticky=W)
    lSaveDir = tkinter.Label(frame1_fm03, text=saveDir, font=("宋体", 10), fg='blue')
    lSaveDir.grid(row=3, column=1, sticky=W)

    #frame1_fm04
    tkinter.Button(frame1_fm04, text='修改wkhtmltopdf.exe所在路径', bg="#BC8F8F", font=('宋体', 10), command=getWkhtmlPath).grid(row=4, column=0, sticky=W)
    lWkhtmlPath = tkinter.Label(frame1_fm04, text=exeFile, font=("宋体", 10), fg='blue')
    lWkhtmlPath.grid(row=4, column=1, sticky=W)
    
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