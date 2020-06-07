
# 开发文档
## 功能开发
- [x] url转PDF保存到本地
- [x] 下载进度展示栏
- [x] 保存目录的选择、展示、打开
- [x] 获取最新版本链接
- [x] wkhtml和保存路径可保存
- [ ] 保存带图片的HTML到本地

## 框架设计
- [ ] 界面、功能代码分离解耦

## buglist
- [ ] 类似CSDN折叠的文章没有展开

# 说明文档
## 依赖文件编译
* 编译主程序之前，需要先执行convert_file2py.py，将依赖文件转换成py文件类。

## 打包exe
* `pyinstaller -F marktool.py -w -i asset/icon2.ico --version-file=asset/file_version_info.txt`
* info：C:/Users/xxx/AppData/Local/Programs/Python/Python37/Lib/site-packages/PyInstaller/utils/cliutils
