from django.conf.urls import patterns, include, url

from views import GeometryView

urlpatterns = patterns('',
        (r'^g/(?P<id>\d+)/$', GeometryView.as_view()),)