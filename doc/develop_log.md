
# 开发记录

## 2020-03-17

* 桌面搜索工具
```
http://guihaidata.com/
功能点在于搜索个人电脑里的数据，可以搜索文件内容里的数据。
目测用的是electron开发的，界面其实比较简陋，但运营配套该有的都有，公司化的运营。
主要开发点在于本地数据库的建立、索引。难点在于将数据库、搜索引擎的环境集成到开发包中并实现一键部署。现在比较流行的搜索引擎有elastic search。
```

* 导出微博记录
```
https://www.yaozeyuan.online/stablog/
https://github.com/YaoZeyuan/stablog
开源项目，提供直接使用的可执行包。
目测也是用electron开发的，功能点主要是导出、备份微博内容，只支持拥有账号密码的个人账号导出。
备份导出的个数有html和pdf两种格式。目测是不带数据库的，大规模、持续备份能力可能稍差。
```

* 打包问题
```
Pyinstaller No module named pkg_resources.py2_warn

参考：https://blog.csdn.net/a362682954/article/details/104511277/

降低setuptools版本到 44.0.0 后成功解决问题。
pip install  setuptools==44.0.0
```

* tkinter：https://www.cnblogs.com/shwee/p/9427975.html
* tkinter 消息框：https://www.cnblogs.com/buchizaodian/p/7076964.html
* tkinter内置浏览器：https://github.com/EugeneJie/CandyPlayer