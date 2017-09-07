from __future__ import unicode_literals
from pathlib import Path
from video_download import youtube_dl
from netdisk_upload.bypy import ByPy
import os
vide_file_name = "video_address"
conf_file_name = "download.conf"
net_disk_map = "net_disk_list.txt"
video_url_list = []
conf_var = {}
net_disk_complete_map = {}

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

ydl_opts_simu = {
    'config_path':"~/Source",
    'json_path': os.path.join(os.getcwd(), "json_folder"),
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

ydl_opts = {
    'config_path':"~/Source",
    'download_path':"~/Youtube",
    'simulate' : False,
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

def preload_local_data():
    video_file = Path(vide_file_name)
    if video_file.exists() and video_file.is_file():
        f_video_list = open(vide_file_name, "r")
        lines = f_video_list.readlines()
        f_video_list.close()
        for line in lines:
            if line is not "" and line[0:4] == "http" and line not in video_url_list:
                video_url_list.append(line)
        print(video_url_list)
    else:
        print("Video file not exists, abort!!!!")
        return

    conf_file = Path(conf_file_name)
    if conf_file.exists() and conf_file.is_file():
        f_conf = open(conf_file_name, "r")
        content = f_conf.read()
        conf_var = eval(content)
        print(conf_var)

    for video_link_item in video_url_list:
        with youtube_dl.YoutubeDL(ydl_opts_simu) as ydl:
            ydl.download([video_link_item])

    if Path(net_disk_map).exists() and Path(net_disk_map).is_file():
        f_disk = open(net_disk_map, "r")
        disk_content_lines = f_disk.readlines()
        f_disk.close()
        disk_content_lines = disk_content_lines[1:]
        bp = ByPy()
        for disk_line in disk_content_lines:
            if disk_line.split(" ")[0] == "D":
                folder_name = " ".join(disk_line.split(" ")[1: -3])
                net_disk_complete_map[folder_name] = []
                for video_list_item in (bp.list(folder_name))[1:]:
                    net_disk_complete_map[folder_name].append(" ".join(video_list_item.split(" ")[1: -3]))
            else:
                net_disk_complete_map[" ".join(disk_line.split(" ")[1: -3])] = -1
        print(net_disk_complete_map)



    for folder, folder_detail in net_disk_complete_map.items():
        if Path(folder + ".json").exists() and Path(folder + ".json").is_file():
            with open(folder + ".json") as f:
                json_content = f.read()
                video_count = int(eval(json_content)["n_entries"])
                if len(folder_detail) == video_count*2:
                    os.remove(folder + ".json")

preload_local_data()
