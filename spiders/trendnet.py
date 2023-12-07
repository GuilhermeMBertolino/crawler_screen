import scrapy
from scrapy import Spider
from scrapy import Request
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import TRENDNET

class TrendnetSpider(Spider):
    name = "trendnet-spider"
    start_urls = [urllib.parse.urljoin(TRENDNET, "/products/wifi/routers")]

    def parse(self, response):
        ROUTER_SELECTOR = "//div[contains(@class, 'box-product')]"
        MODEL_SELECTOR = ".//h5/text()"

        routers = response.xpath(ROUTER_SELECTOR)

        for router in routers:
            model_name = router.xpath(MODEL_SELECTOR).extract_first()
            yield Request(
                url=f"https://downloads.trendnet.com/{model_name}/firmware",
                meta={
                    "model_name": model_name
                },
                callback=self.parse_model
            )

    def parse_model(self, response):
        DOWNLOAD_LINK_SELECTOR = "//a/@href"

        if response.status == 404:
            self.logger.info(f"No firmware available for {response.meta['model_name']}")
            return

        download_link = response.xpath(DOWNLOAD_LINK_SELECTOR).getall()[1]

        self.logger.info(f"Downloading firmware for {response.meta['model_name']}")
        parse_link(f"https://downloads.trendnet.com/{download_link}", "trendnet", response.meta["model_name"])

        