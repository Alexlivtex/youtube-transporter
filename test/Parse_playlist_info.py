from __future__ import unicode_literals
from video_download import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'config_path':"~/Source",
    'download_path':"~/Youtube",
    'simulate' : True,
    'format': 'bestvideo/best',
    'dump_single_json' : False,
    '''
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    '''
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=RxjIOXstxCk&list=PLQVvvaa0QuDeN06s5ervxTfTcVvt-xpZN'])
