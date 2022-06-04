import imp
from django.db import models
from django.contrib.auth.models import User
import zipfile
import os

class Playlist(models.Model):
	user				= models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
	url 				= models.CharField(max_length=500)
	title 			= models.CharField(max_length=200)
	d_datetime	= models.CharField(max_length=50)
	
def getExtention(filename, ext=None):
	if ext:
		return filename, ext
	if "." not in filename:
		return filename.split(".")
	for c in range (len(filename)-1,0,-1):
		print(c, " => ",filename[c])
		if c == ".":
			return filename[c:]
	return filename.split(".")

def thumbnail_upload(d_datetime,filename):
        thumbnail,extention = getExtention(filename)
        return "media/thumbnails/%s/%s.%s"%(d_datetime,thumbnail,extention)

def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])
                


def save_video(instance,filename, ext=None):	
	zip_directory("media/files/%s"%(instance.d_datetime), "media/files/%s.zip"%(instance.d_datetime))
	return "media/files/%s.zip"%(instance.d_datetime)

class Video(models.Model):
	
	title 			= models.CharField(max_length=300)
	url 				= models.CharField(max_length=500)
	d_datetime	= models.CharField(max_length=50)
	user				= models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
	local_src 	= models.FileField(upload_to=save_video)
	thumbnail 	= models.FileField(upload_to=thumbnail_upload)

	def __str__(self):
		return self.title


