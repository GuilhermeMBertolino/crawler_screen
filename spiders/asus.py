import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy_splash import SplashRequest
from splash_scripts.scripts import scroll_down_script
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import ASUS

class AsusSpider(Spider):
    name = "asus-spider"
    start_urls = [urllib.parse.urljoin(ASUS, "/networking-iot-servers/wifi-routers/asus-wifi-routers/filter?Series=ASUS-WiFi-Routers")]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(
                url, 
                callback=self.parse,
                endpoint="execute",
                args={"wait": 0.5, "lua_source": scroll_down_script})

    def parse(self, response):
        ROUTER_SELECTOR = "//div[contains(@class, 'filter_product_list')]"
        
        routers = response.xpath(ROUTER_SELECTOR)

        print(len(routers))

    def parse_model(self, response):
        pass