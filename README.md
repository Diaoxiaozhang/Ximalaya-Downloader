<h1 align="center">喜马拉雅下载工具</h1>
<h4 align="center">Ximalaya-Downloader</h4>

<div align="center">

[![stars](https://img.shields.io/github/stars/Diaoxiaozhang/Ximalaya-Downloader.svg?style=flat&color=green)](https://github.com/Diaoxiaozhang/Ximalaya-Downloader/stargazers)
[![fork](https://img.shields.io/github/forks/Diaoxiaozhang/Ximalaya-Downloader.svg?style=flat&color=critical)](https://github.com/Diaoxiaozhang/Ximalaya-Downloader/forks)
[![release](https://img.shields.io/github/release/Diaoxiaozhang/Ximalaya-Downloader.svg?style=flat&color=blue)](https://github.com/Diaoxiaozhang/Ximalaya-Downloader/releases)
[![downloads](https://img.shields.io/github/downloads/Diaoxiaozhang/Ximalaya-Downloader/total?color=orange)](https://github.com/Diaoxiaozhang/Ximalaya-Downloader/releases)

</div>

### 说明

由于喜马拉雅官方没有下载声音的功能，即使开了vip也只能下载加密后的文件，且市面上很少有好的解密软件，所以我打算开发一款一键下载喜马拉雅专辑的软件。本软件计划使用纯Python语言开发，目前仍在编写中。由于本人的编程水平并不是十分理想，故如果大家在测试过程中发现bug，请一定在github中提交issue，也欢迎各位大佬提交pr。讨论区(Discussions)现已开启，大家关于本项目的一些问题、建议也可以发在这里。

PS：如果觉得这个项目不错，请一定为我点亮star，这对我很重要！另外，如果您愿意的话，也可以给我一点小小的赞助。

### 已实现功能

- [x] 单个声音下载
- [x] 专辑声音下载
- [x] 登录喜马拉雅账号并保存登录信息
- [x] 已购声音或vip免费声音下载
- [x] 自定义下载路径
- [x] 选择下载音频的音质
- [x] 自动重新下载下载失败的音频

### 计划实现功能

- [ ] GUI界面

### 存在的问题

- 由于喜马拉雅官方的限制，每日使用网页端接口下载音频的数量有所限制。请尽量避免短时间下载大量音频，如果达到当日限制，请改日再试，也可以使用喜马拉雅客户端下载加密的xm文件并使用[Ximalaya-XM-Decrypt](https://github.com/Diaoxiaozhang/Ximalaya-XM-Decrypt)解密。

### 手动获取cookie的方法

1. 在浏览器中打开喜马拉雅官网，并确保已登录账号。
2. 按F12打开开发者工具，选择Network（网络）选项卡。
3. 在页面中列出的一串请求列表中任意选择一个。
4. 在右侧的Headers（标头）选项卡中找到Cookie一项，复制其值。
5. 请确保复制的值中包含'1&_token'。
![操作示例](https://s2.loli.net/2023/04/20/rayiYUNEn2u7Q4D.png "操作示例")
操作示例中使用的是最新版edge浏览器，如果使用的是其他浏览器，可以查找相对应浏览器的开发者工具使用教程。

### 手动设置下载路径的方法

1. 先启动一次本软件，自动生成config.json。
2. 打开config.json，找到"path": ""，将右边的引号内改为你想要的下载路径
3. 请使用/或\\\\而不是\\作为路径分隔符，例如"path": "D:/Downloads"
4. 如果不设置下载路径，将默认下载到与软件同目录下的download文件夹

### 请作者喝一杯可乐

<p float="left">
  <img src="https://s2.loli.net/2023/03/03/Grg85kWcdDzMLBH.jpg" width="35%" />
  <img src="https://s2.loli.net/2023/03/03/E3zoxFskr8M7DKS.jpg" width="35%" />
</p>

