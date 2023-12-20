import scrapy
from scrapy import Spider
from scrapy import Request
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import TENDA_BR

class Tenda_enSpider(Spider):
    name = "tenda_br-spider"
    start_urls = [urllib.parse.urljoin(TENDA_BR, "/br/products/roteadores.html")]

    def parse(self, response):
        PRODUCT_SELECTOR = "//div[@class='featured-content']"
        MODEL_SELECTOR = ".//h5/text()"
        # SEARCH_INPUT_SELECTOR = "//input[@id='txtModelkey']"
        products = response.xpath(PRODUCT_SELECTOR)

        self.logger.info(f"Start crawling {len(products)} pages")   

        for product in products:
            model = product.xpath(MODEL_SELECTOR).extract_first()

            yield Request(
                url=urllib.parse.urljoin(TENDA_BR, f"/br/searchdown/{model} Firmware.html"),
                meta={"model_name": model},
                callback=self.parse_model
            )

    def parse_model(self, response):
        LINK_SELECTOR = "//div[@class='ditem']//a/@href"
        download_boxes = response.xpath(LINK_SELECTOR)

        if download_boxes:
            firmware_page = download_boxes.extract_first()
            yield Request(
                url=f"https:{firmware_page}",
                meta={"model_name": response.meta["model_name"]},
                callback=self.parse_firmware
            )
        else:
            self.logger.info(f"No firmware available for {response.meta['model_name']}")
            return

    def parse_firmware(self, response):
        FIRMWARE_LINK_SELECTOR = "//div[@class='onebtn']//a/@href"

        download_link = response.xpath(FIRMWARE_LINK_SELECTOR).extract_first()

        self.logger.info(f"Downloading firmware for {response.meta['model_name']}")
        parse_link(f"https:{download_link}", "tenda_br", response.meta["model_name"].strip())
