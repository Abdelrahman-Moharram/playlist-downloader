from wsgiref.util import FileWrapper
from django.shortcuts import redirect, render, HttpResponse
from pytube.contrib.playlist import Playlist
from pytube import YouTube
from pytube.cli import on_progress
import datetime
import os
from .models import Video, save_video

def Download_Playlist(url, v_quality, vs_option):
    playlist = Playlist(url)
    # print(playlist)
    print("Total Videos: ",len(playlist.video_urls))
    folder = str(datetime.datetime.timestamp(datetime.datetime.now()))
    os.makedirs("media\\files\\"+folder)
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
        stream.download(filename="media\\files\\"+folder+"\\"+yt.title+".mp4")
    return yt.title, folder, None, "mp4"

def Download_Video(url, v_quality, vs_option):
    folder = str(datetime.datetime.timestamp(datetime.datetime.now()))
    os.makedirs("media\\files\\"+folder)
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
    return yt.title, folder,  stream.download(filename="media\\files\\"+folder+"\\"+yt.title+".mp4"), "mp4"




def index(request):
    if request.method == "POST":
        url = request.POST['url']
        if "list" in url :
            if "index" in url:
                downloaded = Download_Video(url, request.POST['v-quality'], request.POST['vs-option'])
                new_video = Video.objects.create(url=request.POST['url'], title=downloaded[0], d_datetime=downloaded[1])
                new_video.local_src =  save_video(new_video, downloaded[0], ext=downloaded[3])
                if request.user.username:
                    new_video.user = request.user
                
                new_video.save()
                print("\n\n\n\n\n",new_video.local_src,"\n\n\n\n\n")
                return render(request, "home/index.html",{"video":new_video})
            else:
                downloaded = Download_Playlist(url, request.POST['v-quality'], request.POST['vs-option'])
                new_video = Video.objects.create(url=request.POST['url'], title=downloaded[0], d_datetime=downloaded[1])
                new_video.local_src =  save_video(new_video, downloaded[0], ext=downloaded[3])
                if request.user.username:
                    new_video.user = request.user
                new_video.save()
                return render(request, "home/index.html",{"video":new_video})
        else :
            downloaded = Download_Video(url, request.POST['v-quality'], request.POST['vs-option'])
            new_video = Video.objects.create(url=request.POST['url'], title=downloaded[0], d_datetime=downloaded[1])
            new_video.local_src =  save_video(new_video, downloaded[0], ext=downloaded[3])
            if request.user.username:
                new_video.user = request.user
            new_video.save()
            print("\n\n\n\n\n",new_video.local_src,"\n\n\n\n\n")
            return render(request, "home/index.html",{"video":new_video})
        
        
        
        print(downloaded)            
        
    return render(request, "home/index.html",{})