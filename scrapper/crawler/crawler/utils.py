import json
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import datetime
from .spiders.youtube import YoutubeSpider
import os


def scrap_youtube_data(channels):
    logging.getLogger('scrapy').setLevel(logging.WARNING)
    settings = get_project_settings()
    filename = f'results_{datetime.datetime.now().timestamp()}.json'
    settings.set('FEED_FORMAT', 'json')
    settings.set('FEED_URI', filename)
    crawler = CrawlerProcess(settings)
    crawler.crawl(YoutubeSpider, channels=channels)
    crawler.start()
    with open(filename) as scraped_data:
        ret_list = json.load(scraped_data)
    os.remove(filename)
    return ret_list
