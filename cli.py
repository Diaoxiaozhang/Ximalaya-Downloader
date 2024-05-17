import main
import asyncio
import re
import requests
import os
import time
import argparse
from fake_useragent import UserAgent

ximalaya = main.Ximalaya()
loop = asyncio.get_event_loop()

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sound', type=int, help='')
ua = UserAgent()

if __name__ == "__main__":
    print("欢迎使用喜马拉雅下载器")
    cookie, path = ximalaya.analyze_config()
    if not cookie:
        username = False
    else:
        username = ximalaya.judge_cookie(cookie)
    if os.path.isdir(path):
        print(f"检测到已设置下载路径为{path}，如果想要修改下载路径，请修改config.json文件中的path字段，将path字段删除或者将值设置为空字符串可恢复默认下载路径")
    else:
        print('在config文件中未检测到有效的下载路径，将使用默认下载路径，如果想要修改下载路径，请修改config.json文件中的path字段为你想要的下载路径')
        path = './download'
    response = requests.get(f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}?device=web&trackId=188017958&trackQualityLevel=1",headers=ximalaya.default_headers)
    if response.json()["ret"] == 927 and not username:
        print("检测到当前ip不在中国大陆，由于喜马拉雅官方限制，必须登录才能继续使用，将自动跳转到登录流程")
        ximalaya.login()
        headers = {
            "user-agent": ua.random,
            "cookie": ximalaya.analyze_config()[0]
        }
        logined = True
    elif not username:
        while True:
            print("未检测到有效喜马拉雅登录信息，请选择是否要登录：")
            print("1. 登录")
            print("2. 不登录")
            choice = input()
            if choice == "1":
                ximalaya.login()
                headers = {
                    "user-agent": ua.random,
                    "cookie": ximalaya.analyze_config()[0]
                }
                logined = True
                break
            elif choice == "2":
                headers = ximalaya.default_headers
                logined = False
                break
            else:
                print("输入有误，请重新输入！")
    else:
        print(f"已检测到有效登录信息，当前登录用户为{username}，如需切换账号请删除config.json文件然后重新启动本程序！")
        headers = {
            "user-agent": ua.random,
            "cookie": ximalaya.analyze_config()[0]
        }
        logined = True
    while True:
        print("请选择要使用的功能：")
        print("1. 下载单个声音")
        print("2. 下载专辑声音")
        print("3. 退出程序")
        choice = input()
        if choice == "1":
            print("请输入声音ID或链接：")
            _ = input()
            try:
                sound_id = int(_)
            except ValueError:
                try:
                    sound_id = re.search(r"sound/(?P<sound_id>\d+)", _).group('sound_id')
                except Exception:
                    print("输入有误，请重新输入！")
                    continue
            sound_info = ximalaya.analyze_sound(sound_id, headers)
            if sound_info is False:
                continue
            if sound_info == 0 and logined:
                print(f"ID为{sound_id}的声音解析为vip声音或付费声音，但当前登录账号未购买！")
                continue
            elif sound_info == 0 and not logined:
                print(f"ID为{sound_id}的声音解析为vip声音或付费声音，请登录后再试！")
                continue
            print(f"成功解析声音{sound_info['name']}，请选择您要下载的音质：（直接回车默认为普通音质）")
            print("0. 低音质")
            print("1. 普通音质")
            if sound_info[2] != "":
                print("2. 高音质")
            while True:
                choice = input()
                if choice == "":
                    choice = "1"
                if choice == "0" or choice == "1":
                    ximalaya.get_sound(sound_info["name"], sound_info[int(choice)], path)
                    break
                elif choice == "2" and sound_info[2] != "":
                    ximalaya.get_sound(sound_info["name"], sound_info[2], path)
                    break
                else:
                    print("输入有误，请重新输入！")
        elif choice == "2":
            print("请输入专辑ID或链接：")
            input_album = input()
            try:
                album_id = int(input_album)
            except ValueError:
                try:
                    album_id = re.search(r"album/(?P<album_id>\d+)", input_album).group('album_id')
                except Exception:
                    print("输入有误，请重新输入！")
                    continue
            album_name, sounds = ximalaya.analyze_album(album_id)
            if not sounds:
                continue
            album_type = ximalaya.judge_album(album_id, headers)
            if album_type == 0:
                print(f"成功解析免费专辑{album_id}，专辑名{album_name}，共{len(sounds)}个声音")
            elif album_type == 1:
                print(f"成功解析已购付费专辑{album_id}，专辑名{album_name}，共{len(sounds)}个声音")
            elif album_type == 2:
                if logined is True:
                    print(f"成功解析付费专辑{album_id}，专辑名{album_name}，但是当前登陆账号未购买此专辑或未开通vip")
                else:
                    print(f"成功解析付费专辑{album_id}，专辑名{album_name}，但是当前未登陆账号，请登录再尝试下载")
                continue
            else:
                continue
            while True:
                print("请选择要使用的功能：")
                print("1. 下载整个专辑")
                print("2. 下载专辑的部分声音")
                print("3. 显示专辑内声音列表")
                choice = input()
                if choice == "1" or choice == "2":
                    if choice == "1":
                        start = 1
                        end = len(sounds)
                    else:
                        while True:
                            print("请输入要下载的声音范围，中间用空格隔开，如输入“1 10”则表示下载第1到第10个声音：")
                            download_range = input()
                            try:
                                start, end = download_range.split(" ")
                                start = int(start)
                                end = int(end)
                            except Exception:
                                print("输入有误，请重新输入！")
                                continue
                            if start > end or start < 1 or end > len(sounds):
                                print("输入有误，请重新输入！")
                            else:
                                break
                    if album_type == 0 or album_type == 1:
                        while True:
                            print("请选择是否要在下载的音频文件名中加入序号：")
                            print("1. 加入序号")
                            print("2. 不加序号")
                            choice = input()
                            if choice == "1":
                                number = True
                                break
                            elif choice == "2":
                                number = False
                                break
                            else:
                                print("输入错误，请重新输入！")
                        print("请选择您想要下载的音质：（直接回车默认为普通音质）")
                        print("0. 低音质")
                        print("1. 普通音质")
                        print("2. 高音质（如果没有高音质则将下载普通音质）")
                        choice = input()
                        while True:
                            if choice == "":
                                choice = "1"
                            if choice == "0" or choice == "1" or choice == "2":
                                loop.run_until_complete(ximalaya.get_selected_sounds(sounds, album_name, start, end, headers, int(choice), number, path))
                                break
                            else:
                                print("输入有误，请重新输入！")
                    break
                elif choice == "3":
                    for sound in sounds:
                        print(f"{sound['index']}. {sound['title']}")
                else:
                    print("无效的选择，请重新输入。")
        elif choice == "3":
            break
        else:
            print("无效的选择，请重新输入。")
