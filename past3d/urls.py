from django.urls import include, re_path, path
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

admin.autodiscover()

from past3d.views import HomeView

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    path('users/', include('users.urls')),
    path('3d/', include('pastebin.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
