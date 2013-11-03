from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy

from pastebin.models import Geometry

from views import UserCreate, SendConfirmationView, CheckConfirmationView

urlpatterns = patterns('',
	url(r'^signup/$', UserCreate.as_view(), name='signup'),
	url(r'^confirm/(?P<user_id>\d+)/$', SendConfirmationView.as_view(), name='send_confirmation'),
	url(r'^confirm/(?P<user_id>\d+)/(?P<token>.+)/$', CheckConfirmationView.as_view(), name='check_confirmation'),
	
	url(r'^login/$', 'django.contrib.auth.views.login', {'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'template_name' : 'users/login.html'},
														name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout',{'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'next_page' : reverse_lazy('login')}, 
														name='logout'),

	url(r'^password/change/$', 'django.contrib.auth.views.password_change',{'extra_context' : {'latest_geometries' : Geometry.get_latest()},
														'template_name' : 'users/password_change.html',
														'post_change_redirect' : reverse_lazy('login')}, 
														name='password_change'),
	)