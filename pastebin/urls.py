from django.conf.urls import patterns, include, url

from views import GeometryView, GeometryCreate

urlpatterns = patterns('',
        url(r'^new/$', GeometryCreate.as_view()),
        url(r'^g/(?P<id>\d+)/$', GeometryView.as_view(), name = 'geometry_details'))