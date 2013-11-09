from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

from pastebin.models import Geometry

from views import *

urlpatterns = patterns('',
	url(r'^signup/$', UserCreateView.as_view(), name='signup'),
	url(r'^confirm/(?P<user_id>\d+)/$', SendConfirmationView.as_view(), name='send_confirmation'),
	url(r'^confirm/(?P<user_id>\d+)/(?P<token>.+)/$', CheckConfirmationView.as_view(), name='check_confirmation'),
	
	url(r'^update/(?P<user_id>\d+)/$', UserUpdateView.as_view(), name='user_update'),

	url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'template_name' : 'users/password_reset.html',
														'post_reset_redirect' : reverse_lazy('password_reset_sent')},
														name='password_reset'),
	
	url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)/(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'template_name' : 'users/password_reset_confirm.html',
														'post_reset_redirect' : reverse_lazy('login')},
														name='password_reset_confirm'),

	url(r'^password/reset/sent/$', 'django.contrib.auth.views.password_reset_done', {'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'template_name' : 'users/password_reset_sent.html',},
														name='password_reset_sent'),


	url(r'^login/$', 'django.contrib.auth.views.login', {'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'template_name' : 'users/login.html'},
														name='login'),

	url(r'^logout/$', 'django.contrib.auth.views.logout',{'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'next_page' : reverse_lazy('login')}, 
														name='logout'),
	)