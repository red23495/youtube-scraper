import scrapy
from scrapy import Request
from typing import Callable, Dict
from django.conf import settings


class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    allowed_domains = ['youtube.googleapis.com']

    def __init__(self, channels=None, *args, **kwargs):
        super(YoutubeSpider, self).__init__(*args, **kwargs)
        self.channels = channels

    def start_requests(self):
        urls = [
            f'https://youtube.googleapis.com/youtube/v3/channels/?key={settings.API_KEY}&part=contentDetails&id={channel}'
            for channel in self.channels
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    @property
    def response_handlers(self) -> Dict[str, Callable]:
        return {
            "youtube#channelListResponse": self.process_channel,
            "youtube#playlistItemListResponse": self.process_playlist,
            "youtube#videoListResponse": self.process_video,
        }

    def parse(self, response: scrapy.http.TextResponse, **kwargs):
        data = response.json()
        response_type = data.get("kind")
        response_handler = self.response_handlers.get(response_type)
        if not response_handler:
            return
        for out in response_handler(data, url=response.url, response=response):
            yield out

    def process_channel(self, data: Dict, **kwargs):
        out = []
        for item in data['items']:
            playlist_id = item["contentDetails"]["relatedPlaylists"]["uploads"]
            out.append(Request(
                url=f'https://youtube.googleapis.com/youtube/v3/playlistItems/?key={settings.API_KEY}&part=contentDetails&playlistId={playlist_id}&maxResults=50',
                callback=self.parse
            ))
        return out

    def process_playlist(self, data, url: str, **kwargs):
        out = []
        video_ids = []
        for item in data['items']:
            video_id = item["contentDetails"]["videoId"]
            video_ids.append(video_id)
        next_page_token = data.get('nextPageToken')
        out.append(
            Request(
                url=f'https://youtube.googleapis.com/youtube/v3/videos/?key={settings.API_KEY}&part=snippet,statistics&id={",".join(video_ids)}&maxResults=50',
                callback=self.parse
            )
        )
        if next_page_token:
            out.append(
                Request(
                    url=f'{url}&pageToken={next_page_token}&maxResults=50',
                    callback=self.parse
                )
            )
        return out

    def process_video(self, data, **kwargs):
        return data["items"]
