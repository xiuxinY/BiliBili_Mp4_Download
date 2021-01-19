import asyncio
import youtube_dl
from tqdm import tqdm
import requests
import json
import os
class CustomLogger:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def debug(self, msg):
        if self.verbose:
            print('DEBUG', msg)

    def warning(self, msg):
        if self.verbose:
            print('WARNING', msg)

    def error(self, msg):
        print('ERROR', msg)


def download_video(url: str, options: dict = None):
    global name
    tqdm.write(f'Downloading {url}')
    ydl_opts = options or {
        'logger': CustomLogger(verbose=False),
        'outtmpl': 'video/'+name+'/%(title)s-%(id)s.%(ext)s',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


async def run_in_executor(sync_func, *params):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, sync_func, *params)


async def async_main(playlist):

    tasks = [run_in_executor(download_video, url) for url in playlist]

    for future in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await future


def main(uid):
    global name
    global dcount
    global ignorecount
    info_url="https://api.bilibili.com/x/space/acc/info?mid=%s&jsonp=jsonp"%(uid)
    search_url="https://api.bilibili.com/x/space/arc/search?mid=%s&pn=%s&ps=100&jsonp=jsonp&tid="%(uid,1)
    res = requests.get(search_url)
    info=json.loads(requests.get(info_url).text)['data']
    data=json.loads(res.text)['data']
    name,count,vlist='['+info['name']+'('+str(ignorecount+1)+'-'+str(ignorecount+dcount)+')'+str(uid)+']',data['page']['count'],data['list']['vlist']
    pcount=count//100 if count%100==0 else count//100+1
    print("视频总页数是",pcount)
    if pcount>1:
        for i in range(2,pcount+1):
            cur_search_url="https://api.bilibili.com/x/space/arc/search?mid=%s&pn=%s&ps=100&jsonp=jsonp"%(uid,i)
            cur_vlist=json.loads(requests.get(search_url).text)['data']['list']['vlist']
            vlist.extend(cur_vlist)
    #print(len(vlist))
    os.makedirs('video\\%s'%(name))#youtube-dl创建目录的判断函数有时会报错，下载前直接创建目录可以避免
    base_url='https://www.bilibili.com/video/'
    playlist=[]
    for i in range(ignorecount,ignorecount+dcount):
        playlist.append(base_url+vlist[i]['bvid'])
    print(playlist)
    asyncio.run(async_main(playlist))
    print('下载完成')
if __name__ == '__main__':
    uid=input("输入up主id")
    dcount=int(input("输入下载的数量"))#建议不超过20，很容易占满带宽
    ignorecount=int(input("忽略前几条视频"))#从第ignorecount+1条开始下载
    name=''
    main(uid)
