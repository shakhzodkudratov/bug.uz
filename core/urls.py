from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<url>[a-zA-Z0-9]{6})/', views.short_url, name='short_url'),
    re_path(r'^stats/(?P<name>[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12})/',
            views.stats, name='stats'),
]
