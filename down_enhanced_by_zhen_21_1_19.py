from os import rename
import threading
import youtube_dl
import requests
import json

class GetItem(object):
    def rename_hook(self, d):
        if d['status'] == 'finished':
            file_name = '%s'% d['filename'] + '.mp4'
            rename(d['filename'], file_name)
            print('下载完成{}'.format(file_name))

    def download(self, youtube_url):
        p = str(youtube_url[0])
        ydl_opts = {
            'format': 'bestaudio/best',
            'progress_hooks': [self.rename_hook],
            'outtmpl': '[%(id)s]'+p,
        }
        url_list=youtube_url[1].split(',')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            result = ydl.download(url_list)
#多线程
def quick_down(url_todo):
    bvid_list = url_todo.split(',')
    url_list = []
    for bvid in bvid_list:
        res = requests.get('http://api.bilibili.com/x/web-interface/view?bvid=%s'%bvid)
        p=int(json.loads(res.text)['data']['videos'])
        for j in range(1,p+1):
            url_list.append([j,'%s%s?p=%s'%(base_url,bvid,j)])
    print(url_list)
    l = []
    for url in url_list:
        l.append(threading.Thread(target=getItem.download, args=(url,)))
    for thread in l:
        thread.start()
    for thread in l:
        thread.join()

if __name__ == '__main__':
    getItem = GetItem()
    base_url = 'https://www.bilibili.com/video/'
    url_todo = input("请输入视频BV号，多个BV用逗号隔开：")
    quick_down(url_todo)
    print('已退出程序')
