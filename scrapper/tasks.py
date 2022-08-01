from __future__ import absolute_import, unicode_literals
from celery import shared_task

from .crawler.crawler.utils import scrap_youtube_data
from multiprocessing import Process, Manager
import datetime


def scrap_worker(channels, return_list):
    return_list.extend(scrap_youtube_data(channels) or [])


def process_video_data(dataset):
    from video.models import Video, Tag, VideoTag
    from scrapper.models import ScrapedData
    tags = create_new_tag_model_from_video_dataset(dataset)
    Tag.objects.bulk_create(tags)
    videos, video_tags = create_new_video_and_video_tag_model_from_video_dataset(dataset)
    Video.objects.bulk_create(videos)
    VideoTag.objects.bulk_create(video_tags)
    stats = create_statistics_model_from_video_data(dataset)
    ScrapedData.objects.bulk_create(stats)


def create_new_video_and_video_tag_model_from_video_dataset(dataset):
    from video.models import Video, Tag, VideoTag
    existing_video_ids = Video.get_existing_video_ids()
    all_tag_map = Tag.get_name_id_dict()
    videos = []
    video_tags = []
    for data in dataset:
        if data['id'] in existing_video_ids:
            continue
        videos.append(
            Video(
                id=data['id'],
                channel_id=data['snippet']['channelId'],
                title=data['snippet']['title']
            )
        )
        for tag in data['snippet'].get('tags', []):
            video_tags.append(
                VideoTag(video_id=data['id'], tag_id=all_tag_map[tag])
            )
    return videos, video_tags


def create_new_tag_model_from_video_dataset(dataset):
    from video.models import Tag
    existing_tag_names = Tag.get_existing_tag_names()
    tag_names = []
    for video_data in dataset:
        tag_names.extend(video_data["snippet"].get("tags", []))
    new_tag_names = set(tag_names).difference(existing_tag_names)
    return [Tag(name=name) for name in new_tag_names]


def create_statistics_model_from_video_data(dataset):
    from scrapper.models import ScrapedData
    return [
        ScrapedData(
            channel_id=data['snippet']['channelId'],
            video_id=data['id'],
            published_at=datetime.datetime.fromisoformat(data['snippet']['publishedAt'].replace("Z", "+00:00")),
            views=data["statistics"]["viewCount"],
        )
        for data in dataset
    ]


@shared_task(name="crawl_video")
def scrap_videos(*args, **kwargs):
    from scrapper.models import Channel
    channels = [channel.id for channel in Channel.objects.all()]
    manager = Manager()
    return_list = manager.list()
    process = Process(target=scrap_worker, args=(channels, return_list,))
    process.start()
    process.join()
    process_video_data(return_list)


@shared_task(name="process_stats")
def process_stats(*args, **kwargs):
    from django.db import transaction
    from scrapper.models import ScrapedData
    with transaction.atomic():
        dataset = ScrapedData.objects.filter(processed=False).all()
        process_fhv(dataset)
        for data in dataset:
            data.processed = True
        ScrapedData.objects.bulk_update(dataset, ['processed'], batch_size=5000)


def process_fhv(dataset):
    processed_videos = process_video_fhv(dataset)
    process_channel_fhv(processed_videos)


def process_video_fhv(dataset):
    from video.models import Video
    updated_video_fhv_map = {}
    updated_channel_id_set = set()
    for data in dataset:
        time_diff = data.scraped_at - data.published_at
        if time_diff <= datetime.timedelta(hours=1):
            updated_channel_id_set.add(data.channel_id)
            updated_video_fhv_map[data.video_id] = max(data.views, updated_video_fhv_map.get(data.video_id, 0))
    updated_videos = []
    to_update_videos = Video.objects.filter(channel_id__in=updated_channel_id_set).all()
    for video in to_update_videos:
        if video.id in updated_video_fhv_map:
            video.fhv = updated_video_fhv_map[video.id]
            updated_videos.append(video)
    Video.objects.bulk_update(updated_videos, ['fhv'], batch_size=5000)
    return to_update_videos


def process_channel_fhv(videos):
    from scrapper.models import Channel
    from video.models import Video
    channel_videos = {}
    for video in videos:
        if video.id not in channel_videos:
            channel_videos[video.channel_id] = []
        channel_videos[video.channel_id].append(video)
    channel_medians = {}
    to_update_videos = []
    for channel_id, video_list in channel_videos.items():
        fhv_list = sorted([video.fhv for video in video_list if video.fhv != 0])
        total_videos = len(fhv_list)
        if total_videos == 0:
            median = 0
        elif total_videos % 2:
            median = fhv_list[total_videos // 2]
        else:
            median = (fhv_list[total_videos // 2] + fhv_list[(total_videos // 2) - 1]) / 2
        channel_medians[channel_id] = median
        for video in video_list:
            video.fhv_rating = video.fhv / median if median != 0 else 0
        to_update_videos.extend(video_list)
    updated_channels = Channel.objects.filter(id__in=channel_medians.keys())
    for channel in updated_channels:
        channel.med_fhv = channel_medians[channel.id]
    Channel.objects.bulk_update(updated_channels, ['med_fhv'], batch_size=5000)
    Video.objects.bulk_update(to_update_videos, ['fhv_rating'], batch_size=5000)

