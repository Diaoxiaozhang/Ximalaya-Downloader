import asyncio
import base64
import binascii
import json
import math
import os
import re
import time

import aiofiles
import aiohttp
import requests
from Crypto.Cipher import AES
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions


class Ximalaya:
    def __init__(self):
        self.default_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14"
        }

    # 解析声音，如果成功返回声音名和声音链接，否则返回False
    def analyze_sound(self, sound_id):
        url = "https://www.ximalaya.com/revision/play/v1/audio"
        params = {
            "id": sound_id,
            "ptype": 1
        }
        try:
            response = requests.get(
                url, headers=self.default_headers, params=params, timeout=5)
        except:
            print(f'ID为{sound_id}的声音解析失败！')
            return False
        sound_url = response.json()["data"]["src"]
        url = "https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/1677297989848"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        try:
            response = requests.get(
                url, headers=self.default_headers, params=params, timeout=5)
        except:
            print(f'ID为{sound_id}的声音解析失败！')
            return False
        sound_name = response.json()["trackInfo"]["title"]
        return sound_name, sound_url

    # 解析专辑，如果成功返回专辑名和专辑声音列表，否则返回False
    def analyze_album(self, album_id):
        url = "https://www.ximalaya.com/revision/album/v1/getTracksList"
        params = {
            "albumId": album_id,
            "pageNum": 1,
            "pageSize": 100
        }
        try:
            response = requests.get(
                url, headers=self.default_headers, params=params, timeout=5)
        except:
            print(f'ID为{album_id}的专辑解析失败！')
            return False
        pages = math.ceil(response.json()["data"]["trackTotalCount"] / 100)
        sounds = []
        for page in range(1, pages + 1):
            params = {
                "albumId": album_id,
                "pageNum": page,
                "pageSize": 100
            }
            try:
                response = requests.get(
                    url, headers=self.default_headers, params=params)
            except:
                print(f'ID为{album_id}的专辑解析失败！')
                return False
            sounds += response.json()["data"]["tracks"]
        album_name = sounds[0]["albumTitle"]
        return album_name, sounds

    # 协程解析声音
    async def async_analyze_sound(self, sound_id, session):
        url = "https://www.ximalaya.com/revision/play/v1/audio"
        params = {
            "id": sound_id,
            "ptype": 1
        }
        async with session.get(url, headers=self.default_headers, params=params) as response:
            sound_url = json.loads(await response.text())["data"]["src"]
        url = "https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/1677297989848"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        async with session.get(url, headers=self.default_headers, params=params) as response:
            sound_name = json.loads(await response.text())["trackInfo"]["title"]
        return sound_name, sound_url

    # 将文件名中不能包含的字符替换为空格
    def replace_invalid_chars(self, name):
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in name:
                name = name.replace(char, " ")
        return name

    # 下载单个声音
    def get_sound(self, sound_name, sound_url):
        sound_name = self.replace_invalid_chars(sound_name)
        if os.path.exists(f"./download/{sound_name}.m4a"):
            print(f'{sound_name}已存在！')
        try:
            response = requests.get(
                sound_url, headers=self.default_headers, timeout=10)
        except:
            print(f'{sound_name}下载失败！')
        sound_file = response.content
        if not os.path.exists(f"./download"):
            os.makedirs(f"./download")
        else:
            with open(f"./download/{sound_name}.m4a", mode="wb") as f:
                f.write(sound_file)
            print(f'{sound_name}下载完成！')

    # 协程下载声音
    async def async_get_sound(self, sound_name, sound_url, album_name, session):
        sound_name = self.replace_invalid_chars(sound_name)
        album_name = self.replace_invalid_chars(album_name)
        if not os.path.exists(f"./download/{album_name}"):
            os.makedirs(f"./download/{album_name}")
        async with session.get(sound_url, headers=self.default_headers) as response:
            async with aiofiles.open(f"./download/{album_name}/{sound_name}.m4a", mode="wb") as f:
                await f.write(await response.content.read())

    # 下载专辑中的选定声音
    async def get_selected_sounds(self, sounds, album_name, start, end):
        tasks = []
        session = aiohttp.ClientSession()
        for i in range(start, end + 1):
            sound_id = sounds[i - 1]["trackId"]
            tasks.append(asyncio.create_task(
                self.async_analyze_sound(sound_id, session)))
        sounds = await asyncio.gather(*tasks)
        for sound in sounds:
            tasks.append(asyncio.create_task(self.async_get_sound(
                sound[0], sound[1], album_name, session)))
        await asyncio.wait(tasks)
        await session.close()

    # 解密vip声音url
    def decrypt_url(self, ciphertext):
        key = binascii.unhexlify("aaad3e4fd540b0f79dca95606e72bf93")
        ciphertext = base64.urlsafe_b64decode(
            ciphertext + '=' * (4 - len(ciphertext) % 4))
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        plaintext = re.sub(r"[^\x20-\x7E]", "", plaintext.decode("utf-8"))
        return plaintext

    # 获取vip声音的加密url，如果成功返回加密url，否则返回False
    def get_encrypted_url(self, sound_id):
        url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        try:
            response = requests.get(
                url, headers=self.default_headers, params=params, timeout=5)
        except:
            print(f'ID为{sound_id}的VIP声音解析失败！')
            return False
        encrypted_url = response.json()["trackInfo"]["playUrlList"][0]["url"]
        return encrypted_url

    # 协程获取vip声音的加密url
    async def async_get_encrypted_url(self, sound_id, session):
        url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        async with session.get(url, headers=self.default_headers, params=params) as response:
            encrypted_url = json.loads(await response.text())["trackInfo"]["playUrlList"][0]["url"]
        return encrypted_url

    # 判断声音是否为付费声音，如果是免费声音返回0，如果是已购买的付费声音返回1，如果是未购买的付费声音返回2，如果解析失败返回False
    def judge_sound(self, sound_id):
        url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        try:
            response = requests.get(
                url, headers=self.default_headers, params=params, timeout=5)
        except:
            print(f'ID为{sound_id}的声音解析失败！')
            return False
        if not response.json()["trackInfo"]["isPaid"]:
            return 0  # 免费
        elif response.json()["trackInfo"]["isAuthorized"]:
            return 1  # 已购
        else:
            return 2  # 未购

    # 判断专辑是否为付费专辑，如果是免费专辑返回0，如果是已购买的付费专辑返回1，如果是未购买的付费专辑返回2，如果解析失败返回False
    def judge_album(self, album_id):
        url = "https://www.ximalaya.com/revision/album/v1/simple"
        params = {
            "albumId": album_id
        }
        try:
            response = requests.get(
                url, headers=self.default_headers, params=params, timeout=5)
        except:
            print(f'ID为{album_id}的专辑解析失败！')
            return False
        if not response.json()["data"]["albumPageMainInfo"]["isPaid"]:
            return 0
        elif response.json()["data"]["albumPageMainInfo"]:  # TODO
            pass

    # 下载vip专辑中的选定声音
    async def get_selected_vip_sounds(self, sounds, album_name, start, end):
        tasks = []
        session = aiohttp.ClientSession()
        for i in range(start, end + 1):
            sound_id = sounds[i - 1]["trackId"]
            tasks.append(asyncio.create_task(
                self.async_get_encrypted_url(sound_id, session)))
        encrypted_urls = await asyncio.gather(*tasks)
        await asyncio.wait(tasks)
        tasks = []
        urls = []
        for encrypted_url in encrypted_urls:
            urls.append(self.decrypt_url(encrypted_url))
        num = 0
        for url in urls:
            tasks.append(asyncio.create_task(self.async_get_sound(
                sounds[num]["title"], url, album_name, session)))
            num += 1
        await asyncio.wait(tasks)
        await session.close()

    def get_cookie(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except:
            self.initialize_config()
        try:
            cookie = config["cookie"]
        except KeyError:
            return False
        return cookie

    # 判断cookie是否有效
    def judge_cookie(self, cookie):
        url = "https://www.ximalaya.com/revision/my/getCurrentUserInfo"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14",
            "cookie": cookie
        }
        response = requests.get(url, headers=headers)
        if response.json()["ret"] == 200:
            return True
        else:
            return False

    # 初始化配置文件
    def initialize_config(self):
        with open("config.json", "w") as f:
            config = {
                "cookie": ""
            }
            json.dump(config, f)

    def login(self):
        print("请输入登录方式：")
        print("1. 在浏览器中登录并自动提取cookie")
        print("2. 手动输入cookie")
        choice = input()
        if choice == "1":
            print("请在弹出的浏览器中登录喜马拉雅账号，登陆成功后请关闭浏览器")
            option = webdriver.ChromeOptions()
            option.add_experimental_option("detach", True)
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
            driver.get("https://passport.ximalaya.com/page/web/login")
            try:
                WebDriverWait(driver, 300).until(EC.url_to_be("https://www.ximalaya.com/"))
                cookie = driver.get_cookies()
                driver.quit()
            except selenium.common.exceptions.TimeoutException:
                print("登录超时，自动返回主菜单！")
                driver.quit()
                return
            token = [d['value'] for d in cookie if d['name'] == '1&_token'][0]
            with open("config.json", "r") as f:
                config = json.load(f)
            config["cookie"] = f"1&_token={token}"
            with open("config.json", "w") as f:
                json.dump(config, f)
        if choice == "2":
            print("请输入cookie：（获取方法详见README）")
            cookie = input()
            with open("config.json", "r") as f:
                config = json.load(f)
            config["cookie"] = cookie
            isCookieAvailable = self.judge_cookie(cookie)
            if isCookieAvailable:
                with open("config.json", "w") as f:
                    json.dump(config, f)
                print("cookie设置成功！")
            else:
                print("cookie无效，将返回主菜单，建议使用方法1自动获取cookie！")
                return


