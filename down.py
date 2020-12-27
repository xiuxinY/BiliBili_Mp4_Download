from os import rename
import youtube_dl
import os
import time

class GetItem(object):

    def rename_hook(self, d):
        if d['status'] == 'finished':
            file_name = '{}.mp4'.format(int(time.time()))
            rename(d['filename'], file_name)
            ffmpeg = 'ffmpeg.exe'
            fn = file_name
            output = file_name + '.mp4'
            cmd = ffmpeg + " -i " + fn + " -c copy " + output
            print(cmd)
            res = os.popen(cmd)
            output_str = res.read()
            print(output_str)
            print('下载完成{}'.format(file_name))

    def download(self, youtube_url):
        ydl_opts = {
            'progress_hooks': [self.rename_hook],
            'outtmpl': '%(id)s%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            result = ydl.download([youtube_url])

if __name__ == '__main__':
    getItem = GetItem()
    url_todo = input("请输入您复制的视频链接：")
    getItem.download(url_todo)

input('按回车键退出~')
