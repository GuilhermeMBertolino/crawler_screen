import scrapy
from scrapy import Spider
from scrapy import Request
from time import sleep
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from browser_webdriver import driver, By
from download_firmware import parse_link
from vendor_links import INTELBRAS

class IntelbrasSpider(Spider):
    name = "intelbras-spider"
    start_urls = [INTELBRAS]

    def parse(self, response):
        driver.get(response.url)
        driver.find_element(By.CLASS_NAME, "cc-dismiss").click()
        driver.find_element(By.XPATH, "//div[text()='Qual tipo de produto?']").click()
        driver.find_element(By.XPATH, "//div[text()='Redes']").click()
        driver.find_element(By.XPATH, "//div[text()='Qual categoria?']").click()
        driver.find_element(By.XPATH, "//div[text()='Roteadores']").click()
        # Wait for element to be clickable
        sleep(5)
        driver.find_element(By.XPATH, "//div[text()='Qual produto?']").click()
        routers = driver.find_element(By.CLASS_NAME, "css-11unzgr").find_elements(By.XPATH, "*")
        routers[0].click()
        # for router in routers:
        #     print(router.text)

    def parse_model(self, response):
        pass