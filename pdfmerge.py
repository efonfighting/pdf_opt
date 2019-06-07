# -*- coding:utf-8*-

import os
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter
import time
import glob
import tkinter.filedialog

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
            title=each_file[:-3].replace(filepath,''), pagenum=outputPages - pageCount)

    print("All Pages Number: " + str(outputPages))
    # 最后写pdf文件
    outputStream = open(filepath + outfile, "wb")
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
    '''
    reference：https://www.cnblogs.com/shwee/p/9427975.html
    '''
    # 第1步，实例化object，建立窗口window
    window = tkinter.Tk()

    # 第2步，给窗口的可视化起名字
    window.title('一番码客 - PDF合并软件')

    # 第3步，设定窗口的大小(长 * 宽)
    window.geometry('500x300')  # 这里的乘是小x

    # 第4步，在图形界面上设定输入框控件entry框并放置
    tkinter.Label(window, text='输入合并后的文档名', bg='red', font=('Arial', 16)).pack()
    e = tkinter.Entry(window, show=None)  # 显示成明文形式
    e.pack()

    # 第5步，获取路径和命名
    def getFolder():
        pdfFolder = tkinter.filedialog.askdirectory() + '/'
        var.set(pdfFolder)

    def startMerge():
        pdfFolder = var.get()
        mergedName = e.get()
        MergePDFWithStep(pdfFolder, mergedName, 10)

    # 第6步，创建并放置两个按钮分别触发两种情况
    tkinter.Button(window, text='选择要合并的pdf所在文件夹', width=40, height=2, command=getFolder).pack()

    # 第7步，创建并放置一个多行文本框text用以显示，指定height=3为文本框是三个字符高度
    var = tkinter.StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
    l = tkinter.Label(window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30, height=2)
    # 说明： bg为背景，fg为字体颜色，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高
    l.pack()

    b2 = tkinter.Button(window, text='开始合并', width=10, height=2, command=startMerge)
    b2.pack()

    # 第8步，主窗口循环显示
    window.mainloop()


