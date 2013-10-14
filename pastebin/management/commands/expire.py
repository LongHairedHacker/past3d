from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import utc

from pastebin.models import Geometry


class Command(BaseCommand):
    args = ''
    help = 'Remove expired pastes and their files.'

    def handle(self, *args, **options):
    	for expiration in [Geometry.HOUR, Geometry.DAY, Geometry.WEEK, Geometry.MONTH]:
    		expiration_time = datetime.utcnow().replace(tzinfo=utc) - Geometry.DELTAS[expiration]
    		for geometry in Geometry.objects.all().filter(expiration = expiration, date__lte = expiration_time):
    			self.stdout.write("Expiring geometry: %s" % geometry.name)
    			geometry.file.delete()
    			if geometry.sourcefile :
    				geometry.sourcefile.delete()
    			geometry.delete()
    	self.stdout.write("done")