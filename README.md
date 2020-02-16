
## 依赖文件编译
* 编译主程序之前，需要先执行convert_file2py.py，将依赖文件转换成py文件类。

## 打包exe
* `pyinstaller -F pdfmerge.py -w -i asset/icon.ico --version-file=asset/file_version_info.txt`
* info：C:/Users/xxx/AppData/Local/Programs/Python/Python37/Lib/site-packages/PyInstaller/utils/cliutils



## 参考文献
* tkinter：https://www.cnblogs.com/shwee/p/9427975.html
* tkinter 消息框：https://www.cnblogs.com/buchizaodian/p/7076964.html
