import requests


# 下载单个声音
def get_sound(sound_id):
    url = "https://www.ximalaya.com/revision/play/v1/audio"
    params = {
        "id": sound_id,
        "ptype": 1
    }
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1660.14"
    }
    response = requests.get(url, params=params, headers=headers)
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
