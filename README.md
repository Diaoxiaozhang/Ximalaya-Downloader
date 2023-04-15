<h1 align="center">喜马拉雅下载工具</h1>
<h4 align="center">Ximalaya-Downloader</h4>

<div align="center">

[![stars](https://img.shields.io/github/stars/Diaoxiaozhang/Ximalaya-Downloader.svg?style=flat&color=green)](https://github.com/Diaoxiaozhang/Ximalaya-Downloader/stargazers)
[![fork](https://img.shields.io/github/forks/Diaoxiaozhang/Ximalaya-Downloader.svg?style=flat&color=critical)](https://github.com/Diaoxiaozhang/Ximalaya-Downloader/forks)
[![release](https://img.shields.io/github/release/Diaoxiaozhang/Ximalaya-Downloader.svg?style=flat&color=blue)](https://github.com/Diaoxiaozhang/Ximalaya-Downloader/releases)
[![downloads](https://img.shields.io/github/downloads/Diaoxiaozhang/Ximalaya-Downloader/total?color=orange)](https://github.com/Diaoxiaozhang/Ximalaya-Downloader/releases)

</div>

### 说明

由于喜马拉雅官方没有下载声音的功能，即使开了vip也只能下载加密后的文件，且市面上很少有好的解密软件，所以我打算开发一款一键下载喜马拉雅专辑的软件。本软件计划使用纯Python语言开发，目前仍在编写中。由于本人的编程水平并不是十分理想，故如果大家在测试过程中发现bug，请一定在github中提交issue，也欢迎各位大佬提交pr。由于个人原因，可能无法及时回复或者解决问题，请大家见谅。

### 已实现功能

- [x] 单个声音下载
- [x] 专辑声音下载
- [x] 登录喜马拉雅账号并保存登录信息
- [x] 已购声音或vip免费声音下载

### 计划实现功能

- [ ] GUI界面
- [ ] 自定义下载路径
- [ ] 选择下载音频的音质
- [ ] 自动重新下载下载失败的音频

### 存在的问题

- 由于喜马拉雅官方的限制，付费音频的下载接口每日只能调用不到1000次，所以如果提示今日下载次数已达上限，请明天再试。这个问题我暂时还没有找到解决方法，如果有大佬知道的话，欢迎提交pr或issue。
