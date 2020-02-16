import tkinter as tk
from tkinter import ttk
 
window = tk.Tk()
# 设置窗口大小
winWidth = 800
winHeight = 500
# 获取屏幕分辨率
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
 
x = int((screenWidth - winWidth) / 2)
y = int((screenHeight - winHeight) / 2)
 
# 设置主窗口标题
window.title("TreeView参数说明")
# 设置窗口初始位置在屏幕居中
window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
# 设置窗口图标
window.iconbitmap(".\\assert\\efon.ico")
# 设置窗口宽高固定
window.resizable(0, 0)
 
# 定义列的名称
tab = ttk.Notebook(window)
frame1 = tk.Frame(tab, bg = "red")
tab1 = tab.add(frame1, text = "1")
 
frame2 = tk.Frame(tab, bg = "yellow")
tab2 = tab.add(frame2, text = "2")
 
frame3 = tk.Frame(tab, bg = "blue")
tab3 = tab.add(frame3, text = "3")
 
tab.pack(expand = True, fill = tk.BOTH)
 
# 设置选中tab2
tab.select(frame2)
 
window.mainloop()