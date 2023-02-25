import requests
from lxml import etree
import math


headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14"
    }


# 下载单个声音
def get_sound(sound_id):
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
    response = requests.get(sound_url, headers=headers)
    sound_file = response.content
    with open(f"./download/{sound_name}.m4a", mode="wb") as f:
        f.write(sound_file)


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
