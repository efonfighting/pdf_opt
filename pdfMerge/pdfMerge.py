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
import base64
import webbrowser
from PIL import Image, ImageTk

class PdfMerge(object):
    def __init__(self, processBar, processBarText):
        self.processBar = processBar
        self.processBarText = processBarText
        print("PdfMerge init")

    def getFileName(self, filepath):
        file_list = sorted(glob.glob("{}*.pdf".format(filepath) ),key=os.path.getmtime, reverse=False)
        # 默认安装字典序排序，也可以安装自定义的方式排序
        # file_list.sort()
        return file_list

    ##########################合并filepath文件夹下所有PDF文件########################
    def MergePDF(self, filepath, fileNameList, outfile):
        output = PdfFileWriter()
        outputPages = 0

        for idx,each_file in enumerate(fileNameList):
            print("adding %s" % each_file)
            self.run_progressbar(idx, len(fileNameList))
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
        self.run_progressbar(len(fileNameList), len(fileNameList))
        self.processBarText.config(text="合并完成！", font=("宋体", 12))
        print("finished")


    def MergePDFWithStep(self, filepath, outfile, step):
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

    def run_progressbar(self, cur, max):
        self.processBar["maximum"] = max
        self.processBar["value"] = cur   # increment progressbar
        self.processBar.update()       # have to call update() in loop

        process = "已合并：{}/{}".format(cur,max)
        self.processBarText.config(text=process, font=("宋体", 12))