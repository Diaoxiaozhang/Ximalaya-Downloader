# -*- coding:utf-8 -*-
import asyncio
import json
import math
import os
import time
import logging
import traceback
import sys
import re
from fake_useragent import UserAgent
from base64 import b64decode
import subprocess
import aiofiles
import aiohttp
import requests
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from seleniumwire import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions
import colorama

version = "v0.5.5"
colorama.init(autoreset=True)
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('app.log', mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
path = ""
ua = UserAgent()
try:
    dws_path = os.path.join(sys._MEIPASS, "dws.exe")
except AttributeError:
    dws_path = "dws.exe"


class Ximalaya:
    def __init__(self):
        self.default_headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
        }
    
    def get_sid(self):
        retries = 3
        while retries > 0:
            try:
                sid = json.loads(subprocess.check_output(dws_path, shell=True).decode())["sid"]
                return sid
            except Exception as e:
                logger.debug(f'获取sid失败！')
                logger.debug(traceback.format_exc())
                retries -= 1
                return False

    # 解析声音，如果成功返回声音名和声音链接，否则返回False
    def analyze_sound(self, sound_id, headers, bid):
        logger.debug(f'开始解析ID为{sound_id}的声音')
        url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
        params = {
            "device": "www2",
            "trackId": sound_id,
            "trackQualityLevel": 2
        }
        headers["referer"] = f"https://www.ximalaya.com/sound/{sound_id}"
        headers["xm-sign"] = f"{bid}&&{self.get_sid()}"
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        try:
            not response.json()["trackInfo"]["isAuthorized"]
        except KeyError:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败，可能因为达到每日音频下载上限！')
            logger.debug(f'ID为{sound_id}的声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        if not response.json()["trackInfo"]["isAuthorized"]:
            return 0  # 未购买或未登录vip账号
        try:
            sound_name = response.json()["trackInfo"]["title"]
            encrypted_url_list = response.json()["trackInfo"]["playUrlList"]
        except Exception as e:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音解析失败！')
            logger.debug(traceback.format_exc())
            return False
        if encrypted_url_list[0]["type"][:2] == "AI":
            sound_info = {"name": sound_name, 0: "", 1: "", 2: ""}
            sound_info[0] = sound_info[1] = self.decrypt_url(encrypted_url_list[0]["url"])
            logger.debug(f'ID为{sound_id}的声音解析成功！')
            return sound_info
        else:
            sound_info = {"name": sound_name, 0: "", 1: "", 2: ""}
            for encrypted_url in encrypted_url_list:
                if encrypted_url["type"] == "M4A_128":
                    sound_info[2] = self.decrypt_url(encrypted_url["url"])
                elif encrypted_url["type"] == "MP3_64":
                    sound_info[1] = self.decrypt_url(encrypted_url["url"])
                elif encrypted_url["type"] == "MP3_32":
                    sound_info[0] = self.decrypt_url(encrypted_url["url"])
            logger.debug(f'ID为{sound_id}的声音解析成功！')
            return sound_info

    # 解析专辑，如果成功返回专辑名和专辑声音列表，否则返回False
    def analyze_album(self, album_id, headers, bid):
        logger.debug(f'开始解析ID为{album_id}的专辑')
        url = "https://www.ximalaya.com/revision/album/v1/getTracksList"
        params = {
            "albumId": album_id,
            "pageNum": 1,
            "sort": 0,
            "pageSize": 100
        }
        headers["referer"] = f"https://www.ximalaya.com/album/{album_id}"
        headers["xm-sign"] = f"{bid}&&{self.get_sid()}"
        retries = 5
        while True:
            try:
                response = requests.get(url, headers=headers, params=params, timeout=15)
            except Exception as e:
                print(colorama.Fore.RED + f'ID为{album_id}的专辑解析失败！')
                logger.debug(f'ID为{album_id}的专辑解析失败！')
                logger.debug(traceback.format_exc())
                return False, False
            if response.json()["data"]["tracks"] == []:
                retries -= 1
            else:
                break
            if retries == 0:
                print(colorama.Fore.RED + f'ID为{album_id}的专辑解析失败！')
                logger.debug(f'ID为{album_id}的专辑解析失败！')
                return False, False
        pages = math.ceil(response.json()["data"]["trackTotalCount"] / 100)
        sounds = []
        for page in range(1, pages + 1):
            params = {
                "albumId": album_id,
                "pageNum": page,
                "sort": 0,
                "pageSize": 100
            }
            retries = 5
            while True:
                sid = self.get_sid()
                if not sid:
                    print(colorama.Fore.RED + f'ID为{album_id}的专辑解析失败！')
                    logger.debug(f'ID为{album_id}的专辑解析失败！')
                    return False, False
                else:
                    headers["xm-sign"] = f"{bid}&&{sid}"
                try:
                    response = requests.get(url, headers=headers, params=params, timeout=30)
                except Exception as e:
                    print(colorama.Fore.RED + f'ID为{album_id}的专辑解析失败！')
                    logger.debug(f'ID为{album_id}的专辑解析失败！')
                    logger.debug(traceback.format_exc())
                    return False, False
                if response.json()["data"]["tracks"] == []:
                    print(f"第{page}页解析失败第{6-retries}次，共{pages}页")
                    retries -= 1
                else:
                    print(f"第{page}页解析成功，共{pages}页")
                    break
                if retries == 0:
                    print(colorama.Fore.RED + f'ID为{album_id}的专辑解析失败！')
                    logger.debug(f'ID为{album_id}的专辑解析失败！')
                    return False, False
            sounds += response.json()["data"]["tracks"]
        album_name = sounds[0]["albumTitle"]
        logger.debug(f'ID为{album_id}的专辑解析成功')
        return album_name, sounds

    # 协程解析声音
    async def async_analyze_sound(self, sound_id, session, headers, bid):
        logger.debug(f'开始解析ID为{sound_id}的声音')
        retries = 3
        url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
        params = {
            "device": "www2",
            "trackId": sound_id,
            "trackQualityLevel": 2
        }
        headers["referer"] = f"https://www.ximalaya.com/sound/{sound_id}"
        sid = self.get_sid()
        if not sid:
            print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
            logger.debug(f'ID为{sound_id}的声音解析失败！')
            return False
        else:
            headers["xm-sign"] = f"{bid}&&{sid}"
        while retries > 0:
            try:
                async with session.get(url, headers=headers, params=params, timeout=20) as response:
                    response_json = json.loads(await response.text())
                    sound_name = response_json["trackInfo"]["title"]
                    encrypted_url_list = response_json["trackInfo"]["playUrlList"]
                    break
            except KeyError:
                print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败，可能因为达到每日音频下载上限')
                logger.debug(f'ID为{sound_id}的声音解析失败！')
                logger.debug(traceback.format_exc())
                return False
            except Exception as e:
                logger.debug(f'ID为{sound_id}的声音解析失败！')
                logger.debug(traceback.format_exc())
            retries -= 1
            if retries == 0:
                print(colorama.Fore.RED + f'ID为{sound_id}的声音解析失败！')
                logger.debug(f'ID为{sound_id}的声音解析失败！')
                return False
        if not response_json["trackInfo"]["isAuthorized"]:
            return 0  # 未购买或未登录vip账号
        if encrypted_url_list[0]["type"][:2] == "AI":
            sound_info = {"name": sound_name, 0: "", 1: "", 2: ""}
            sound_info[0] = sound_info[1] = self.decrypt_url(encrypted_url_list[0]["url"])
            logger.debug(f'ID为{sound_id}的声音解析成功！')
            return sound_info
        else:
            sound_info = {"name": sound_name, 0: "", 1: "", 2: ""}
            for encrypted_url in encrypted_url_list:
                if encrypted_url["type"] == "M4A_128":
                    sound_info[2] = self.decrypt_url(encrypted_url["url"])
                elif encrypted_url["type"] == "MP3_64":
                    sound_info[1] = self.decrypt_url(encrypted_url["url"])
                elif encrypted_url["type"] == "MP3_32":
                    sound_info[0] = self.decrypt_url(encrypted_url["url"])
            logger.debug(f'ID为{sound_id}的声音解析成功！')
            return sound_info

    # 将文件名中不能包含的字符替换为空格
    def replace_invalid_chars(self, name):
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in name:
                name = name.replace(char, " ")
        return name

    # 下载单个声音
    def get_sound(self, sound_name, sound_url, path):
        print("正在下载，请稍等……")
        retries = 3
        sound_name = self.replace_invalid_chars(sound_name)
        if '?' in sound_url:
            type = sound_url.split('?')[0][-3:]
        else:
            type = sound_url[-3:]
        if os.path.exists(f"{path}/{sound_name}.{type}"):
            print(f'{sound_name}已存在！')
            return
        while retries > 0:
            try:
                logger.debug(f'开始下载声音{sound_name}')
                response = requests.get(sound_url, headers=self.default_headers, timeout=60)
                break
            except Exception as e:
                logger.debug(f'{sound_name}第{4 - retries}次下载失败！')
                logger.debug(traceback.format_exc())
                retries -= 1
        if retries == 0:
            print(colorama.Fore.RED + f'{sound_name}下载失败！')
            logger.debug(f'{sound_name}经过三次重试后下载失败！')
            return False
        sound_file = response.content
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"{path}/{sound_name}.{type}", mode="wb") as f:
            f.write(sound_file)
        print(f'{sound_name}下载完成！')
        logger.debug(f'{sound_name}下载完成！')

    # 协程下载声音
    async def async_get_sound(self, sound_name, sound_url, album_name, session, path, global_retries, num=None):
        retries = 3
        logger.debug(f'开始下载声音{sound_name}')
        if num is None:
            sound_name = self.replace_invalid_chars(sound_name)
        else:
            sound_name = f"{num}-{sound_name}"
            sound_name = self.replace_invalid_chars(sound_name)
        if '?' in sound_url:
            type = sound_url.split('?')[0][-3:]
        else:
            type = sound_url[-3:]
        album_name = self.replace_invalid_chars(album_name)
        if not os.path.exists(f"{path}/{album_name}"):
            os.makedirs(f"{path}/{album_name}")
        if os.path.exists(f"{path}/{album_name}/{sound_name}.{type}"):
            print(f'{sound_name}已存在！')
            return None
        while retries > 0:
            try:
                async with session.get(sound_url, headers=self.default_headers, timeout=120) as response:
                    async with aiofiles.open(f"{path}/{album_name}/{sound_name}.{type}", mode="wb") as f:
                        await f.write(await response.content.read())
                print(f'{sound_name}下载完成！')
                logger.debug(f'{sound_name}下载完成！')
                break
            except Exception as e:
                logger.debug(f'{sound_name}第{global_retries * 3 + 4 - retries}次下载失败！')
                logger.debug(traceback.format_exc())
                retries -= 1
                if os.path.exists(f"{path}/{album_name}/{sound_name}.{type}"):
                    os.remove(f"{path}/{album_name}/{sound_name}.{type}")
        if retries == 0:
            return ([sound_name, sound_url, album_name, session, path, global_retries, num])

    # 下载专辑中的选定声音
    async def get_selected_sounds(self, sounds, album_name, start, end, headers, bid, quality, number, path):
        print("正在下载，请稍等……")
        tasks = []
        global_retries = 0
        max_global_retries = 2
        session = aiohttp.ClientSession()
        digits = len(str(len(sounds)))
        for i in range(start - 1, end):
            sound_id = sounds[i]["trackId"]
            tasks.append(asyncio.create_task(self.async_analyze_sound(sound_id, session, headers, bid)))
        sounds_info = await asyncio.gather(*tasks)
        tasks = []
        if number:
            num = start
            for sound_info in sounds_info:
                if sound_info is False or sound_info == 0:
                    continue
                num_ = str(num).zfill(digits)
                if quality == 2 and sound_info[2] == "":
                     quality = 1
                tasks.append(asyncio.create_task(self.async_get_sound(sound_info["name"], sound_info[quality], album_name, session, path, global_retries, num_)))
                num += 1
        else:
            for sound_info in sounds_info:
                if sound_info is False or sound_info == 0:
                    continue
                if quality == 2 and sound_info[2] == "":
                    quality = 1
                tasks.append(asyncio.create_task(self.async_get_sound(sound_info["name"], sound_info[quality], album_name, session, path, global_retries)))
        failed_downloads = [result for result in await asyncio.gather(*tasks) if result is not None]
        while failed_downloads and global_retries < max_global_retries:
            tasks = [asyncio.create_task(self.async_get_sound(*failed_download)) for failed_download in failed_downloads]
            failed_downloads = [result for result in await asyncio.gather(*tasks) if result is not None]
            global_retries += 1
        print("专辑全部选定声音下载完成！")
        if failed_downloads:
            for failed_download in failed_downloads:
                print(colorama.Fore.RED + f'声音{failed_download[0]}下载失败！')
        await session.close()

    # 解密vip声音url
    def decrypt_url(self, encrypted_url):
        o = bytes([183, 174, 108, 16, 131, 159, 250, 5, 239, 110, 193, 202, 153, 137, 251, 176, 119, 150, 47, 204, 97, 237, 1, 71, 177, 42, 88, 218, 166, 82, 87, 94, 14, 195, 69, 127, 215, 240, 225, 197, 238, 142, 123, 44, 219, 50, 190, 29, 181, 186, 169, 98, 139, 185, 152, 13, 141, 76, 6, 157, 200, 132, 182, 49, 20, 116, 136, 43, 155, 194, 101, 231, 162, 242, 151, 213, 53, 60, 26, 134, 211, 56, 28, 223, 107, 161, 199, 15, 229, 61, 96, 41, 66, 158, 254, 21, 165, 253, 103, 89, 3, 168, 40, 246, 81, 95, 58, 31, 172, 78, 99, 45, 148, 187, 222, 124, 55, 203, 235, 64, 68, 149, 180, 35, 113, 207, 118, 111, 91, 38, 247, 214, 7, 212, 209, 189, 241, 18, 115, 173, 25, 236, 121, 249, 75, 57, 216, 10, 175, 112, 234, 164, 70, 206, 198, 255, 140, 230, 12, 32, 83, 46, 245, 0, 62, 227, 72, 191, 156, 138, 248, 114, 220, 90, 84, 170, 128, 19, 24, 122, 146, 80, 39, 37, 8, 34, 22, 11, 93, 130, 63, 154, 244, 160, 144, 79, 23, 133, 92, 54, 102, 210, 65, 67, 27, 196, 201, 106, 143, 52, 74, 100, 217, 179, 48, 233, 126, 117, 184, 226, 85, 171, 167, 86, 2, 147, 17, 135, 228, 252, 105, 30, 192, 129, 178, 120, 36, 145, 51, 163, 77, 205, 73, 4, 188, 125, 232, 33, 243, 109, 224, 104, 208, 221, 59, 9])
        a = bytes([204, 53, 135, 197, 39, 73, 58, 160, 79, 24, 12, 83, 180, 250, 101, 60, 206, 30, 10, 227, 36, 95, 161, 16, 135, 150, 235, 116, 242, 116, 165, 171])
        encrypted_url = encrypted_url.replace('_', '/').replace('-', '+')
        padding = '=' * (-len(encrypted_url) % 4)
        encrypted_data = b64decode(encrypted_url + padding)
        if len(encrypted_data) < 16:
            return encrypted_url
        data = encrypted_data[:-16]
        iv = encrypted_data[-16:]
        decrypted_data = bytearray(data)
        for i in range(len(decrypted_data)):
            decrypted_data[i] = o[decrypted_data[i]]
        for i in range(0, len(decrypted_data), 16):
            block = decrypted_data[i:i+16]
            decrypted_data[i:i+16] = bytes(a ^ b for a, b in zip(block, iv))
        for i in range(0, len(decrypted_data), 32):
            block = decrypted_data[i:i+32]
            decrypted_data[i:i+32] = bytes(a ^ b for a, b in zip(block, a))
        return decrypted_data.decode('utf-8')

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

    # 获取配置文件中的cookie和path
    def analyze_config(self):
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            with open("config.json", "w", encoding="utf-8") as f:
                config = {
                    "cookie": "",
                    "path": "",
                    "bid": "",
                }
                json.dump(config, f)
            return False, False, False
        try:
            cookie = config["cookie"]
        except Exception:
            config["cookie"] = ""
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f)
            cookie = False
        try:
            path = config["path"]
        except Exception:
            config["path"] = ""
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f)
            path = False
        try:
            bid = config["bid"]
            if bid == "":
                bid = False
        except Exception:
            config["bid"] = ""
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f)
            bid = False
        return cookie, path, bid

    # 判断登录信息是否有效
    def judge_config(self, cookie, bid):
        url = "https://www.ximalaya.com/revision/my/getCurrentUserInfo"
        headers = {
            "user-agent": ua.random,
            "cookie": cookie
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
        except Exception as e:
            print(colorama.Fore.RED + "无法获取喜马拉雅用户数据，请检查网络状况！")
            logger.debug("无法获取喜马拉雅用户数据！")
            logger.debug(traceback.format_exc())
        if response.json()["ret"] == 200:
            url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time()*1000)}?device=www2&trackId=359357383&trackQualityLevel=1"
            headers["xm-sign"] = f"{bid}&&{self.get_sid()}"
            try:
                requests.get(url, headers=headers, timeout=15).json()["trackInfo"]
            except KeyError:
                return False
            except Exception:
                print(colorama.Fore.RED + "无法获取喜马拉雅用户数据，请检查网络状况！")
                logger.debug("无法获取喜马拉雅用户数据！")
                logger.debug(traceback.format_exc())
                return False
            return response.json()["data"]["userName"]
        else:
            return False
            
    # 登录喜马拉雅账号
    def login(self):
        print("请选择浏览器：")
        print("1. Google Chrome")
        print("2. Microsoft Edge")
        choice = input()
        print("请等待到浏览器窗口弹出后登录喜马拉雅账号，登录成功后浏览器会自动关闭")
        if choice == "1":
            option = webdriver.ChromeOptions()
            option.add_experimental_option("detach", True)
            option.add_experimental_option('excludeSwitches', ['enable-logging'])
            option.page_load_strategy = 'eager'
            driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=option)
        elif choice == "2":
            option = webdriver.EdgeOptions()
            option.add_experimental_option("detach", True)
            option.add_experimental_option('excludeSwitches', ['enable-logging'])
            option.page_load_strategy = 'eager'
            driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install(), options=option)
        else:
            return
        driver.get("https://passport.ximalaya.com/page/web/login")
        try:
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'jymain')))
            driver.get("https://www.ximalaya.com/sound/62919401")
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, 'xm-player')))
            time.sleep(1)
            retries = 3
            while retries > 0:
                for request in driver.requests:
                    if request.url == "https://www.ximalaya.com/m-revision/page/track/queryRelativeTracksById?trackId=62919401&preOffset=9&nextOffset=0&countKeys=play&order=2":
                        with open("config.json", "r", encoding="utf-8") as f:
                            config = json.load(f)
                        for key, value in request.headers.items():
                            if key.lower() == "cookie":
                                config["cookie"] = value
                            if key.lower() == "xm-sign":
                                pattern = r"^(.*?)&&"
                                match = re.match(pattern, value)
                                config["bid"] = match.group(1)
                        break
                try:
                    with open("config.json", "w", encoding="utf-8") as f:
                        json.dump(config, f)
                    break
                except UnboundLocalError:
                    retries -= 1
                    time.sleep(1)
                    if retries == 0:
                        print(colorama.Fore.RED + "登录失败！")
                        logger.debug("登录失败！")
                        driver.quit()
                        return False
            logger.debug('以下是使用浏览器登录喜马拉雅账号时的浏览器日志：')
            for entry in driver.get_log('browser'):
                logger.debug(entry['message'])
            logger.debug('浏览器日志结束')
            driver.quit()
        except selenium.common.exceptions.TimeoutException:
            print(colorama.Fore.RED + "登录超时，自动返回主菜单！")
            logger.debug('以下是使用浏览器登录喜马拉雅账号时的浏览器日志：')
            for entry in driver.get_log('browser'):
                logger.debug(entry['message'])
            logger.debug('浏览器日志结束')
            driver.quit()
            return False
        username = self.judge_config(config["cookie"], config["bid"])
        print(f"成功登录账号{username}！")
