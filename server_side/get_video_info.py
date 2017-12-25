from __future__ import unicode_literals
import youtube_dl
import os
import pickle
import shutil
from bypy import ByPy

youtube_data_path = os.path.join("Data", "YoutubeVideo")
video_address_path = os.path.join("config", "video_address")

finished_downloading_pickle = os.path.join("config", "finished_youtube.pickle")
finished_downloading_pickle_bak = os.path.join("config", "finished_youtube_bak.pickle")

finished_video_list = list()
total_video_list = list()

def download_video(update=False):
    global finished_video_list
    global total_video_list

    f_total_videolist = open(video_address_path, "r")
    for line in f_total_videolist.readlines():
        if not line.strip() or line[0] == '#':
            print("Blank line, skip!")
            continue
        else:
            total_video_list.append(line)
    f_total_videolist.close()

    if not update:
        if os.path.exists(finished_downloading_pickle):
            try:
                f_finished = open(finished_downloading_pickle, "rb")
                finished_video_list = pickle.load(f_finished)
                f_finished.close()
            except:
                f_finished = open(finished_downloading_pickle_bak, "rb")
                finished_video_list = pickle.load(f_finished)
                f_finished.close()

    ydl_opts = {
        #'format' : 'bestvideo/best',
        'format' : 'mp4',
        'outtmpl': os.path.join("Data", "YoutubeVideo", os.path.join("%(playlist)s", "%(playlist_index)s - %(title)s.%(ext)s")),
        'writeautomaticsub': True,
    }

    for video_link in total_video_list:
        if video_link not in finished_video_list:
            print("New video {} need to download!".format(video_link.strip()))
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])

            bp = ByPy()
            bp.upload("Data")
            bp.cleancache()
            shutil.rmtree(youtube_data_path)
            os.mkdir(youtube_data_path)

            finished_video_list.append(video_link)
            f_finished = open(finished_downloading_pickle, "wb")
            pickle.dump(finished_video_list, f_finished)
            f_finished.close()
            shutil.copy(finished_downloading_pickle, finished_downloading_pickle_bak)

        else:
            print("Link {} has already existed!".format(video_link.strip()))

    del finished_video_list
    del total_video_list
