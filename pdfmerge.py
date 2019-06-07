# -*- coding:utf-8*-

import os
import os.path
from PyPDF2 import PdfFileReader, PdfFileWriter
import time
import glob

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
    MergePDFWithStep('C:/Users/soy/Desktop/tmp/dist/',"判断",10)
