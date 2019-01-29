# import urllib.request
# urllib.request.urlretrieve("http://m10.music.126.net/20190128163758/f84f7617e6d729e527c4cff7cd259035/ymusic/101f/02d0/4c23/d95247a7de901df7b22f33564bd5d5f9.mp3", './wangyi.mp3')

import requests
import json
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}
file_path = './author_home_page/item.json'
with open(file_path,'r') as file:
    for data in file.readlines():
        line = json.loads(data)
        res = requests.get(line["link"],headers=headers,verify=False)
        res.encoding = 'UTF-8'
        with open('./Wangyiyun_MP3/' + line["name"] + '.mp3','wb') as f:
            f.write(res.content)
            f.close()
