from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json, time
from LoginSpider import get_login_class
from scrapy.crawler import CrawlerProcess

with open('config.json') as f:
    CONFIG = json.load(f)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})


def login(response):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox()
    # driver = webdriver.Firefox(options=options, executable_path=r'/usr/local/bin/geckodriver')
    driver.get(response.url)
    time.sleep(5) # loading page and getting session cookie
    print(driver.get_cookies())
    return driver


process.crawl(get_login_class("mad_device@gravmail.com", "JzscyYVz", login))
process.start()
