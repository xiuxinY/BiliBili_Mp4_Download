from os import rename
import youtube_dl
import os
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
import subprocess

class GetItem(object):
    def __init__(self):
        self.win = tk.Tk()  # Create instance
        self.win.title("B站mp4下载器")  # Add a title
        self.win.configure(background='SeaGreen3')

        self.create_widgets()

    def create_widgets(self):
        mighty = ttk.LabelFrame(self.win, text=' 欢迎余老师使用！ ')
        mighty.grid(column=0, row=0, padx=8, pady=4)

        label = ttk.Label(mighty, text="输入链接：")
        label.grid(column=0, row=0, sticky='W', padx=10, pady=3)

        self.var = tk.StringVar()
        self.entry = ttk.Entry(mighty, textvariable=self.var)
        self.entry.grid(column=0, row=1, sticky='W', padx=10, pady=3)

        self.action = ttk.Button(mighty, text="下载！", command=self.download)
        self.action.grid(column=0, row=2, sticky='W', padx=20, pady=3)

        self.excel_label = ttk.Label(mighty, text="等待下载")
        self.excel_label.grid(column=1, row=2, sticky='W', padx=20, pady=3)

    def rename_hook(self, d):
        if d['status'] == 'finished':
            self.file_name = '{}.mp4'.format(int(time.time()))
            rename(d['filename'], self.file_name)
            print('下载完成{}'.format(self.file_name))

    def download(self):
        self.youtube_url = self.var.get()
        ydl_opts = {
            'progress_hooks': [self.rename_hook],
            'outtmpl': '%(id)s%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # 下载给定的URL列表
            result = ydl.download([self.youtube_url])
        self.excel_label.configure(text="下载完成：\n" + self.file_name)

oop = GetItem()
oop.win.mainloop()

