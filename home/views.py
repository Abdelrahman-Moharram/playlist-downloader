from django.shortcuts import render, redirect
from .models import Video, save_video, notification, report
from pytube.contrib.playlist import Playlist
from pytube import YouTube
from pytube.cli import on_progress
import datetime
import os
from datetime import datetime
from django.contrib import messages




def Download_Playlist(url, v_quality, vs_option):
    playlist = Playlist(url)
    # print(playlist)
    length = len(playlist.video_urls)
    print("Total Videos: ", length)
    folder = str(datetime.timestamp(datetime.now()))
    os.makedirs("media/files/"+folder)
    for video_url in playlist.video_urls:
        yt = YouTube(video_url, on_progress_callback=on_progress)
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
        return yt.title, folder, None, "mp3", yt.thumbnail_url, length
    return yt.title, folder, None, "mp4", yt.thumbnail_url, length

def Download_Video(url, v_quality, vs_option):
    folder = str(datetime.timestamp(datetime.now()))
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



def Report(request):
    if request.method == "POST":
        reprt = report.objects.create(message=request.POST['message'], Email=request.POST['Email'], image=request.FILES['image'])
        if request.user.username:
            reprt.user = request.user
        reprt.save()
        messages.success(request,"Message sent Succesfully! Thank U ",extra_tags="success")
        return redirect('home:index')
    return render(request, 'home/report.html', {})

def index(request):
    if request.method == "POST":
        vids = request.session["videos"]
        url = request.POST['url']
        if "list" in url :
            if "index" not in url:

                # download playlist
                downloaded = Download_Playlist(url, request.POST['v-quality'], request.POST['vs-option'])
                new_video = Video.objects.create(url=request.POST['url'], title=downloaded[0], d_datetime=downloaded[1], link_type=0, length=downloaded[5], quality= request.POST['v-quality'])
                new_video.thumbnail = downloaded[4]
                new_video.local_src =  save_video(new_video, downloaded[0], ext=downloaded[3])
                if request.user.username:
                    new_video.user = request.user
                new_video.save()
                vids.insert(0, new_video.id)
                videos = []
                for v in vids:
                    sv = Video.objects.filter(id=v)[0]
                    if sv:
                        videos.append(sv)
                request.session["videos"] = vids
                return render(request, "home/index.html", {"videos": videos})

        # download videos        
        downloaded = Download_Video(url, request.POST['v-quality'], request.POST['vs-option'])
        new_video = Video.objects.create(url=request.POST['url'], title=downloaded[0], d_datetime=downloaded[1], link_type=1, length=1, quality= request.POST['v-quality'])
        new_video.local_src = save_video(new_video, downloaded[0], ext=downloaded[3])
        new_video.thumbnail = downloaded[4]
        if downloaded[3] == "mp3":
            new_video.file_type = 0
        else:
            new_video.file_type = 1

        if request.user.username:
            new_video.user = request.user
        
        new_video.save()
        vids.insert(0, new_video.id)
        videos = []
        
        for v in vids:
            sv = Video.objects.filter(id=v)[0]
            if sv:
                videos.append(sv)
        request.session["videos"] = vids
        return render(request, "home/index.html", {"videos": videos})
    request.session["videos"] = []
    Video.objects.select_old()
    if request.user.username:
        return render(request, "home/index.html", {"notifications":notification.objects.filter(user=request.user, seen=False)})
    else:
        return render(request, "home/index.html", {})

def notfound404(request, exception):
    return render(request, "home/notfound404.html",{})


def notifications(request, notifyId):
    notify = notification.objects.get(id=notifyId)
    notify.seen = True
    notify.save()
    return redirect('home:index')


