import scrapy
from scrapy import Spider
from scrapy import Request
from time import sleep
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import INTELBRAS

class IntelbrasSpider(Spider):
    name = "intelbras-spider"
    start_urls = [INTELBRAS]

    def parse(self, response):
        pass

    def parse_model(self, response):
        pass