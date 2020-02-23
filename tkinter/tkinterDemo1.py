import tkinter.filedialog
import tkinter.messagebox
from tkinter import *    #注意模块导入方式，否则代码会有差别
from tkinter import ttk
import time

window = tkinter.Tk()
window.title('与python聊天中')
tab = ttk.Notebook(window)
frame1 = tkinter.Frame(tab)
tab1 = tab.add(frame1, text = "主页面")
tab.pack(expand = True, fill = tkinter.BOTH)
#创建frame容器
frmLT = tkinter.Frame(frame1, width=500, height=320, bg='white')
frmLC = tkinter.Frame(frame1, width=500, height=150, bg='red')
frmLB = tkinter.Frame(frame1, width=500, height=30)
frmRT = tkinter.Frame(frame1, width=200, height=500)

frmLT.grid(row=0, column=0,padx=1,pady=3)
frmLC.grid(row=1, column=0,padx=1,pady=3)
frmLB.grid(row=2, column=0)
frmRT.grid(row=0, column=1, rowspan=3,padx=2,pady=3)

'''#固定容器大小
frmLT.grid_propagate(0)
frmLC.grid_propagate(0)
frmLB.grid_propagate(0)
frmRT.grid_propagate(0)'''

#添加按钮
btnSend = tkinter.Button(frmLB, text='发 送', width = 8)#在frmLB容器中添加
btnSend.grid(row=2,column=0)
btnCancel = tkinter.Button(frmLB, text='取消', width = 8)
btnCancel.grid(row=2,column=1)

# #添加图片
# imgInfo = PhotoImage(file = "../asset/efon.jpg")
# lblImage = Label(frmRT, image = imgInfo)
# lblImage.image = imgInfo
# lblImage.grid()

#固定容器大小
frmLT.grid_propagate(0)
frmLC.grid_propagate(0)
frmLB.grid_propagate(0)
# frmRT.grid_propagate(0)
# 主窗口循环显示
window.mainloop()