from django.db import models
from django.contrib.auth.models import User
import zipfile
import os
from django.utils import timezone
import datetime

def save_video(instance,filename, ext=None):	
	zip_directory("media/files/%s"%(instance.d_datetime), "media/files/%s.zip"%(instance.d_datetime))
	return "media/files/%s.zip"%(instance.d_datetime)




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
                


		
class VideoManager(models.Manager):
    def select_old(self):
    	day_ago = timezone.now() - datetime.timedelta(days=1)
    	print("day_ago",day_ago)
    	return self.filter(pdatetime=day_ago)

class Video(models.Model):
	
	title 			= models.CharField(max_length=300)
	url 				= models.CharField(max_length=500)
	d_datetime	= models.CharField(max_length=50)
	user				= models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
	local_src 	= models.FileField(upload_to=save_video)
	thumbnail 	= models.CharField(max_length=300)
	file_type 	= models.IntegerField(default=1)
	link_type 	= models.IntegerField(default=1)
	length 			= models.IntegerField()
	quality 		= models.CharField(max_length=10, blank=True, null=True)
	pdatetime 	= models.DateTimeField(auto_now=True)
	
	objects 		= VideoManager()

	def __str__(self):
		return self.title
