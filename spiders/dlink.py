import scrapy
from scrapy import Spider
from scrapy import Request
import sys, os
import urllib.parse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
                callback=self.parse_model
            )
    
    def parse_model(self, response):
        print("oioioioioi\n\n\n")
        LINK_SELECTOR = ".fileDownload::text"

        firmware = response.css(LINK_SELECTOR)
        yield {
            "firmware": firmware
        }