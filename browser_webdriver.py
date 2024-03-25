from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

opt = webdriver.FirefoxOptions()
opt.add_argument("-headless")
opt.log.level = "error"

driver = webdriver.Firefox(options=opt)
driver.implicitly_wait(5)