import scrapy
from scrapy import Spider
from scrapy import Request
from scrapy_selenium import SeleniumRequest
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from browser_webdriver import By, WebDriverWait, TimeoutException, EC
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

        FIRMWARE_BAR_SELECTOR = "//h6[text()='firmware']"
        DOWNLOAD_LINK_SELECTOR = "//a[starts-with(@href, 'https://fw-download.ubnt.com')]/@href"

        firmware_bar = response.xpath(FIRMWARE_BAR_SELECTOR)

        if not firmware_bar:
            self.logger.info(f"No firmware available for {response.meta['model_name']}")
            return
        
        download_link = response.xpath(DOWNLOAD_LINK_SELECTOR).extract_first()
        print(download_link)

        self.logger.info(f"Downloading firmware for {response.meta['model_name']}")

        
