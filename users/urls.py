from django.urls import re_path, path, reverse_lazy
from django.contrib.auth import views as auth_views

from pastebin.models import Geometry

from users.views import *

urlpatterns = [
    re_path(r'^signup/$', UserCreateView.as_view(), name='signup'),
    re_path(r'^confirm/(?P<user_id>\d+)/$', SendConfirmationView.as_view(), name='send_confirmation'),
    re_path(r'^confirm/(?P<user_id>\d+)/(?P<token>.+)/$',
        CheckConfirmationView.as_view(),
        name='check_confirmation'),
    re_path(r'^update/(?P<user_id>\d+)/$', UserUpdateView.as_view(), name='user_update'),
    path('password/reset/',
        auth_views.PasswordResetView.as_view(), {
            'extra_context': {
                'latest_geometries': Geometry.get_latest()
            },
            'template_name': 'users/password_reset.html',
            'post_reset_redirect': reverse_lazy('password_reset_sent')
        },
        name='password_reset'),
    path('password/reset/confirm/',
        auth_views.PasswordResetConfirmView.as_view(), {
            'extra_context': {
                'latest_geometries': Geometry.get_latest()
            },
            'template_name': 'users/password_reset_confirm.html',
            'post_reset_redirect': reverse_lazy('login')
        },
        name='password_reset_confirm'),
    path('password/reset/sent/',
        auth_views.PasswordResetDoneView.as_view(), {
            'extra_context': {
                'latest_geometries': Geometry.get_latest()
            },
            'template_name': 'users/password_reset_sent.html',
        },
        name='password_reset_sent'),
    path('login/',
        auth_views.LoginView.as_view(), {
            'extra_context': {
                'latest_geometries': Geometry.get_latest()
            },
            'template_name': 'users/login.html'
        },
        name='login'),
    path('logout/',
        auth_views.LogoutView.as_view(), {
            'extra_context': {
                'latest_geometries': Geometry.get_latest()
            },
            'next_page': reverse_lazy('login')
        },
        name='logout'),
]