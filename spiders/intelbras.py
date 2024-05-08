import scrapy
from scrapy import Spider
from scrapy import Request
from time import sleep
import sys, os
import urllib.parse, urllib.request
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from download_firmware import parse_link
from vendor_links import INTELBRAS

def get_base_url(url):
    parsed_url = urllib.parse.urlparse(url)
    base_url = parsed_url._replace(path='/'.join(parsed_url.path.split('/')[:-1]))
    return f"{urllib.parse.urlunparse(base_url)}/"

class IntelbrasSpider(Spider):
    name = "intelbras-spider"
    start_urls = ["https://manual-bifrost.intelbras.com.br/index_ChangLogs.html",
                  "https://manuais.intelbras.com.br/manual-linha-rx/index_ChangeLogs.html",
                  ]

    def parse(self, response):
        CONTAINER_SELECTOR = "//div[contains(@class, 'menuManual')]"
        LINK_SELECTOR = ".//a/@href"
        MODEL_SELECTOR = ".//p[@class='titleOptionMenuManual']/text()"

        container = response.xpath(CONTAINER_SELECTOR)

        if container:
            urls = container.xpath(LINK_SELECTOR)
            models = container.xpath(MODEL_SELECTOR)
            self.logger.info(f"Start crawling {len(models)} pages")

            for url, model in zip(urls, models):
                model_code = model.extract().split(" ")[-1]
                yield Request(
                    url=urllib.parse.urljoin(get_base_url(response.url), url.extract()),
                    meta={"model_name": model_code},
                    callback=self.parse_model
                )


    def parse_model(self, response):
        LINK_SELECTOR = "//img[@id='download-box']/../@href"

        download_link = response.xpath(LINK_SELECTOR)

        if not download_link:
            self.logger.info(f"No firmware available for {response.meta['model_name']}")
            with open("intelbras.txt", "a") as f:
                f.write(f"{response.meta['model_name']} - No firmware\n")
            return
        
        self.logger.info(f"Downloading firmware for {response.meta['model_name']}")
        url = urllib.parse.urljoin(get_base_url(response.url), download_link.extract_first())
        with open("intelbras.txt", "a") as f:
            f.write(f"{response.meta['model_name']} - {url}\n")