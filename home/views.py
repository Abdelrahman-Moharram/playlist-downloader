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
            files = stream.download(filename="media/files/"+folder+"/"+yt.title+".mp3")

        else:
            if v_quality == "highest":
                stream = yt.streams.get_highest_resolution()
            elif v_quality == "lowest":
                stream = yt.streams.get_lowest_resolution()
            else:
                stream = yt.streams.filter(resolution=v_quality, res=v_quality).first()
            print(yt.title)
            files = stream.download(filename="media/files/"+folder+"/"+yt.title+".mp4")
    if vs_option != "video":
        return yt.title, folder, None, "mp3", yt.thumbnail_url
    return yt.title, folder, None, "mp4", yt.thumbnail_url

def Download_Video(url, v_quality, vs_option):
    folder = str(datetime.datetime.timestamp(datetime.datetime.now()))
    os.makedirs("media/files/"+folder)
    yt=YouTube(url,on_progress_callback=on_progress)
    if vs_option != "video":
        stream = yt.streams.get_audio_only()
        files = stream.download(filename="media/files/"+folder+"/"+yt.title+".mp3")
        return yt.title, folder,  files, "mp3", yt.thumbnail_url

    else:
        if v_quality == "highest":
            stream = yt.streams.get_highest_resolution()
        elif v_quality == "lowest":
            stream = yt.streams.get_lowest_resolution()
        else:
            stream = yt.streams.filter(resolution=v_quality, res=v_quality).first()
        print(yt.title)
        files = stream.download(filename="media/files/"+folder+"/"+yt.title+".mp4")
        return yt.title, folder,  files, "mp4", yt.thumbnail_url




def index(request):
    
    if request.method == "POST":
        if not request.session['videos']:
            print("\n\n\nhere\n\n\n")
            request.session['videos'] = []
        url = request.POST['url']
        if "list" in url :
            if "index" not in url:
        
                # download playlist

                downloaded = Download_Playlist(url, request.POST['v-quality'], request.POST['vs-option'])
                new_video = Video.objects.create(url=request.POST['url'], title=downloaded[0], d_datetime=downloaded[1])
                new_video.thumbnail = downloaded[4]
                new_video.local_src =  save_video(new_video, downloaded[0], ext=downloaded[3])
                if request.user.username:
                    new_video.user = request.user
                new_video.save()
                request.session['videos'].append(new_video.id)
                videos = []
                for v in request.session['videos']:
                    sv = Video.objects.filter(id=v)[0]
                    if sv:
                        videos.append(sv)
                    print("\n\n\n\n\n\nlists",v,":",videos,"\n\n\n\n\n\n")
                return render(request, "home/index.html",{"videos":videos})
        

        # download videos
        


        downloaded = Download_Video(url, request.POST['v-quality'], request.POST['vs-option'])

        new_video = Video.objects.create(url=request.POST['url'], title=downloaded[0], d_datetime=downloaded[1], thumbnail=downloaded[4])
        new_video.local_src =  save_video(new_video, downloaded[0], ext=downloaded[3])
        print(downloaded[4])
        new_video.thumbnail = downloaded[4]
        if request.user.username:
            new_video.user = request.user
        new_video.save()
        request.session['videos'].append(new_video.id)
        print("\n\n\n\n\n\nvideos",request.session['videos'],"\n\n\n\n\n\n")
        videos = []
        for v in request.session['videos']:
            sv = Video.objects.filter(id=v)[0]
            if sv:
                videos.append(sv)
            print("\n\n\n\n\n\nvideos",v,":",videos,"\n\n\n\n\n\n")
        return render(request, "home/index.html",{"videos":videos})
    
    return render(request, "home/index.html",{})