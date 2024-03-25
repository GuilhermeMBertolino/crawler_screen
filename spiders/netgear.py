import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
import sys, os
import urllib.parse, urllib.request
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from browser_webdriver import driver, By
from download_firmware import parse_link
from vendor_links import NETGEAR

class NetgearSpider(Spider):
    name = "netgear-spider"
    start_urls = [urllib.parse.urljoin(NETGEAR, "/home/wifi/routers")]

    def parse(self, response):
        PRODUCT_SELECTOR = "//div[@class='list-view product_buy_info']"
        MODEL_SELECTOR = ".//a/text()"
        MODEL_CODE_PATTERN = r"\((.*?)\)"
        products = response.xpath(PRODUCT_SELECTOR)

        self.logger.info(f"Start crawling {len(products)} pages")

        for product in products:
            model = product.xpath(MODEL_SELECTOR).extract_first()
            model_code = re.search(MODEL_CODE_PATTERN, model).group()[1:-1]
            yield SeleniumRequest(
                url=urllib.parse.urljoin(NETGEAR, f"/support/download/?model={model_code}"),
                meta={"model_name": model_code},
                callback=self.parse_model,
                wait_time=2
            )

    def parse_model(self, response):
        FIRMWARE_LINK_SELECTOR = "//p[contains(text(), 'Firmware')]/../@href"      

        download_link = response.xpath(FIRMWARE_LINK_SELECTOR)

        if download_link:
            self.logger.info(f"Downloading firmware for {response.meta['model_name']}")
            parse_link(download_link.extract_first(), "netgear", response.meta["model_name"])

        else:
            self.logger.info(f"No firmware available for {response.meta['model_name']}")

        