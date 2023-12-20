import scrapy
from scrapy import Spider
from scrapy import Request
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
        products = response.xpath(PRODUCT_SELECTOR)

        self.logger.info(f"Start crawling {len(products)} pages")

        for product in products:
            model = product.xpath(MODEL_SELECTOR).extract_first()
            model_code = re.search(r"\((.*?)\)", model).group()[1:-1]
            yield Request(
                url=urllib.parse.urljoin(NETGEAR, f"/support/download/?model={model_code}"),
                meta={"model_name": model_code},
                callback=self.parse_model
            )

    def parse_model(self, response):
        FIRMWARE_LINK_SELECTOR = "//p[contains(text(), 'Firmware')]/.."      

        driver.get(response.url)
        download_link = driver.find_element(By.XPATH, FIRMWARE_LINK_SELECTOR)

        if download_link:
            self.logger.info(f"Downloading firmware for {response.meta['model_name']}")
            parse_link(download_link.get_attribute("href"), "netgear", response.meta["model_name"])

        else:
            self.logger.info(f"No firmware available for {response.meta['model_name']}")

        