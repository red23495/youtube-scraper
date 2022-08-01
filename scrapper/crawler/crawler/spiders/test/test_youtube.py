import json
import unittest
from ..youtube import YoutubeSpider
import os
from ... import settings


class YoutubeTest(unittest.TestCase):

    def get_crawler(self):
        settings.API_KEY = 'DEMO_KEY'
        return YoutubeSpider(channels=['test_channel'])

    def test_channel_processing(self):
        crawler = self.get_crawler()
        expected_url = 'https://youtube.googleapis.com/youtube/v3/playlistItems/' \
                       '?key=DEMO_KEY&part=contentDetails&playlistId=UURWXAQsN5S3FPDHY4Ttq1Xg&maxResults=50'
        path = os.path.join(*os.path.split(__file__)[:-1])
        with open(os.path.join(path, 'channel_data.json')) as datafile:
            data = json.load(datafile)
            out = crawler.process_channel(data)
            assert len(out) == 1, "Incorrect no of response found"
            assert out[0].url == expected_url, "Invalid playlist url"

    def test_playlist_processing(self):
        crawler = self.get_crawler()
        expected_url = 'https://youtube.googleapis.com/youtube/v3/videos/' \
                       '?key=DEMO_KEY&part=snippet,statistics' \
                       '&id=mCuxbI0FqzM,X_01ytMQzDw,mkYSHzSN0mM,W4zEAtIUcbI,MLzcci5HL0Y&maxResults=50'
        next_page_url = 'http://example.com&pageToken=EAAaBlBUOkNESQ&maxResults=50'
        path = os.path.join(*os.path.split(__file__)[:-1])
        with open(os.path.join(path, 'playlist_item_data.json')) as datafile:
            data = json.load(datafile)
            out = crawler.process_playlist(data, url='http://example.com')
            assert len(out) == 2, "Incorrect no of response found"
            assert out[0].url == expected_url, "Invalid video url"
            assert out[1].url == next_page_url, "Invalid next page url"

    def test_video_processing(self):
        crawler = self.get_crawler()
        path = os.path.join(*os.path.split(__file__)[:-1])
        with open(os.path.join(path, 'video_expected.json')) as expected_file:
            expected_data = json.load(expected_file)
        with open(os.path.join(path, 'video_data.json')) as datafile:
            data = json.load(datafile)
            out = crawler.process_video(data, url='http://example.com')
            self.assertListEqual(out, expected_data, ""), "Invalid video data received"


if __name__ == '__main__':
    unittest.main()
