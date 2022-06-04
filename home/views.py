from wsgiref.util import FileWrapper
from django.shortcuts import redirect, render, HttpResponse
from pytube.contrib.playlist import Playlist
from pytube import YouTube
from pytube.cli import on_progress
import datetime
import os
from .models import Video, save_video, thumbnail_upload
import pathlib,urllib.request,uuid






def Download_Playlist(url, v_quality, vs_option):
    playlist = Playlist(url)
    # print(playlist)
    print("Total Videos: ",len(playlist.video_urls))
    folder = str(datetime.datetime.timestamp(datetime.datetime.now()))
    os.makedirs("media/files/"+folder)
    for video_url in playlist.video_urls:
        yt=YouTube(video_url,on_progress_callback=on_progress)
        if vs_option != "video":
            stream = yt.streams.get_audio_only()
        else:
            if v_quality == "highest":
                stream = yt.streams.get_highest_resolution()
            elif v_quality == "lowest":
                stream = yt.streams.get_lowest_resolution()
            else:
                stream = yt.streams.filter(resolution=v_quality, res=v_quality).first()
        print(yt.title)
        stream.download(filename="media/files/"+folder+"/"+yt.title+".mp4")
    return yt.title, folder, None, "mp4", yt.thumbnail_url

def Download_Video(url, v_quality, vs_option):
    folder = str(datetime.datetime.timestamp(datetime.datetime.now()))
    os.makedirs("media/files/"+folder)
    yt=YouTube(url,on_progress_callback=on_progress)
    if vs_option != "video":
        stream = yt.streams.get_audio_only()
    else:
        if v_quality == "highest":
            stream = yt.streams.get_highest_resolution()
        elif v_quality == "lowest":
            stream = yt.streams.get_lowest_resolution()
        else:
            stream = yt.streams.filter(resolution=v_quality, res=v_quality).first()
    print(yt.title)
    return yt.title, folder,  stream.download(filename="media/files/"+folder+"/"+yt.title+".mp4"), "mp4", yt.thumbnail_url




def index(request):
    if request.method == "POST":
        url = request.POST['url']
        if "list" in url :
            if "index" not in url:
        
                # download playlist

                downloaded = Download_Playlist(url, request.POST['v-quality'], request.POST['vs-option'])
                new_video = Video.objects.create(url=request.POST['url'], title=downloaded[0], d_datetime=downloaded[1])
                new_video.thumbnail = thumbnail_upload(downloaded[1], filename=downloaded[4].split("/")[-1])
                new_video.local_src =  save_video(new_video, downloaded[0], ext=downloaded[3])
                if request.user.username:
                    new_video.user = request.user
                new_video.save()
                return render(request, "home/index.html",{"video":new_video})
        

        # download videos
        


        downloaded = Download_Video(url, request.POST['v-quality'], request.POST['vs-option'])

        # filename = str(uuid.uuid4())
        # file_ext = pathlib.Path(downloaded[4]).suffix
        # picture_filename = filename + file_ext
        # downloads_path = "media/thumbnails/%s/"%(downloaded[1])
        # picture_path  = os.path.join(downloads_path, picture_filename)
        thumbnail,extention = downloaded[4].split("/")[-1].split(".")
        print("thumbnail,extention = ", thumbnail,extention)
        urllib.request.urlretrieve(downloaded[4], "media/thumbnails/%s/%s.%s"%(downloaded[1],thumbnail,extention))


        new_video = Video.objects.create(url=request.POST['url'], title=downloaded[0], d_datetime=downloaded[1], thumbnail=downloaded[4])
        new_video.local_src =  save_video(new_video, downloaded[0], ext=downloaded[3])
        new_video.thumbnail = thumbnail_upload(downloaded[1], filename=downloaded[4].split("/")[-1])

        if request.user.username:
            new_video.user = request.user
        new_video.save()
        return render(request, "home/index.html",{"video":new_video})
                
    return render(request, "home/index.html",{})