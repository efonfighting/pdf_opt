import pdfkit
import re, os, sys, time
import urllib.request
from lxml import html
import datetime,random,requests
from bs4 import BeautifulSoup
from imgOpt import imgOpt

class MarkWebDownload(object):
    def __init__(self):
        print("MarkWebDownload init")

    def url2pdf(self, url, exeFile, pdfPath, ops, savePdfEn):
        '''
        通过wkhtmltopdf下载url/html为pdf
        :param url : 要保存的url
        :param exeFile : wkhtmltopdf.exe路径
        :param saveDir : 下载内容保存的目录
        :return False : wkhtmltopdf.exe 不可用
        :return True : 下载成功
        '''
        pdfPath = pdfPath.replace("\\", "/")
        print("exeFile ： " + exeFile )
        if(os.path.exists(exeFile)):
            pass
        else:
            print('请选择正确的wkhtmltopdf.exe路径')
            return False

        config = pdfkit.configuration(wkhtmltopdf=exeFile)
        try:
            htmlPath = self.url2html(url, pdfPath).replace("\\", "/")
            htmlName = os.path.split(htmlPath)[-1].replace(".html","")
            if savePdfEn:
                print("HTML转换PDF中...")
                pdfkit.from_file(htmlPath, pdfPath+f'/{htmlName}.pdf', options=ops, configuration=config)
            print("download finished : " + url + " ---> " + pdfPath)
        except Exception as e:
            print("download error : " + url)
            print(e)
            return False
            pass

        return True

    def url2html(self, url, savePath):
        '''
        url保存为本地html，带图片
        :param url : 要保存的url
        :param savePath : 下载内容保存的文件夹的绝对路径
        :return htmlTitle : html名字
        '''
        if(os.path.exists(savePath) == False):
            os.makedirs(savePath)
            print("mkdir:{}".format(savePath))
        for i in range(10): #防止访问时间过长造成假死
            try:
                htmlCont = self.open_url(url)
                htmlCont = htmlCont.decode("utf-8", "ignore") #read出的是bytes，使用前需要转换为str类型
                soup = BeautifulSoup(htmlCont, "html.parser")
                htmlTitle = soup.title.string
                if(htmlTitle == '\n'): # 例如微信文章
                    htmlTitle = re.findall(r'<meta property=\"og:title\" content=\"(.*?)\"', htmlCont)[0] #用?来控制正则贪婪和非贪婪匹配;(.*?) 小括号来控制是否包含匹配的关键字  
                nowTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                htmlTitle = nowTime+'_'+htmlTitle
                special_flag = ['(', ')', '|', ' ', '/', '*', '\\', '.', '<', '>', '&', '?', ':', ',', ';', '"', '\'', '`']
                for flg in special_flag:
                    htmlTitle = htmlTitle.replace(flg, '-')

                realSaveDir = savePath + '/' + htmlTitle
                if(os.path.exists(realSaveDir) == False):
                    os.makedirs(realSaveDir)
                    print("mkdir:{}".format(realSaveDir))
                htmlPath = realSaveDir + '/' + htmlTitle + '.html'
                
                img_src = soup.findAll("img")
            except Exception as e:
                print(e)
                if i >= 9:
                    print("requests failed and return.")
                    return
                else:
                    time.sleep(1)
            else:
                break

        picCnt = 0
        for i in img_src:
            picCnt = picCnt + 1
            try:
                #print(picCnt, " : ", str(i))
                imgUrl = re.findall(r'src=\"(.*?)\"', str(i))[0]
                print(picCnt, " : ", imgUrl)
            except Exception as e:
                print("imgUrl is invalible." + str(i))
                print(e)
                continue
            
            picPath = '{}/{}.png'.format(realSaveDir, str(picCnt))
            if(self.saveUrlPic(imgUrl, picPath)): # 返回长度大于0才往下执行
                picNameOnly = picPath.replace(realSaveDir+'/', '') # 转换为相对路径
                htmlCont = htmlCont.replace(imgUrl, picNameOnly)
                imgData_flg = ['data-src', 'data-original-src','quotes: none;', 'data-actualsrc']
                for flg in imgData_flg:
                    htmlCont = htmlCont.replace(flg, 'src')

        htmlCont = htmlCont + '<p>声明：<br>原文地址：<a href=\"{}\">{}</a>。<br> 文档仅供学习使用，一切版权归原创所有，学习愉快！</p>'.format(url, url)
        fd = open(htmlPath, 'w', encoding="utf-8")
        fd.write(htmlCont)
        fd.close()
        return htmlPath

    def open_url(self, url_str):
        http_ip = [
            '119.101.117.134:9999',
            '125.40.238.181:56738',
            '139.198.191.107:1080',
            '106.15.42.179:33543',
            '183.185.78.49:80'
        ]

        proxy_ip = {
        'http' : random.choice(http_ip),
        }
        html = ""
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate",
            "Connection":"keep-alive"
        }
        #返回网页内容,动态加载的需要另行处理
        if bool(proxy_ip):
            html = requests.get(url=url_str.replace('http:', 'https:'), timeout=20, headers = headers, proxies=proxy_ip).content
        else:
            html = requests.get(url=url_str, timeout=20, headers = headers).content
        
        print('使用代理的IP:{}，返回网页长度:{}'.format(proxy_ip, len(html)))
        return html

    def saveUrlPic(self, url, picName):
        '''
        保存url为图片的内容
        :param url : 要保存的url
        :param picName : 保存文件路径
        :return : 获取到的url内容长度
        '''
        # url有效性检查
        if(url.find("http") == -1 and url[:2] != "//"):
            print("url is not legal:" + url)
            return 0
        elif(url[:2] == "//"):
            url = "http:" + url

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
                imgOpt.imgConvert(picName, picName)
            else:
                print("get url failed.")
        except Exception as e:
            print("get url Exception：" + url)
            print(e)
        return contLen
