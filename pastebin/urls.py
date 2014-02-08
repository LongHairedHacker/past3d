from django.conf.urls import patterns, include, url

from views import GeometryView, GeometryListView, GeometryCreate, GeometryDelete

urlpatterns = patterns('',
        url(r'^new/$', GeometryCreate.as_view(), name='geometry_create'),
        url(r'^list/$', GeometryListView.as_view(), name='geometry_list'),
        url(r'^list/page/(?P<page>[0-9]+)/$', GeometryListView.as_view(), name='geometry_list'),
        url(r'^delete/(?P<id>\d+)/$', GeometryDelete.as_view(), name='geometry_delete'),
        url(r'^(?P<id>\d+)/$', GeometryView.as_view(), name='geometry_details'))
		