from django.conf.urls import patterns, include, url

from pastebin.models import Geometry

urlpatterns = patterns('',
	url(r'^login/$', 'django.contrib.auth.views.login', {'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'template_name' : 'users/login.html'},
														name='login'))