class ConsoleVersion:
    def __init__(self):
        self.ximalaya = Ximalaya()
        self.loop = asyncio.get_event_loop()

    def run(self):
        print("欢迎使用喜马拉雅下载器")
        isLogined = self.ximalaya.judge_cookie(self.ximalaya.get_cookie())
        if not isLogined:
            print("未检测到有效喜马拉雅登录信息，请选择是否要登录：")
            print("1. 登录")
            print("2. 不登录")
            choice = input()
            if choice == "1":
                self.ximalaya.login()
            elif choice == "2":
                pass
            else:
                print("输入有误，将返回主菜单！")
                return
        while True:
            print("请选择要使用的功能：")
            print("1. 单个声音")
            print("2. 专辑声音")
            print("3. 退出程序")
            choice = input()
            if choice == "1":
                print("请输入声音ID或链接：")
                _ = input()
                try:
                    sound_id = int(_)
                except ValueError:
                    try:
                        sound_id = re.search(r"ximalaya.com/sound/(?P<sound_id>\d+)", _).group('sound_id')
                    except:
                        print("输入有误，请重新输入！")
                        continue
                sound_type = self.ximalaya.judge_sound(sound_id)
                if sound_type == 0:
                    sound_name, sound_url = self.ximalaya.analyze_sound(
                        sound_id)
                    print(f"声音名{sound_name}，判断为免费声音，正在开始下载……")
                    self.ximalaya.get_sound(sound_name, sound_url)

            elif choice == "2":
                print("请输入专辑ID：")
                _ = input()
                try:
                    album_id = int(_)
                except ValueError:
                    try:
                        album_id = re.search(r"ximalaya.com/album/(?P<album_id>\d+)", _).group('album_id')
                    except:
                        print("输入有误，请重新输入！")
                        continue
                album_name, sounds = self.ximalaya.analyze_album(album_id)
                album_type = self.ximalaya.judge_album(album_id)
                if album_type == 0:
                    print(
                        f"成功解析免费专辑{album_id}，专辑名{album_name}，共{len(sounds)}个声音")
                    print("请选择要使用的功能：")
                    print("1. 下载整个专辑")
                    print("2. 下载专辑的部分声音")
                    print("3. 显示专辑内声音列表")
                    choice = input()
                    if choice == "1":
                        self.loop.run_until_complete(self.ximalaya.get_selected_sounds(
                            sounds, album_name, 1, len(sounds)))
                        print("专辑全部声音下载完成！")

            elif choice == "3":
                break

            else:
                print("无效的选择，请重新输入。")
