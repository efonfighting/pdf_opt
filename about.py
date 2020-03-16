import os, base64
from tkinter import *    #注意模块导入方式，否则代码会有差别
from asset.efon import Efon
from PIL import Image, ImageTk

class About(object):
    def __init__(self, tkFrame):
        vbar=Scrollbar(tkFrame) #竖直滚动条
        canvas=Canvas(tkFrame, bg='#FFFFFF', yscrollcommand=vbar.set) #创建canvas

        vbar.configure(command=canvas.yview)
        vbar.pack(side=RIGHT,fill=Y)
        
        frame=Frame(canvas) #把frame放在canvas里
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window(0,0,window=frame, anchor='nw')

        # ---------第 1 栏---------
        subFram1 = Frame(frame)
        Label(subFram1, text="联系作者：", font=("楷书", 13)).pack(side=TOP)
        with open('tmp.jpg','wb') as tmp:
            tmp.write(base64.b64decode(Efon().img))
        im = Image.open('tmp.jpg')
        # you need to keep a reference to the photo object, otherwise, it will be out of the scope and be garbage collected.
        tkFrame.tk_im = ImageTk.PhotoImage(im)
        Label(subFram1, image=tkFrame.tk_im).pack()
        subFram1.pack(side=TOP, fill=BOTH, expand=YES)
        os.remove('tmp.jpg')

        # ---------第 2 栏---------
        subFram2 = Frame(frame)
        verDes =   '版本说明：\n'\
                    '========================\n'\
                    '* 2020-02-23 V_1.1.1\n'\
                    '  1.url转PDF保存到本地。\n'\
                    '  2.下载进度展示栏。\n'\
                    '  3.保存目录的选择、展示、打开。\n'\
                    '  4.获取最新版本链接。\n'\
                    '  4.wkhtml和保存路径可保存。\n'\
                    '========================\n'
        Label(subFram2, text=verDes, font=("楷书", 13), justify = 'left').pack(side=LEFT)
        subFram2.pack(side=TOP, fill=BOTH, expand=YES, pady=20)

        tkFrame.update()
        canvas.config(scrollregion=canvas.bbox("all"))