import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy_splash import SplashRequest
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import MULTILASER

class MultilaserSpider(Spider):
    name = "multilaser-spider"
    start_urls = [urllib.parse.urljoin(MULTILASER, "/produtos/buscar/roteador")]

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield SplashRequest(
    #             url,
    #             callback=self.parse,
    #             endpoint="execute",
    #             args={"wait": 0.5}
    #         )

    def parse(self, response):
        ROUTER_SELECTOR = "//article[@class='products-list__item']"
        MODEL_SELECTOR = ".//h3[@class='products-list__title']/text()"
        MODEL_PAGE_SELECTOR = ".//a[contains(@class, 'products-list__link')]/@href"

        routers = response.xpath(ROUTER_SELECTOR)

        self.logger.info(f"Start crawling {len(routers)} pages")

        for router in routers:
            model = router.xpath(MODEL_SELECTOR).extract_first().split(" ")[-1]
            model_page = router.xpath(MODEL_PAGE_SELECTOR).extract_first()
            yield Request(
                url=urllib.parse.urljoin(MULTILASER, model_page),
                meta={"model_name": model},
                callback=self.parse_model
            )

    def parse_model(self, response):
        pass