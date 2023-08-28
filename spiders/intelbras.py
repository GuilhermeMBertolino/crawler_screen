import scrapy
from scrapy import Spider
from scrapy import Request
from time import sleep
import sys, os
import urllib.parse, urllib.request

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from browser_webdriver import driver, By, Ec, WebDriverWait
from download_firmware import parse_link
from vendor_links import INTELBRAS

class IntelbrasSpider(Spider):
    name = "intelbras-spider"
    start_urls = [INTELBRAS]

    def parse(self, response):
        driver.implicitly_wait(5)
        driver.get(response.url)
        driver.find_element(By.CLASS_NAME, "cc-dismiss").click()
        driver.find_element(By.XPATH, "//div[text()='Qual tipo de produto?']").click()
        driver.find_element(By.XPATH, "//div[text()='Redes']").click()
        driver.find_element(By.XPATH, "//div[text()='Qual categoria?']").click()
        driver.find_element(By.XPATH, "//div[text()='Roteadores']").click()
        # Wait for element to be clickable
        sleep(1)
        driver.find_element(By.XPATH, "//div[text()='Qual produto?']").click()
        print(driver.find_element(By.XPATH, "//div[contains(text(), 'WRN 300')]"))

    def parse_model(self, response):
        pass