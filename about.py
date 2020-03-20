import os, base64
from tkinter import *    #注意模块导入方式，否则代码会有差别
from asset import asset
from PIL import Image, ImageTk

class About(object):
    def __init__(self, tkFrame):
        vbar=Scrollbar(tkFrame) #竖直滚动条
        self.canvas=Canvas(tkFrame, yscrollcommand=vbar.set) #创建canvas

        vbar.configure(command=self.canvas.yview)
        vbar.pack(side=RIGHT,fill=Y)
        
        frame=Frame(self.canvas) #把frame放在canvas里
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(0,0,window=frame, anchor='nw')

        # ---------第 1 栏---------
        subFram1 = Frame(frame)

        title1 = "联系我们："
        Label(subFram1, text=title1, font=("楷书", 15, "bold"), justify = 'left').grid(sticky=W)
        with open('tmp.jpg','wb') as tmp:
            tmp.write(base64.b64decode(asset.Lianxi().img))
        im = Image.open('tmp.jpg')
        # you need to keep a reference to the photo object, otherwise, it will be out of the scope and be garbage collected.
        subFram1.tk_im = ImageTk.PhotoImage(im)
        Label(subFram1, image=subFram1.tk_im).grid(pady=10)
        subFram1.grid(pady=10)
        os.remove('tmp.jpg')

        # ---------第 2 栏---------
        subFram1 = Frame(frame)

        title1 = "交流社区："
        Label(subFram1, text=title1, font=("楷书", 15, "bold"), justify = 'left').grid(sticky=W)
        with open('tmp.jpg','wb') as tmp:
            tmp.write(base64.b64decode(asset.Shequ().img))
        im = Image.open('tmp.jpg')
        # you need to keep a reference to the photo object, otherwise, it will be out of the scope and be garbage collected.
        subFram1.tk_im = ImageTk.PhotoImage(im)
        Label(subFram1, image=subFram1.tk_im).grid(pady=10)
        subFram1.grid(sticky=W, pady=10)
        os.remove('tmp.jpg')

        # ---------第 3 栏---------
        subFram2 = Frame(frame)

        title2 = "版本说明："
        Label(subFram2, text=title2, font=("楷书", 15, "bold"), justify = 'left').grid(sticky=W,pady=10)

        verDes =   '================================================================================\n'\
                    '* 2020-02-23 V_1.1.1\n\n'\
                    '  1.url转PDF保存到本地。\n'\
                    '  2.下载进度展示栏。\n'\
                    '  3.保存目录的选择、展示、打开。\n'\
                    '  4.获取最新版本链接。\n'\
                    '  5.wkhtml和保存路径可保存。\n'\
                    '================================================================================\n'
        Label(subFram2, text=verDes, font=("楷书", 13), justify = 'left').grid(sticky=W,pady=10)

        subFram2.grid(sticky=W, pady=10)

        # ---------第 4 栏---------


        tkFrame.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*int(event.delta/120), "units")