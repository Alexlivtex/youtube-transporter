#encoding: utf-8
from __future__ import unicode_literals
from pathlib import Path
import video_download.YoutubeDL as YoutubeDL
import netdisk_upload.bypy as ByPy
import os
import pickle
import shutil
import sys
reload(sys)
vide_file_name = "video_address"
conf_file_name = "download.conf"
net_disk_map = "netdisk_map.pickle"
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
    'json_path': "./",
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
    'format': 'bestvideo/mp4',
    'format': 'mp4',
    'dump_single_json' : False,
    'writeautomaticsub' : True,
    'outtmpl' : "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s",
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
    sys.setdefaultencoding('utf8')
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
        f_conf.close()
        conf_var = eval(content)
        print(conf_var)

    for video_link_item in video_url_list:
        with YoutubeDL(ydl_opts_simu) as ydl:
            ydl.download([video_link_item])

    #os.system("mv *.json json_folder/")


    disk_content_lines=get_folder_list("")
    for disk_line in disk_content_lines:
        if disk_line.split(" ")[0] == "D":
            folder_name = " ".join(disk_line.split(" ")[1: -4])
            net_disk_complete_map[folder_name] = []
            for video_list_item in get_folder_list(folder_name):
                net_disk_complete_map[folder_name].append(" ".join(video_list_item.split(" ")[1: -4]))

        else:
            file_name = " ".join(disk_line.split(" ")[1: -4])
            net_disk_complete_map[file_name] = []

    for key, value in net_disk_complete_map.items():
        print("%s has %d items"%(key, len(value)))


    for folder, folder_detail in net_disk_complete_map.items():
        if Path(folder + ".json").exists() and Path(folder + ".json").is_file():
            with open(folder + ".json") as f:
                json_content = f.read()
                video_count = int(eval(json_content)["n_entries"])
                net_disk_video_count = 0
                if len(folder_detail) > 0:
                    for video_item in folder_detail:
                        if video_item.split(".")[-1] == "mp4":
                            net_disk_video_count += 1
                    if video_count == net_disk_video_count:
                        os.remove(folder + ".json")
                else:
                    os.remove(folder + ".json")


    json_list = []
    for current_folder_item in os.listdir(os.getcwd()):
        if current_folder_item.split(".")[-1] == "json":
            json_list.append(os.path.join(os.getcwd(), current_folder_item))

    #os.chdir(conf_var["download_path"])
    os.chdir("/root/youtube_video")
    bp = ByPy.ByPy()
    for item in json_list:
        with open(item, "r") as f_json:
            json_file_content = eval(f_json.read())
            f_json.close()
            video_link = json_file_content["webpage_url"]
            print(video_link)
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])
            try:
                bp.upload()
            except:
                print("%s upload failed"%(video_link))
                continue
            folder_finished = json_file_content["playlist"]
            print(folder_finished)
            os.system("rm -rf ./*")
            os.remove(item)



def get_folder_list(path):
    bp = ByPy.ByPy()
    bp.list(path)
    f = open(net_disk_map, "r")
    folder_list = pickle.load(f)
    f.close()
    os.remove(net_disk_map)
    return folder_list
    
preload_local_data()