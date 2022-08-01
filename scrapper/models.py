from django.db import models


class Channel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    med_fhv = models.DecimalField(default=0, max_digits=30, decimal_places=6, verbose_name="median first hour view")

    class Meta:
        db_table = 'channels'


class ScrapedData(models.Model):
    channel_id = models.CharField(max_length=64)
    video_id = models.CharField(max_length=64)
    scraped_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField()
    views = models.BigIntegerField()
    processed = models.BooleanField(default=False)

    class Meta:
        db_table = 'scrapped_data'
