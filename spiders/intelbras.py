import scrapy
from scrapy import Spider
from scrapy import Request
from time import sleep
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import INTELBRAS

def get_base_url(url):
    parsed_url = urllib.parse.urlparse(url)
    base_url = urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))
    return urllib.parse.urljoin(base_url, "/")

class IntelbrasSpider(Spider):
    name = "intelbras-spider"
    start_urls = ["https://manual-bifrost.intelbras.com.br/index_ChangLogs.html",
                  "https://manuais.intelbras.com.br/manual-linha-rx/index_ChangeLogs.html"]

    def parse(self, response):
        CONTAINER_SELECTOR = "//div[@class='menuManual']"
        LINK_SELECTOR = ".//a/@href"
        MODEL_SELECTOR = ".//p[@class='titleOptionMenuManual']/text()"

        container = response.xpath(CONTAINER_SELECTOR).extract_first()

        if container:
            urls = response.xpath(LINK_SELECTOR)
            models = response.xpath(MODEL_SELECTOR)
            self.logger.info(f"Start crawling {len(models)} pages")

            for url, model in zip(urls, models):
                model_code = model.extract().split(" ")[-1]
                yield Request(
                    url=urllib.parse.urljoin(get_base_url(response.url), url.extract()),
                    meta={"model_name": model_code},
                    callback=self.parse_model
                )


    def parse_model(self, response):
        pass