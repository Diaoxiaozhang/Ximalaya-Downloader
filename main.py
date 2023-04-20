import asyncio
import base64
import binascii
import json
import math
import os
import re
import time
import logging
import traceback

import aiofiles
import aiohttp
import requests
from Crypto.Cipher import AES
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
import colorama

colorama.init(autoreset=True)
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('app.log', mode='w')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class Ximalaya:
    def __init__(self):
        self.default_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14"
        }

    # 解析声音，如果成功返回声音名和声音链接，否则返回False
    def analyze_sound(self, sound_id):
        logger.debug(f'开始解析ID为{sound_id}的声音')
        url = "https://www.ximalaya.com/revision/play/v1/audio"
        params = {
            "id": sound_id,
            "ptype": 1
        }
        try:
            response = requests.get(url, headers=self.default_headers, params=params, timeout=5)
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        try:
            sound_url = response.json()["data"]["src"]
        except:
            sound_url = None
        url = "https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/1677297989848"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        try:
            response = requests.get(url, headers=self.default_headers, params=params, timeout=5)
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        try:
            sound_name = response.json()["trackInfo"]["title"]
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        logger.debug(f'ID为{sound_id}的声音解析成功！')
        return sound_name, sound_url

    # 解析专辑，如果成功返回专辑名和专辑声音列表，否则返回False
    def analyze_album(self, album_id):
        logger.debug(f'开始解析ID为{album_id}的专辑')
        url = "https://www.ximalaya.com/revision/album/v1/getTracksList"
        params = {
            "albumId": album_id,
            "pageNum": 1,
            "pageSize": 100
        }
        try:
            response = requests.get(url, headers=self.default_headers, params=params, timeout=15)
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{album_id}的专辑解析失败！')
            logger.debug(f'ID为{album_id}的专辑解析失败！')
            logger.debug(traceback.format_exc())
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
                response = requests.get(url, headers=self.default_headers, params=params, timeout=15)
            except Exception as e:
                print(colorama.Fore.RED + f'ID为{album_id}的专辑解析失败！')
                logger.debug(f'ID为{album_id}的专辑解析失败！')
                logger.debug(traceback.format_exc())
                return False
            sounds += response.json()["data"]["tracks"]
        album_name = sounds[0]["albumTitle"]
        logger.debug(f'ID为{album_id}的专辑解析成功')
        return album_name, sounds

    # 协程解析声音
    async def async_analyze_sound(self, sound_id, session):
        logger.debug(f'开始解析ID为{sound_id}的声音')
        url = "https://www.ximalaya.com/revision/play/v1/audio"
        params = {
            "id": sound_id,
            "ptype": 1
        }
        try:
            async with session.get(url, headers=self.default_headers, params=params, timeout=30) as response:
                sound_url = json.loads(await response.text())["data"]["src"]
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        try:
            async with session.get(url, headers=self.default_headers, params=params, timeout=30) as response:
                sound_name = json.loads(await response.text())["trackInfo"]["title"]
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        logger.debug(f'ID为{sound_id}的声音解析成功')
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
        retries = 3
        sound_name = self.replace_invalid_chars(sound_name)
        if os.path.exists(f"./download/{sound_name}.m4a"):
            print(f'{sound_name}已存在！')
            return
        while retries > 0:
            try:
                logger.debug(f'开始下载声音{sound_name}')
                response = requests.get(sound_url, headers=self.default_headers, timeout=30)
                break
            except Exception as e:
                print(colorama.Fore.RED + f'{sound_name}下载失败！')
                logger.debug(f'{sound_name}下载失败！')
                logger.debug(traceback.format_exc())
                retries -= 1
            print(f'{sound_name}经过三次重试后下载失败！')
            logger.debug(f'{sound_name}经过三次重试后下载失败！')
            logger.debug(traceback.format_exc())
            return False
        sound_file = response.content
        if not os.path.exists(f"./download"):
            os.makedirs(f"./download")
        with open(f"./download/{sound_name}.m4a", mode="wb") as f:
            f.write(sound_file)
        print(f'{sound_name}下载完成！')
        logger.debug(f'{sound_name}下载完成！')

    # 协程下载声音
    async def async_get_sound(self, sound_name, sound_url, album_name, session, num=None):
        logger.debug(f'开始下载声音{sound_name}')
        if num is None:
            sound_name = self.replace_invalid_chars(sound_name)
        else:
            sound_name = f"{num}-{sound_name}"
            sound_name = self.replace_invalid_chars(sound_name)
        album_name = self.replace_invalid_chars(album_name)
        if not os.path.exists(f"./download/{album_name}"):
            os.makedirs(f"./download/{album_name}")
        if os.path.exists(f"./download/{sound_name}.m4a"):
            print(f'{sound_name}已存在！')
        try:
            async with session.get(sound_url, headers=self.default_headers, timeout=300) as response:
                async with aiofiles.open(f"./download/{album_name}/{sound_name}.m4a", mode="wb") as f:
                    await f.write(await response.content.read())
            print(f'{sound_name}下载完成！')
            logger.debug(f'{sound_name}下载完成！')
        except Exception as e:
            print(colorama.Fore.RED + f'{sound_name}下载失败！')
            logger.debug(f'{sound_name}下载失败！')
            logger.debug(traceback.format_exc())

    # 下载专辑中的选定声音
    async def get_selected_sounds(self, sounds, album_name, start, end, number=True):
        tasks = []
        session = aiohttp.ClientSession()
        digits = len(str(len(sounds)))
        for i in range(start - 1, end):
            sound_id = sounds[i]["trackId"]
            tasks.append(asyncio.create_task(self.async_analyze_sound(sound_id, session)))
        sounds = await asyncio.gather(*tasks)
        if number:
            num = start
            for sound in sounds:
                num_ = str(num).zfill(digits)
                tasks.append(asyncio.create_task(self.async_get_sound(sound[0], sound[1], album_name, session, num_)))
                num += 1
        else:
            for sound in sounds:
                tasks.append(asyncio.create_task(self.async_get_sound(sound[0], sound[1], album_name, session)))
        await asyncio.wait(tasks)
        await session.close()

    # 解密vip声音url
    def decrypt_url(self, ciphertext):
        key = binascii.unhexlify("aaad3e4fd540b0f79dca95606e72bf93")
        ciphertext = base64.urlsafe_b64decode(ciphertext + '=' * (4 - len(ciphertext) % 4))
        cipher = AES.new(key, AES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        plaintext = re.sub(r"[^\x20-\x7E]", "", plaintext.decode("utf-8"))
        return plaintext

    # 获取vip声音的加密url，如果成功返回加密url，否则返回False
    def get_encrypted_url(self, sound_id, headers):
        logger.debug(f'开始获取ID为{sound_id}的vip声音的加密url')
        url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的vip声音解析失败！')
            logger.debug(f'ID为{sound_id}的vip声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        try:
            encrypted_url = response.json()["trackInfo"]["playUrlList"][0]["url"]
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的vip声音解析失败！')
            logger.debug(f'ID为{sound_id}的vip声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        logger.debug(f'ID为{sound_id}的vip声音获取加密url成功！')
        return encrypted_url

    # 协程获取vip声音的加密url
    async def async_get_encrypted_url(self, sound_id, session, headers):
        logger.debug(f'开始获取ID为{sound_id}的vip声音的加密url')
        url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        async with session.get(url, headers=headers, params=params, timeout=30) as response:
            try:
                encrypted_url = json.loads(await response.text())["trackInfo"]["playUrlList"][0]["url"]
            except Exception as e:
                print(colorama.Fore.RED + f'ID为{sound_id}的vip声音解析失败！')
                logger.debug(f'ID为{sound_id}的vip声音解析失败')
                logger.debug(traceback.format_exc())
                return False
        logger.debug(f'ID为{sound_id}的vip声音获取加密url成功！')
        return encrypted_url

    # 判断声音是否为付费声音，如果是免费声音返回0，如果是已购买的付费声音返回1，如果是未购买的付费声音返回2，如果解析失败返回False
    def judge_sound(self, sound_id, headers):
        logger.debug(f'开始判断ID为{sound_id}的声音的类型')
        url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
        params = {
            "device": "web",
            "trackId": sound_id,
            "trackQualityLevel": 1
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音判断类型失败！')
            logger.debug(traceback.format_exc())
            return False
        try:
            track_info = response.json()["trackInfo"]
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音判断类型失败！')
            logger.debug(traceback.format_exc())
            return False
        logger.debug(f'ID为{sound_id}的声音判断类型成功！')
        if not track_info["isPaid"]:
            return 0  # 免费
        elif track_info["isAuthorized"]:
            return 1  # 已购
        else:
            return 2  # 未购

    # 判断专辑是否为付费专辑，如果是免费专辑返回0，如果是已购买的付费专辑返回1，如果是未购买的付费专辑返回2，如果解析失败返回False
    def judge_album(self, album_id, headers):
        logger.debug(f'开始判断ID为{album_id}的专辑的类型')
        url = "https://www.ximalaya.com/revision/album/v1/simple"
        params = {
            "albumId": album_id
        }
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{album_id}的专辑解析失败！')
            logger.debug(f'ID为{album_id}的专辑判断类型失败！')
            logger.debug(traceback.format_exc())
            return False
        logger.debug(f'ID为{album_id}的专辑判断类型成功！')
        if not response.json()["data"]["albumPageMainInfo"]["isPaid"]:
            return 0  # 免费专辑
        elif response.json()["data"]["albumPageMainInfo"]["hasBuy"]:
            return 1  # 已购专辑
        else:
            return 2  # 未购专辑

    # 下载单个vip声音
    def get_vip_sound(self, sound_name, sound_id, headers):
        encrypted_url = self.get_encrypted_url(sound_id, headers)
        sound_url = self.decrypt_url(encrypted_url)
        self.get_sound(sound_name, sound_url)

    # 下载vip专辑中的选定声音
    async def get_selected_vip_sounds(self, sounds, album_name, start, end, headers, number=True):
        tasks = []
        session = aiohttp.ClientSession()
        for i in range(start, end + 1):
            sound_id = sounds[i - 1]["trackId"]
            tasks.append(asyncio.create_task(self.async_get_encrypted_url(sound_id, session, headers)))
        encrypted_urls = await asyncio.gather(*tasks)
        await asyncio.wait(tasks)
        tasks = []
        urls = []
        i = 0
        for encrypted_url in encrypted_urls:
            if not encrypted_url:
                print(colorama.Fore.RED + sounds[start + i - 1]["title"] + "下载失败！")
                logger.debug(sounds[start + i - 1]["title"] + "下载失败！")
            else:
                urls.append(self.decrypt_url(encrypted_url))
            i += 1
        if not urls:
            await session.close()
            return False
        if number:
            digits = len(str(len(sounds)))
            file_num = start
            num = 0
            for url in urls:
                file_num_ = str(file_num).zfill(digits)
                tasks.append(asyncio.create_task(self.async_get_sound(sounds[num]["title"], url, album_name, session, file_num_)))
                num += 1
                file_num += 1
        else:
            num = 0
            for url in urls:
                tasks.append(asyncio.create_task(self.async_get_sound(sounds[num]["title"], url, album_name, session)))
                num += 1
        await asyncio.wait(tasks)
        await session.close()

    # 获取配置文件中的cookie
    def get_cookie(self):
        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except:
            self.initialize_config()
        try:
            cookie = config["cookie"]
        except:
            return False
        return cookie

    # 判断cookie是否有效
    def judge_cookie(self, cookie):
        url = "https://www.ximalaya.com/revision/my/getCurrentUserInfo"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14",
            "cookie": cookie
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
        except Exception as e:
            print("无法获取喜马拉雅用户数据，请检查网络状况！")
            logger.debug("无法获取喜马拉雅用户数据！")
            logger.debug(traceback.format_exc())
        if response.json()["ret"] == 200:
            return response.json()["data"]["userName"]
        else:
            return False

    # 初始化配置文件
    def initialize_config(self):
        with open("config.json", "w") as f:
            config = {
                "cookie": ""
            }
            json.dump(config, f)

    # 登录喜马拉雅账号
    def login(self):
        print("请输入登录方式：")
        print("1. 在浏览器中登录并自动提取cookie")
        print("2. 手动输入cookie")
        choice = input()
        if choice == "1":
            print("请选择浏览器：")
            print("1. Google Chrome")
            print("2. Microsoft Edge")
            choice = input()
            if choice == "1":
                    option = webdriver.ChromeOptions()
                    option.add_experimental_option("detach", True)
                    option.add_experimental_option('excludeSwitches', ['enable-logging'])
                    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
            elif choice == "2":
                    option = webdriver.EdgeOptions()
                    option.add_experimental_option("detach", True)
                    option.add_experimental_option('excludeSwitches', ['enable-logging'])
                    driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=option)
            else:
                return
            print("请在弹出的浏览器中登录喜马拉雅账号，登陆成功浏览器会自动关闭")
            driver.get("https://passport.ximalaya.com/page/web/login")
            try:
                WebDriverWait(driver, 300).until(EC.url_to_be("https://www.ximalaya.com/"))
                cookies = driver.get_cookies()
                logger.debug('以下是使用浏览器登录喜马拉雅账号时的浏览器日志：')
                for entry in driver.get_log('browser'):
                    logger.debug(entry['message'])
                logger.debug('浏览器日志结束')
                driver.quit()
            except selenium.common.exceptions.TimeoutException:
                print("登录超时，自动返回主菜单！")
                logger.debug('以下是使用浏览器登录喜马拉雅账号时的浏览器日志：')
                for entry in driver.get_log('browser'):
                    logger.debug(entry['message'])
                logger.debug('浏览器日志结束')
                driver.quit()
                return
            cookie = ""
            for cookie_ in cookies:
                cookie += f"{cookie_['name']}={cookie_['value']}; "
            with open("config.json", "r") as f:
                config = json.load(f)
            config["cookie"] = cookie
            with open("config.json", "w") as f:
                json.dump(config, f)
        elif choice == "2":
            print("请输入cookie：（获取方法详见README）")
            cookie = input()
            with open("config.json", "r") as f:
                config = json.load(f)
            config["cookie"] = cookie
            is_cookie_available = self.judge_cookie(cookie)
            if is_cookie_available:
                with open("config.json", "w") as f:
                    json.dump(config, f)
                print("cookie设置成功！")
            else:
                print("cookie无效，将返回主菜单，建议使用方法1自动获取cookie！")
                return
        username = self.judge_cookie(cookie)
        print(f"成功登录账号{username}！")


class ConsoleVersion:
    def __init__(self):
        self.ximalaya = Ximalaya()
        self.loop = asyncio.get_event_loop()

    def run(self):
        print("欢迎使用喜马拉雅下载器")
        cookie = self.ximalaya.get_cookie()
        if not cookie:
            username = False
        else:
            username = self.ximalaya.judge_cookie(cookie)
        if not username:
            print("未检测到有效喜马拉雅登录信息，请选择是否要登录：")
            print("1. 登录")
            print("2. 不登录")
            choice = input()
            if choice == "1":
                self.ximalaya.login()
                headers = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14",
                    "cookie": self.ximalaya.get_cookie()
                }
                logined = True
            elif choice == "2":
                headers = self.ximalaya.default_headers
                logined = False
            else:
                print("输入有误，将返回主菜单！")
                return
        else:
            print(f"已检测到有效登录信息，当前登录用户为{username}，如需切换账号请删除config.json文件然后重新启动本程序！")
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14",
                "cookie": self.ximalaya.get_cookie()
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
                        sound_id = re.search(r"ximalaya.com/sound/(?P<sound_id>\d+)", _).group('sound_id')
                    except:
                        print("输入有误，请重新输入！")
                        continue
                sound_type = self.ximalaya.judge_sound(sound_id, headers)
                if sound_type is False:
                    continue
                if sound_type == 0:
                    sound_name, sound_url = self.ximalaya.analyze_sound(sound_id)
                    print(f"声音名{sound_name}，判断为免费声音，正在开始下载……")
                    self.ximalaya.get_sound(sound_name, sound_url)
                elif sound_type == 1:
                    sound_name, _ = self.ximalaya.analyze_sound(sound_id)
                    print(f"声音名{sound_name}，判断为已购付费声音或vip免费声音，正在开始下载……")
                    self.ximalaya.get_vip_sound(sound_name, sound_id, headers)
                else:
                    print(f"声音名{sound_name}，判断为付费声音，请登录已购买该声音的账号后再尝试下载！")
            elif choice == "2":
                print("请输入专辑ID或链接：")
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
                album_type = self.ximalaya.judge_album(album_id, headers)
                if album_type == 0:
                    print(f"成功解析免费专辑{album_id}，专辑名{album_name}，共{len(sounds)}个声音")
                elif album_type == 1:
                    print(f"成功解析已购付费专辑{album_id}，专辑名{album_name}，共{len(sounds)}个声音")
                elif album_type == 2:
                    if logined is True:
                        print(f"成功解析付费专辑{album_id}，专辑名{album_name}，但是当前登陆账号未购买此专辑或未开通vip，请登录可以下载此专辑的账号后再尝试下载")
                    else:
                        print(f"成功解析付费专辑{album_id}，专辑名{album_name}，但是当前未登陆账号，请登录可以下载此专辑的账号后再尝试下载")
                    continue
                else:
                    break
                while True:
                    print("请选择要使用的功能：")
                    print("1. 下载整个专辑")
                    print("2. 下载专辑的部分声音")
                    print("3. 显示专辑内声音列表")
                    choice = input()
                    if choice == "1":
                        if album_type == 0:
                            self.loop.run_until_complete(self.ximalaya.get_selected_sounds(sounds, album_name, 1, len(sounds)))
                            print("专辑全部声音下载完成！")
                            break
                        else:
                            self.loop.run_until_complete(self.ximalaya.get_selected_vip_sounds(sounds, album_name, 1, len(sounds), headers))
                            print("专辑全部声音下载完成！")
                            break
                    elif choice == "2":
                        print("请输入要下载的声音范围，中间用空格隔开，如输入“1 10”则表示下载第1到第10个声音：")
                        _ = input()
                        try:
                            start, end = _.split(" ")
                            try:
                                start = int(start)
                            except:
                                print("输入有误，请重新输入！")
                                continue
                            try:
                                end = int(end)
                            except:
                                print("输入有误，请重新输入！")
                                continue
                        except:
                            print("输入有误，请重新输入！")
                        if start > end:
                            print("输入有误，请重新输入！")
                            continue
                        if album_type == 0:
                            self.loop.run_until_complete(self.ximalaya.get_selected_sounds(sounds, album_name, start, end))
                            print("专辑选定声音下载完成！")
                            break
                        else:
                            self.loop.run_until_complete(self.ximalaya.get_selected_vip_sounds(sounds, album_name, start, end, headers))
                            print("专辑选定声音下载完成！")
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
