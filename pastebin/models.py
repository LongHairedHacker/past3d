import os.path
import struct

from hashlib import md5
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models



def safe_upload_path(base_dir):
	
	def generate_path(instance, filename):

		ext = os.path.splitext(filename)[1]

		md5sum = md5()
		md5sum.update(instance.name 
			+ str(datetime.now()) 
			+ filename)
		randomname = md5sum.hexdigest()

		return os.path.join(base_dir,'%s%s' % (randomname, ext))

	return generate_path



class Geometry(models.Model):
	name = models.CharField(max_length = 128)
	description = models.TextField(blank=True)
	user = models.ForeignKey(User, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	polycount = models.IntegerField(blank=True, default=0)
	file = models.FileField(upload_to=safe_upload_path('models'))
	sourcefile = models.FileField(upload_to=safe_upload_path('sources'), blank=True)

	def get_polycount(self):
		if self.polycount == 0:
			self.file.open()
			self.polycount = 0

			if self.file.read(5) != "solid":
				self.file.seek(80)
				self.polycount = struct.unpack("i",self.file.read(4))[0]
			else:
				line = self.file.readline()
				while line != "":
					line = line.strip()
					if line.startswith("facet"):
						self.polycount +=  1
					line = self.file.readline()	

			self.save()

		return self.polycount


