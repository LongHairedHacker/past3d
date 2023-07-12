from django.urls import re_path

from pastebin.views import GeometryView, GeometryListView, GeometryCreate, GeometryDelete

urlpatterns = [
    re_path(r'^new/$', GeometryCreate.as_view(), name='geometry_create'),
    re_path(r'^list/$', GeometryListView.as_view(), name='geometry_list'),
    re_path(r'^list/page/(?P<page>[0-9]+)/$', GeometryListView.as_view(), name='geometry_list'),
    re_path(r'^delete/(?P<id>\d+)/$', GeometryDelete.as_view(), name='geometry_delete'),
    re_path(r'^(?P<id>\d+)/$', GeometryView.as_view(), name='geometry_details')
]