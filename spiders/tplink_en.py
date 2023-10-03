import scrapy
from scrapy import Spider
from scrapy import Request
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import TPLINK_EN

class TPLink_enSpider(Spider):
    name = "tplink_en-spider"
    start_urls = [urllib.parse.urljoin(TPLINK_EN, "/en/support/download")]

    def parse(self, response):
        ROUTER_WIFI_SELECTOR = "//div[@data-class='wi-fi-routers']"
        ROUTER_5G_SELECTOR = "//div[@data-class='c-3g-4g-routers']"
        MODEL_SELECTOR = ".//a[@class='ga-click']"

        routers_1 = response.xpath(ROUTER_WIFI_SELECTOR)
        routers_2 = response.xpath(ROUTER_5G_SELECTOR)
        models = routers_1.xpath(MODEL_SELECTOR) + (routers_2.xpath(MODEL_SELECTOR))

        self.logger.info(f"Starting crawling of {len(models)} pages")

        for model in models:
            page_link = model.xpath("@href").extract_first()
            model_name = model.xpath("text()").extract_first()
            yield Request(
                url=urllib.parse.urljoin(TPLINK_EN, page_link),
                meta={
                    "model_name": model_name
                },
                callback=self.parse_model
            )

    def parse_model(self, response):
        FIRMWARE_CONTAINER_SELECTOR = "//div[@id='content_Firmware']"
        DOWNLOAD_LINK_SELECTOR1 = ".//a[@class='tp-dialog-btn tp-dialog-btn-white ga-click']"
        DOWNLOAD_LINK_SELECTOR2 = ".//a[@class='download-resource-btn ga-click']"

        firmware_container = response.xpath(FIRMWARE_CONTAINER_SELECTOR)

        if(not firmware_container):
            self.logger.info(f"No firmware available for {response.meta['model_name']}")
            return
        
        if(firmware_container.xpath(DOWNLOAD_LINK_SELECTOR1)):
            download_link = firmware_container.xpath(DOWNLOAD_LINK_SELECTOR1).xpath("@href").extract_first()
            print(download_link)
        else:
            download_link = firmware_container.xpath(DOWNLOAD_LINK_SELECTOR2).xpath("@href").extract_first()
            print(download_link)

        self.logger.info(f"Downloading firmware for {response.meta['model_name']}")
        parse_link(download_link, "tplink_en", response.meta["model_name"])