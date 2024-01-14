import scrapy
from scrapy import Spider
from scrapy import Request
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import HUAWEI

class HuaweiSpider(Spider):
    name = "huawei-spider"
    start_urls = []

    def parse(self, response):
        pass

    def parse_model(self, response):
        pass