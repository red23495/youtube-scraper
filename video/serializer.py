from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Video
        fields = '__all__'
