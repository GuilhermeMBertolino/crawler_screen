import scrapy
from scrapy import Spider
from scrapy import Request
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import MERCUSYS

class MercusysSpider(Spider):
    name = "mercusys-spider"
    start_urls = [urllib.parse.urljoin(MERCUSYS, "/product/list-15445")]

    def parse(self, response):
        ROUTER_SELECTOR = "//div[@class='product-text']"
        MODEL_SELECTOR = ".//p[@class='product-model']/text()"

        routers = response.xpath(ROUTER_SELECTOR)

        self.logger.info(f"Start crawling {len(routers)} pages")

        for router in routers:
            model = router.xpath(MODEL_SELECTOR).extract_first()

            yield Request(
                url=urllib.parse.urljoin(MERCUSYS, f"/download/{model}#Firmware"),
                meta={"model_name": model},
                callback=self.parse_model
            )
    
    def parse_model(self, response):
        DOWNLOAD_LINK_SELECTOR = "//a[@class='download-btn ga-click']/@href"

        download_link = response.xpath(DOWNLOAD_LINK_SELECTOR)

        if not download_link:
            self.logger.info(f"No firmware available for {response.meta['model_name']}")
            return
        
        self.logger.info(f"Downloading firmware for {response.meta['model_name']}")
        parse_link(download_link.extract_first(), "mercusys", response.meta["model_name"])