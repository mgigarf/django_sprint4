from django.urls import path

from .views import *

app_name = 'pages'

urlpatterns = [
    path('about/', about, name='about'),
    path('rules/', rules, name='rules'),
    path('404/', not_found, name='not_found'),
    path('403csrf/', forbidden, name='forbidden'),
    path('500', server_error, name='server_error'),
]
