from django.conf.urls import patterns, include, url

from views import GeometryView, GeometryCreate, GeometryDelete

urlpatterns = patterns('',
        url(r'^new/$', GeometryCreate.as_view(), name='geometry_create'),
        url(r'^g/delete/(?P<id>\d+)/$', GeometryDelete.as_view(), name='geometry_delete'),
        url(r'^g/(?P<id>\d+)/$', GeometryView.as_view(), name='geometry_details'))