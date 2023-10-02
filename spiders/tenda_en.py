import scrapy
from scrapy import Spider
from scrapy import Request
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import TENDA_EN

class Tenda_enSpider(Spider):
    name = "tenda_en-spider"
    start_urls = TENDA_EN

    def parse(self, response):
        pass

    def parse_model(self, response):
        pass