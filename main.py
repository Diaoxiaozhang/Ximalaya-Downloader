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
from lxml import etree

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14",
    "cookie": "_xmLog=h5&5e6ed5db-6ab7-4c49-9830-f69a4f052506&process.env.sdkVersion; fds_otp=6043714892552979561; 1&remember_me=y; 1&_token=74284569&32B85180240N0EA2DDABC8B2D2BEB3B13E80FD6FDC679A50801E0989C966A94E25F6F693C0F9114MCE18290D482A411_; login_type=password_mobile; xm-page-viewid=ximalaya-web; impl=www.ximalaya.com.login; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1677297967,1677319931,1677330706,1677376271; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1677376271; web_login=1677376524640"
}


# 解析声音
def analyze_sound(sound_id):
    url = "https://www.ximalaya.com/revision/play/v1/audio"
    params = {
        "id": sound_id,
        "ptype": 1
    }
    response = requests.get(url, headers=headers, params=params)
    sound_url = response.json()["data"]["src"]
    url = "https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/1677297989848"
    params = {
        "device": "web",
        "trackId": sound_id,
        "trackQualityLevel": 1
    }
    response = requests.get(url, headers=headers, params=params)
    sound_name = response.json()["trackInfo"]["title"]
    return sound_name, sound_url


# 解析专辑
def analyze_album(album_id):
    url = f"https://www.ximalaya.com/album/{album_id}"
    response = requests.get(url, headers=headers)
    tree = etree.HTML(response.text)
    episodes = tree.xpath('//*[@id="anchor_sound_list"]/div[1]/span[1]/span/text()[2]')[0]
    pages = math.ceil(int(episodes) / 100)
    url = "https://www.ximalaya.com/revision/album/v1/getTracksList"
    sounds = []
    for page in range(1, pages + 1):
        params = {
            "albumId": album_id,
            "pageNum": page,
            "sort": 0,
            "pageSize": 100
        }
        response = requests.get(url, headers=headers, params=params)
        sounds += response.json()["data"]["tracks"]
    album_name = sounds[0]["albumTitle"]
    return album_name, sounds


# 协程解析声音
async def async_analyze_sound(sound_id, session):
    url = "https://www.ximalaya.com/revision/play/v1/audio"
    params = {
        "id": sound_id,
        "ptype": 1
    }
    async with session.get(url, headers=headers, params=params) as response:
        sound_url = json.loads(await response.text())["data"]["src"]
    url = "https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/1677297989848"
    params = {
        "device": "web",
        "trackId": sound_id,
        "trackQualityLevel": 1
    }
    async with session.get(url, headers=headers, params=params) as response:
        sound_name = json.loads(await response.text())["trackInfo"]["title"]
    return sound_name, sound_url


# 将文件名中不能包含的字符替换为空格
def replace_invalid_chars(name):
    invalid_chars = ['/', '\\', ':,' '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        if char in name:
            name = name.replace(char, " ")
    return name


# 下载单个声音
def get_sound(sound_name, sound_url):
    response = requests.get(sound_url, headers=headers)
    sound_file = response.content
    if not os.path.exists(f"./download"):
        os.makedirs(f"./download")
    with open(f"./download/{sound_name}.m4a", mode="wb") as f:
        f.write(sound_file)


# 协程下载声音
async def async_get_sound(sound_name, sound_url, album_name, session):
    sound_name = replace_invalid_chars(sound_name)
    album_name = replace_invalid_chars(album_name)
    if not os.path.exists(f"./download/{album_name}"):
        os.makedirs(f"./download/{album_name}")
    async with session.get(sound_url, headers=headers) as response:
        async with aiofiles.open(f"./download/{album_name}/{sound_name}.m4a", mode="wb") as f:
            await f.write(await response.content.read())


# 下载专辑中的选定声音
async def get_selected_sounds(sounds, album_name, start, end):
    tasks = []
    session = aiohttp.ClientSession()
    for i in range(start, end + 1):
        sound_id = sounds[i - 1]["trackId"]
        tasks.append(asyncio.create_task(async_analyze_sound(sound_id, session)))
    sounds = await asyncio.gather(*tasks)
    for sound in sounds:
        tasks.append(asyncio.create_task(async_get_sound(sound[0], sound[1], album_name, session)))
    await asyncio.wait(tasks)
    await session.close()


# 解密vip声音url
def decrypt_url(ciphertext):
    key = binascii.unhexlify("aaad3e4fd540b0f79dca95606e72bf93")
    ciphertext = base64.urlsafe_b64decode(ciphertext + '=' * (4 - len(ciphertext) % 4))
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    plaintext = re.sub(r"[^\x20-\x7E]", "", plaintext.decode("utf-8"))
    return plaintext


# 获取vip声音的加密url
def get_encrypted_url(sound_id):
    url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
    params = {
        "device": "web",
        "trackId": sound_id,
        "trackQualityLevel": 1
    }
    response = requests.get(url, headers=headers, params=params)
    encrypted_url = response.json()["trackInfo"]["playUrlList"][0]["url"]
    return encrypted_url


# 协程获取vip声音的加密url
async def async_get_encrypted_url(sound_id, session):
    url = f"https://www.ximalaya.com/mobile-playpage/track/v3/baseInfo/{int(time.time() * 1000)}"
    params = {
        "device": "web",
        "trackId": sound_id,
        "trackQualityLevel": 1
    }
    response = session.get(url, headers=headers, params=params)
    encrypted_url = json.loads(await response.text())["trackInfo"]["playUrlList"][0]["url"]
    return encrypted_url


# 判断专辑是否为vip专辑
def judge_album(album_id):
    url = "https://www.ximalaya.com/revision/album/v1/simple"
    params = {
        "albumId": album_id
    }
    response = requests.get(url, headers=headers, params=params)
    if response.json()["data"]["albumPageMainInfo"]["isPaid"] == "false":
        return "free"
    elif response.json()["data"]["albumPageMainInfo"]["hasBuy"] == "true":
        return "bought"
    else:
        return "not_bought"


# 判断声音是否为vip声音
def judge_sound(sound_id):
    url = "https://www.ximalaya.com/revision/track/simple"
    params = {
        "trackId": sound_id
    }
    response = requests.get(url, headers=headers, params=params)
