import youtube_dl

ydl_opts = {
    'format': 'bestaudio/best',
    "simulate" : True,

}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])