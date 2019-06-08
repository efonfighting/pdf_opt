# -*- coding:utf-8*-

import os
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter
import time
import glob
import tkinter.filedialog
import tkinter.messagebox
from tkinter import *    #注意模块导入方式，否则代码会有差别
'''
reference:
    打包exe: ' pyinstaller -F pdfmerge.py -w -i assert/efon.ico --version-file=assert/file_version_info.txt'
    info：C:/Users/xxx/AppData/Local/Programs/Python/Python37/Lib/site-packages/PyInstaller/utils/cliutils
    tkinter：https://www.cnblogs.com/shwee/p/9427975.html
    tkinter 消息框：https://www.cnblogs.com/buchizaodian/p/7076964.html
'''

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
    # 第5步，获取路径和命名
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
    title = '一番码客 - PDF合并软件 - V_0.0.1'
    window.title(title)

    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry('800x500')  # 这里的乘是小x

    def show_me():
        tkinter.messagebox.showinfo(title,'联系我:\n\n'
                                          '微信公众号【一番码客】: 发掘你关心的亮点!\n\n'
                                          '微信【Efon-fighting】: 请备注(一番工具)!\n\n'
                                          '邮箱【efongfighting@126.com】')
    def help():
        tkinter.messagebox.showinfo(title,'使用说明:\n\n'
                                          '1.选择要合并的文档。\n\n'
                                          '2.如果需要调整顺序，在文本框内调整顺序。\n\n'
                                          '3.开始合并，选择要保存的位置。\n\n'
                                          '\n'
                                          '功能说明：\n\n'
                                          '1.合并后的文档带目录。\n\n'
                                          '2.最多支持400个文档的合并。\n\n')

    about = tkinter.Menu(window)
    about.add_command(label='about', command=show_me)
    about.add_command(label='help', command=help)
    window.config(menu=about)

    # 第6步，创建并放置两个按钮分别触发两种情况
    fm2 = Frame(window)
    tkinter.Button(fm2, text='选择要合并的PDF文档', font=('Arial', 14), command=getNameFiles).pack(side=LEFT)
    var = tkinter.StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
    l = tkinter.Label(fm2, textvariable=var, font=('Arial', 12)).pack(side=LEFT)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    fm2.pack(side=TOP, fill=BOTH, expand=YES)

    fm3 = Frame(window)
    t1 = tkinter.Text(fm3, height=30, width=110)
    t1.pack(side=LEFT)
    fm3.pack(side=TOP, fill=BOTH, expand=YES)


    fm4 = Frame(window)
    b2 = tkinter.Button(fm4, text='开始合并', font=('Arial', 14), command=startMerge).pack(side=LEFT)
    fm4.pack(side=TOP, fill=BOTH, expand=YES)

    # 第8步，主窗口循环显示
    window.mainloop()


