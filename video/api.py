from rest_framework.generics import ListAPIView
from video.filters import VideoFilter
from video.models import Video
from video.serializer import VideoSerializer


class VideoListAPI(ListAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
    filterset_class = VideoFilter

