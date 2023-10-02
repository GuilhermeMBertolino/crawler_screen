import scrapy
from scrapy import Spider
from scrapy import Request
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import NETGEAR

class NetgearSpider(Spider):
    name = "netgear-spider"
    start_urls = [NETGEAR]

    def parse(self, response):
        pass

    def parse_model(self, response):
        pass