from django.db import models
from typing import Set


class Video(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    channel_id = models.CharField(max_length=64)
    title = models.CharField(max_length=256)
    fhv = models.IntegerField(default=0, help_text="first hour view")
    fhv_rating = models.DecimalField(default=0, decimal_places=6, max_digits=30, help_text="first hour view rating on channel")

    class Meta:
        db_table = 'videos'
        ordering = ('-fhv_rating',)

    @property
    def tags(self):
        return [tag.tag.name for tag in self.video_tags.all()]

    @classmethod
    def get_existing_video_ids(cls) -> Set[str]:
        return {video['id'] for video in cls.objects.values('id')}


class Tag(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = 'tags'

    @classmethod
    def get_existing_tag_names(cls) -> Set[str]:
        return {tag['name'] for tag in cls.objects.values('name')}

    @classmethod
    def get_name_id_dict(cls):
        return {tag.name: tag.id for tag in cls.objects.all()}


class VideoTag(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE,
        db_column='video_id',
        related_name='video_tags',
        related_query_name='video_tag'
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        db_column='tag_id',
        related_name='video_tags',
        related_query_name='video_tag'
    )

    class Meta:
        db_table = 'video_tags'
