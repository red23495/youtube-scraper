from django.shortcuts import render
from video.models import Tag


def home(request):
    tags = Tag.objects.all()
    return render(request, 'home.html', context={'tags': tags})
