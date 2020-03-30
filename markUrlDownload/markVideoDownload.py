import pdfkit
import os
import subprocess

class MarkVideoDownload(object):
    def __init__(self):
        print("MarkVideoDownload init")

    def url2video(self, url, exeFile, saveDir):
        '''
        通过annie下载url中的视频
        :param url : 要保存的url
        :param exeFile : annie.exe路径
        :param saveDir : 下载内容保存的目录
        :return False : annie.exe 不可用
        :return True : 下载成功
        '''
        retval = 0
        print("exeFile ： " + exeFile)
        if(os.path.exists(exeFile)):
            pass
        else:
            print('请选择正确的annie.exe路径')
            return False

        p = subprocess.Popen([exeFile, url, '-o', saveDir], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        retval = p.wait()
        print("download finished [{}]:{} ---> {}".format(retval, url, saveDir))

        return bool(retval)