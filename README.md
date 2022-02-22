# 通过输入bilibili网站的视频链接，下载相应弹幕xml文件
---
## 介绍
### 环境依赖：
* python>=3.6
* requests
### 使用说明：
在终端使用如下命令可以利用test文件夹中的测试样例批量下载弹幕
```python
   python main -i ./test/inputUrl.json
```
默认输出路径是./xms/下，如果想自定义输出路径可以输入如下命令
```python
   python main -i ./test/url.json -o xxx
```
目前支持读取两种文件批量下载，分别是json,txt,test文件夹下有样例，自行参照自定义自己的输入文件
### 目前支持的链接类型
输入链接包含多种情况：

    ep号：下载对应的番剧弹幕
    Bv_id:下载对应的视频弹幕
    ss_id:下载对应番剧全集的弹幕文件，并存储在单独文件夹中 
目前程序暂时不支持多线程下载，后期有时间会完善





