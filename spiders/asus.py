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
        MODEL_SELECTOR = ".//h2/text()"
        MODEL_PAGE_SELECTOR = ".//div[contains(@class, 'buttonBuy')]/a/@href"

        routers = response.xpath(ROUTER_SELECTOR)
        
        self.logger.info(f"Start crawling {len(routers)} pages")

        for router in routers:
            model = router.xpath(MODEL_SELECTOR).extract_first().replace(" ", "-")
            model_page = router.xpath(MODEL_PAGE_SELECTOR).extract_first()
            yield Request(
                url=urllib.parse.urljoin(model_page, f"helpdesk_bios/?model2Name={model}"),
                meta={"model_name": model},
                callback=self.parse_model
            )

    def parse_model(self, response):
        DOWNLOAD_BOX_SELECTOR = "//div[@class='overHidden']"
        DOWNLOAD_LINK_SELECTOR = ".//a/@href"
        
        download_box = response.xpath(DOWNLOAD_BOX_SELECTOR)

        if not download_box:
            self.logger.info(f"No firmware available for {response.meta['model_name']}")
            return
        
        self.logger.info(f"Downloading firmware for {response.meta['model_name']}")
        
        download_link = download_box[0].xpath(DOWNLOAD_LINK_SELECTOR).extract_first()
        print(download_link)
        parse_link(download_link, "asus", response.meta["model_name"])