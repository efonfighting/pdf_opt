import pdfkit
import os

class MarkWebDownload(object):
    def __init__(self):
        print("urlDownload init")

    def url2pdf(self, url, exeFile, pdfPath, ops):
        '''
        通过wkhtmltopdf下载url/html为pdf
        :param url : 要保存的url
        :param exeFile : wkhtmltopdf.exe路径
        :param saveDir : 下载内容保存的目录
        :return False : wkhtmltopdf.exe 不可用
        :return True : 下载成功
        '''
        print("exeFile ： " + exeFile )
        if(os.path.exists(exeFile)):
            pass
        else:
            print('请选择正确的wkhtmltopdf.exe路径')
            return False

        config = pdfkit.configuration(wkhtmltopdf=exeFile)
        try:
            pdfkit.from_url(url, pdfPath, options=ops, configuration=config)
            print("download finished : " + url + " ---> " + pdfPath)
        except:
            print("download error : " + url)
            pass

        return True

    def url2html(self, url, saveDir):
        '''
        url保存为本地html，带图片
        :param url : 要保存的url
        :param exeFile : wkhtmltopdf.exe路径
        :param saveDir : 下载内容保存的目录
        :return False : wkhtmltopdf.exe 不可用
        :return True : 下载成功
        '''
        return True