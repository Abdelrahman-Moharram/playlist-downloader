from django.db import models
from django.contrib.auth.models import User
import zipfile
import os
from datetime import datetime, timedelta
import shutil
from django.utils import timezone
from django.db.models.signals import post_save
from django.core.cache import cache
from django.dispatch import receiver

class VideoManager(models.Manager):
	def select_old(self):
			userNone = Video.objects.filter(user=None)
			self.delete_data(userNone.exclude(local_src=None))
			userNone.delete()

			startdate = datetime(2011, 1, 25, 12, 0, 0, 423063)
			enddate = timezone.now() - timedelta(days=7)

			vids = Video.objects.filter(pdatetime__range=[startdate, enddate])
			vids.delete()
			self.delete_data(Video.objects.filter(pdatetime__range=[startdate, timezone.now() - timedelta(hours=1)]).exclude(local_src=None))

	def delete_data(self, vids):
		print("delete data => ",vids)
		for vid in vids:
			try:
				shutil.rmtree(str(vid.local_src).replace(".zip", ""))
			except:
				pass
			try:
				os.remove(str(vid.local_src))
			except:
				pass
			vid.local_src = None
			vid.save()


def save_video(instance,filename, ext=None):
	zip_directory("media/files/%s"%(instance.d_datetime), "media/files/%s.zip"%(instance.d_datetime))
	return "media/files/%s.zip"%(instance.d_datetime)


def getExtention(filename, ext=None):
	if ext:
		return filename, ext
	if "." not in filename:
		return filename.split(".")
	for c in range (len(filename)-1,0,-1):
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
	pdatetime		= models.DateTimeField(auto_now=True)
	objects 		= VideoManager()

	def __str__(self):
		return self.title

class notification(models.Model):
	title 		= models.CharField(max_length=50)
	body 			= models.TextField()
	date 			= models.DateTimeField(auto_now=True)
	user 			= models.ForeignKey(User, on_delete=models.CASCADE)
	seen 			= models.BooleanField(default=False)
	def __str__(self):
		return self.title
		
@receiver(post_save)
def clear_the_cache(**kwargs):
	cache.clear()