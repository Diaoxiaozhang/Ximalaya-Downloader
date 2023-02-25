import requests
from lxml import etree
import math
import aiohttp
import aiofiles
import asyncio
import os


headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14"
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


# 下载选定专辑声音
async def get_selected_sounds(sounds, album_name, start, end):
    tasks = []
    session = aiohttp.ClientSession()
    for i in range(start, end + 1):
        sound_id = sounds[i - 1]["trackId"]
        sound_name, sound_url = analyze_sound(sound_id)
        tasks.append(asyncio.create_task(async_get_sound(sound_name, sound_url, album_name, session)))
    await asyncio.wait(tasks)
    await session.close()
