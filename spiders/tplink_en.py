import scrapy
from scrapy import Spider
from scrapy import Request
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from vendor_links import TPLINK_EN

class TPLink_enSpider(Spider):
    name = "tplink_en-spider"
    start_urls = [urllib.parse.urljoin(TPLINK_EN, "/hk/support/download")]

    def parse(self, response):
        ROUTER_WIFI_SELECTOR = "[data-class='wi-fi-routers']"
        ROUTER_5G_SELECTOR = "[data-class='c-3g-4g-routers']"
        MODEL_SELECTOR = ".ga-click"

        routers_1 = response.css(ROUTER_WIFI_SELECTOR)
        routers_2 = response.css(ROUTER_5G_SELECTOR)

        models = routers_1.css(MODEL_SELECTOR) + (routers_2.css(MODEL_SELECTOR))

        for model in models:
            page_link = model.attrib["href"]
            model_name = model.css("::text").get()
            yield Request(
                url=urllib.parse.urljoin(TPLINK_EN, page_link),
                meta={"model_name": model_name},
                callback=self.parse_model
            )

    def parse_model(self, response):
        FIRMWARE_CONTAINER_SELECTOR = "#content_Firmware"
        DOWNLOAD_LINK_SELECTOR1 = ".tp-dialog-btn"
        DOWNLOAD_LINK_SELECTOR2 = ".download-resource-btn"

        firmware_container = response.css(FIRMWARE_CONTAINER_SELECTOR)

        if(not firmware_container):
            print("No firmware available")
            return
        
        if(firmware_container.css(DOWNLOAD_LINK_SELECTOR1)):
            download_link = firmware_container.css(DOWNLOAD_LINK_SELECTOR1)[0].attrib["href"].replace(" ", "%20")
        else:
            download_link = firmware_container.css(DOWNLOAD_LINK_SELECTOR2)[0].attrib["href"].replace(" ", "%20")

        urllib.request.urlretrieve(download_link, f"{response.meta['model_name']}.zip")