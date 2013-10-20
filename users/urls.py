from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

from pastebin.models import Geometry

from views import UserCreate

urlpatterns = patterns('',
	url(r'^signup/$', UserCreate.as_view(), name='user_signup'),
	url(r'^login/$', 'django.contrib.auth.views.login', {'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'template_name' : 'users/login.html'},
														name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout',{'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'next_page' : reverse_lazy('login')}, 
														name='logout'),)