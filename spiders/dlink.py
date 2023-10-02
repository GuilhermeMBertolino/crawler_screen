import scrapy
from scrapy import Spider
from scrapy import Request
from time import sleep
import sys, os
import urllib.parse
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from browser_webdriver import driver, By, Ec, WebDriverWait
from download_firmware import parse_link
from vendor_links import DLINK

class DlinkSpider(Spider):
    name = "dlink-spider"
    start_urls = [urllib.parse.urljoin(DLINK, "/AllPro.aspx")]

    def parse(self, response):
        LINE_SELECTOR = "table tr"
        MODEL_SELECTOR = ".aRedirect::text"
        lines = response.css(LINE_SELECTOR)

        for line in lines:
            model = line.css(MODEL_SELECTOR).extract_first()
            yield Request(
                url=urllib.parse.urljoin(DLINK, f"/ProductInfo.aspx?m={model}"),
                meta={"model_name": model},
                callback=self.parse_model
            )
    
    def parse_model(self, response):
        LINK_REGEX_PATTERN = r"https://.*?Firmware.*?\.(bin|zip|rar)"

        driver.get(response.url)
        download_link = re.search(LINK_REGEX_PATTERN, driver.page_source, re.IGNORECASE)

        if download_link:
            parse_link(download_link.group(), "dlink", response.meta["model_name"])

