from .api import VideoListAPI
from . import views
from django.urls import path

urlpatterns = [
    path('api/list/', VideoListAPI.as_view(), name='video-api'),
]
