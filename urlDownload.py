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
from configobj import ConfigObj

import threading


class Url2pdf(object):
    def __init__(self):
        self.title = '一番码客 - 网页下载工具'
        self.version= 'V_1.1.1' #版本规则：框架改动.功能改动.问题修复
        self.downloading = False
        self.paramInit()
        print("Url2pdf init")

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
        self.saveDir = os.getcwd() 

    def paramSet(self):
        f= open("pdfmerge_config.ini","w+")
        f.close()
        config = ConfigObj("pdfmerge_config.ini",encoding='UTF8')  
        config['PATH_PRRA'] = {}
        config['PATH_PRRA']['exeFile'] = self.exeFile
        config['PATH_PRRA']['saveDir'] = self.saveDir
        config.write()



    def setWin(self):
        # 第1步，实例化object，建立窗口window
        window = tkinter.Tk()
        
        # 第2步，给窗口的可视化起名字
        window.title(self.title)
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
        tkinter.Label(frame1_fm00, text='请输入您想要下载的网址，每个网址换行输入，一次最多可输入30个网址：', font=("华文行楷", 13), fg='blue').grid()

        #frame1_fm01
        self.tWebSites = tkinter.Text(frame1_fm01, height=30, width=125)
        self.tWebSites.grid()

        #frame1_fm02
        tkinter.Button(frame1_fm02, text='开始下载为PDF', bg="#BC8F8F", font=('宋体', 14), command=lambda : self.thread_it(self.startDownload)).grid(row=2, column=0, stick=W)
        self.lDldProcess = tkinter.Label(frame1_fm02, text='', font=("宋体", 10))
        self.lDldProcess.grid(row=2, column=1, padx=8, sticky=W)

        #frame1_fm03
        self.lSaveDir = tkinter.Label(frame1_fm03, text="保存路径："+self.saveDir, font=("宋体", 10, "bold"))
        self.lSaveDir.grid(row=3, column=0, sticky=W)
        tkinter.Button(frame1_fm03, text='打开', font=('宋体', 10), command=lambda : self.thread_it(self.openDir, self.saveDir)).grid(row=3, column=1, padx=10)
        tkinter.Button(frame1_fm03, text='修改', font=('宋体', 10), command=self.getSaveDir).grid(row=3, column=2, sticky=W)

        #frame1_fm04
        self.lWkhtmlPath = tkinter.Label(frame1_fm04, text="wkhtmltopdf.exe路径：" + self.exeFile, font=("宋体", 10, "bold"))
        self.lWkhtmlPath.grid(row=4, column=0, sticky=W)
        tkinter.Button(frame1_fm04, text='修改', font=('宋体', 10), command=self.getWkhtmlPath).grid(row=4, column=1, padx=10, stick=E)

        # ---------第2页---------
        funcDes =   '\n'\
                    '功能说明：\n\n'\
                    '1.输入批量网址，将网址转换为pdf保存到本地。\n\n'\
                    '2.一次最多支持30个网址下载。\n\n'\
                    '3.如有无法访问网址，将自动跳过。\n\n'\
                    '\n'\
                    '使用说明:\n\n'\
                    '1.首先安装wkhtml2pdf.exe，采用默认安装即可。\n\n'\
                    '2.请输入您想要下载的网址，每个网址换行输入。\n\n'\
                    '3.点击“开始下载为PDF”，可以看到下载进度。 \n\n'\
                    '4.保存路径默认为当前路径，可以点击“修改”设置为其他目录。 \n\n'\
                    '5.如果提示“请选择正确的wkhtmltopdf.exe路径”，点击“修改”设置wkhtmltopdf.exe安装路径。\n\n'\
                    '6.wkhtmltopdf.exe默认安装路径为C:/Program Files/wkhtmltopdf/bin/。\n\n'\
                    '\n'\
                    '其他说明:\n\n'\
                    '1.版本持续升级，请点击“获取最新版本”。\n\n'\
                    '2.有任何问题或建议，请“联系作者”。\n\n'\

        fram2_fm1 = Frame(frame2)
        tkinter.Label(fram2_fm1, text=funcDes, font=("楷书", 13), justify = 'left').pack(anchor=N, side=LEFT)
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
                    '* 2020-02-23 V_1.1.1\n'\
                    '  1.url转PDF保存到本地。\n'\
                    '  2.下载进度展示栏。\n'\
                    '  3.保存目录的选择、展示、打开。\n'\
                    '  4.获取最新版本链接。\n'\
                    '  4.wkhtml和保存路径可保存。\n'\
                    '========================\n'

        fram4_fm1 = Frame(frame4)
        tkinter.Label(fram4_fm1, text=versionDes, font=("楷书", 12), justify = 'left').pack(anchor=N, side=LEFT)
        fram4_fm1.pack(side=TOP, fill=BOTH, expand=YES)

        # ---------主窗口循环显示---------
        window.mainloop()

    def openDir(self, path):
        try:
            os.system("start explorer {}".format(path.replace('/','\\')))
        except:
            print('打开{}失败'.format(path))
            return
        

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

    def getWkhtmlPath(self):
        ret = tkinter.filedialog.askopenfilename(filetypes=[("EXE",".exe")])
        if(ret != ""):
            self.exeFile = ret.replace("\\",'/')
            print(self.exeFile)
            self.lWkhtmlPath.config(text="wkhtmltopdf.exe路径：" + self.exeFile, font=("宋体", 10, "bold"))
            self.paramSet()

    def getSaveDir(self):
        ret = tkinter.filedialog.askdirectory()
        if(ret != ""):
            self.saveDir = ret.replace("\\",'/')
            print(self.saveDir)
            self.lSaveDir.config(text="保存路径："+self.saveDir, font=("宋体", 10, "bold"))
            self.paramSet()

    def startDownload(self):
        print(self.exeFile)
        print(self.saveDir)
        if(self.downloading == True):
            print("正在下载中")
            return
        
        if(os.path.exists(self.exeFile) and self.exeFile.find('wkhtmltopdf.exe') != -1):
            self.downloading = True
            pass
        else:
            tkinter.messagebox.showinfo(self.title,'请选择正确的wkhtmltopdf.exe路径')
            return False
        
        urls = self.tWebSites.get("1.0", "30.end").split('\n')
        urls = [i for i in urls if i != ''] # 删除所有空元素
        print(urls)
        config = pdfkit.configuration(wkhtmltopdf=self.exeFile)
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
        for idx,url in enumerate(urls):
            print(url)
            pdfPath = self.saveDir + '/{}.pdf'.format(idx+1)
            print(pdfPath)
            #wkhUrl2pdfWindows(url, saveDir + '/{}.pdf'.format(idx))
            process = "正在下载：{}/{}".format(idx+1,len(urls))
            self.lDldProcess.config(text=process, font=("宋体", 12))
            try:
                pdfkit.from_url(url, pdfPath, options=options, configuration=config)
            except:
                pass
            
        self.lDldProcess.config(text="下载完成！", font=("宋体", 12))
        self.downloading = False
        #tkinter.messagebox.showinfo(self.title,'下载完成！')

    def saveUrl(self, url, picName):
        '''
        保存url内容
        :param url : 要保存的url
        :param picName : 保存文件路径
        :return : 获取到的url内容长度
        '''
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

    def wkhUrl2pdfWindows(self, url, pdfName):
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


    def getFileName(self, filepath):
        file_list = sorted(glob.glob("{}*.pdf".format(filepath) ),key=os.path.getmtime, reverse=False)
        # 默认安装字典序排序，也可以安装自定义的方式排序
        # file_list.sort()
        return file_list


if __name__ == "__main__":  #这里可以判断，当前文件是否是直接被python调用执行
    url2pdfObj = Url2pdf()
    url2pdfObj.setWin()