import os.path
import struct
import re

from hashlib import md5
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

vertex_pattern = re.compile(r'vertex\s+([0-9.e+-]+)\s+([0-9.e+-]+)\s+([0-9.e+-]+)')

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
	user = models.ForeignKey(User, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	polycount = models.IntegerField(blank=True, default=0)
	width = models.FloatField(blank=True, default=0)
	depth = models.FloatField(blank=True, default=0)
	height = models.FloatField(blank=True, default=0)
	file = models.FileField(upload_to=safe_upload_path('models'))
	sourcefile = models.FileField(upload_to=safe_upload_path('sources'), blank=True)

	def _generate_meta_infos(self):
		print "Generating metainfos %s" % self.name

		self.file.open()

		count = 0
		min_coord = [None,None,None]
		max_coord = [None,None,None]	

		if self.file.read(5) != "solid":
			print "binary"
			#Skip header
			self.file.seek(80)
			count = struct.unpack("i",self.file.read(4))[0]	

			done = False
			for pos in range(0,count):
				#Skip normal (3 * 32bit)
				self.file.seek(self.file.tell()+3*4)
				#Loop over each coordinate
				for vert in range(0,3):
					# Loop over each coordinate 
					for i in range(0,3):
						x = struct.unpack("<f",self.file.read(4))[0]	

						if min_coord[i] != None :
							min_coord[i] = min(min_coord[i], x)
						else:
							min_coord[i] = x
						
						if max_coord[i] != None :
							max_coord[i] = max(max_coord[i], x)
						else:
							max_coord[i] = x
				#Skip attributes (16bit) 
				self.file.seek(self.file.tell()+2)	

		else:
			print "ascii"		

			line = self.file.readline()
			while line != "":
				line = line.strip()
				if line.startswith("facet"):
					count = count + 1
				if line.startswith("vertex"):
					coords = vertex_pattern.match(line).groups();
					for i in range(0,3):
						x = float(coords[i])	

						if min_coord[i] != None :
							min_coord[i] = min(min_coord[i], x)
						else:
							min_coord[i] = x
						
						if max_coord[i] != None :
							max_coord[i] = max(max_coord[i], x)
						else:
							max_coord[i] = x	

				line = self.file.readline()

		self.file.close()
			
		self.width = max_coord[0] - min_coord[0]
		self.depth = max_coord[1] - min_coord[1]
		self.height = max_coord[2] - min_coord[2]	
		self.polycount = count

	def get_polycount(self):
		if self.polycount == 0:
			self._generate_meta_infos()
		return self.polycount

	def get_width(self):
		if self.polycount == 0:
			self._generate_meta_infos()
		return self.width

	def get_depth(self):
		if self.polycount == 0:
			self._generate_meta_infos()
		return self.depth

	def get_height(self):
		if self.polycount == 0:
			self._generate_meta_infos()
		return self.height


