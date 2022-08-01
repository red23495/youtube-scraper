from django.test import TestCase
from rest_framework.test import APIClient


class VideoAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        from video.models import Video, VideoTag, Tag
        code_tag = Tag.objects.create(id=1, name='code')
        c_tag = Tag.objects.create(id=4, name='c++')
        game_tag = Tag.objects.create(id=2, name='game')
        fifa_tag = Tag.objects.create(id=5, name='fifa')
        music_tag = Tag.objects.create(id=3, name='music')
        lp_tag = Tag.objects.create(id=6, name='lp')
        code_video = Video.objects.create(id='code', title='coding video', channel_id='coding_channel', fhv=50, fhv_rating=0.5)
        game_video = Video.objects.create(id='game', title='gaming video', channel_id='gaming_channel', fhv=100, fhv_rating=1)
        music_video = Video.objects.create(id='music', title='music video', channel_id='music_channel', fhv=150, fhv_rating=1.5)
        VideoTag.objects.create(tag=code_tag, video=code_video)
        VideoTag.objects.create(tag=c_tag, video=code_video)
        VideoTag.objects.create(tag=game_tag, video=game_video)
        VideoTag.objects.create(tag=fifa_tag, video=game_video)
        VideoTag.objects.create(tag=music_tag, video=music_video)
        VideoTag.objects.create(tag=lp_tag, video=music_video)

    def test_get(self):
        client = APIClient()
        response = client.get('/video/api/list/')
        match = [
            {
                'id': 'music',
                'channel_id': 'music_channel', 'title': 'music video', 'fhv': 150,
                'fhv_rating': '1.500000', 'tags': ['music', 'lp'],
            },
            {
                'id': 'game', 'tags': ['game', 'fifa'], 'channel_id': 'gaming_channel', 'title': 'gaming video',
                'fhv': 100, 'fhv_rating': '1.000000'
            },
            {
                'id': 'code', 'tags': ['code', 'c++'], 'channel_id': 'coding_channel',
                'title': 'coding video', 'fhv': 50,
                'fhv_rating': '0.500000'
            }
        ]
        self.assertEqual(response.json()['results'], match)
        self.assertEqual(response.status_code, 200)

    def test_tag_filter(self):
        client = APIClient()
        response = client.get('/video/api/list/?tags=1')
        match = [
            {
                'id': 'code', 'tags': ['code', 'c++'], 'channel_id': 'coding_channel',
                'title': 'coding video', 'fhv': 50,
                'fhv_rating': '0.500000'
            }
        ]
        self.assertEqual(response.json()['results'], match)
        self.assertEqual(response.status_code, 200)
        response = client.get('/video/api/list/?tags=2,3')
        match = [
            {
                'id': 'music',
                'channel_id': 'music_channel', 'title': 'music video', 'fhv': 150,
                'fhv_rating': '1.500000', 'tags': ['music', 'lp'],
            },
            {
                'id': 'game', 'tags': ['game', 'fifa'], 'channel_id': 'gaming_channel', 'title': 'gaming video',
                'fhv': 100, 'fhv_rating': '1.000000'
            },
        ]
        self.assertEqual(response.json()['results'], match)
        self.assertEqual(response.status_code, 200)

    def test_rating_filter(self):
        client = APIClient()
        response = client.get('/video/api/list/?rating_from=0.0&rating_to=1.0')
        match = [
            {
                'id': 'game', 'tags': ['game', 'fifa'], 'channel_id': 'gaming_channel', 'title': 'gaming video',
                'fhv': 100, 'fhv_rating': '1.000000'
            },
            {
                'id': 'code', 'tags': ['code', 'c++'], 'channel_id': 'coding_channel',
                'title': 'coding video', 'fhv': 50,
                'fhv_rating': '0.500000'
            }
        ]
        self.assertEqual(response.json()['results'], match)
        self.assertEqual(response.status_code, 200)
        response = client.get('/video/api/list/?rating_from=0.0&rating_to=0.5')
        match = [
            {
                'id': 'code', 'tags': ['code', 'c++'], 'channel_id': 'coding_channel',
                'title': 'coding video', 'fhv': 50,
                'fhv_rating': '0.500000'
            }
        ]
        self.assertEqual(response.json()['results'], match)
        self.assertEqual(response.status_code, 200)
        response = client.get('/video/api/list/?rating_from=1&rating_to=2')
        match = [
            {
                'id': 'music',
                'channel_id': 'music_channel', 'title': 'music video', 'fhv': 150,
                'fhv_rating': '1.500000', 'tags': ['music', 'lp'],
            },
            {
                'id': 'game', 'tags': ['game', 'fifa'], 'channel_id': 'gaming_channel', 'title': 'gaming video',
                'fhv': 100, 'fhv_rating': '1.000000'
            }
        ]
        self.assertEqual(response.json()['results'], match)
        self.assertEqual(response.status_code, 200)
