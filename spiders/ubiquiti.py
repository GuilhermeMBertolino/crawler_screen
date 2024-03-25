import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys, os
import urllib.parse, urllib.request
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import UBIQUITI

class UbiquitiSpider(Spider):
    name = "ubiquiti-spider"
    start_urls = [urllib.parse.urljoin(UBIQUITI, "/us/en?category=all-wifi")]

    def parse(self, response):
        ROUTER_SELECTOR = "//a[starts-with(@href, '/us/en/pro/category/all-wifi/products')]"
        MODEL_SELECTOR = "./child::*[3]/text()"

        routers = response.xpath(ROUTER_SELECTOR)

        self.logger.info(f"Start crawling {len(routers)} pages")

        for router in routers:
            model = router.xpath(MODEL_SELECTOR).extract_first()
            yield SeleniumRequest(
                url=f"https://ui.com/download/software/{model.lower()}",
                callback=self.parse_model,
                wait_time=5,
                wait_until=EC.invisibility_of_element_located((By.CLASS_NAME, 'react-loading-skeleton')),
                meta={"model_name": model},
            )

    def parse_model(self, response):
        LINK_REGEX_PATTERN = r'https:.[^"]*?Firmware.[^"]*?\.(?:zip|bin|rar)'

        download_link = re.search(LINK_REGEX_PATTERN, response.body.decode("utf-8"), re.IGNORECASE)

        if download_link:
            self.logger.info(f"Downloading firmware for {response.meta['model_name']}")
            parse_link(download_link.group(), "ubiquiti", response.meta["model_name"])
        else:
            self.logger.info(f"No firmware available for {response.meta['model_name']}")
        
