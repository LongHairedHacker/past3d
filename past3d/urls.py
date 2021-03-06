from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from views import HomeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'past3d.views.home', name='home'),
    # url(r'^past3d/', include('past3d.foo.urls')),

    url(r'^$', HomeView.as_view(), name='home'),

	url(r'^users/', include('users.urls')),
    url(r'^3d/', include('pastebin.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
