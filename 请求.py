import json
# 该请求实现根据歌曲id拿到音乐链接
import requests
# 如果代码中有中文 把以下这段代码加入
import subprocess
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")

import execjs


def download(url):
    resp = requests.get(url)
    file_name = str(url).split("/")[-1]
    file_name = file_name + ".mp4"
    with open(file_name, "wb") as f:
        f.write(resp.content)


with open("jiami.js", "r", encoding="utf-8") as f:
    fn = f.read()
url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
id = "1895330088"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
js = execjs.compile(fn)
origin_data = js.call("get_data", id)
data = {
    "params": origin_data["encText"],
    "encSecKey": origin_data["encSecKey"]
}

res = requests.post(url=url, headers=headers, data=data)
json = json.loads(res.text)
music_url = json["data"][0]["url"]
print(music_url)
print("开始下载")
download(music_url)
print("下载完成")
