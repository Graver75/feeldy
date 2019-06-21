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
    # driver = webdriver.Firefox(options=options, executable_path=r'/usr/local/bin/geckodriver') #headless version, disabled while developing
    driver.get(response.url)
    time.sleep(10) # loading page and getting session cookie
    follow(driver)


def follow(driver):
    urls_to_follow = CONFIG['urls']['follow']
    for elem in urls_to_follow:
        driver.get(elem["value"])
        time.sleep(10)
        feeds = driver.find_elements_by_css_selector('.DiscoverFeed')
        for feed in feeds:
            if feed.find_element_by_css_selector('.item-header').text == elem['title']:
                button = feed.find_element_by_css_selector('.follow')
                button.click()

                input = driver.find_elements_by_css_selector('.fx-input')[1].find_element_by_tag_name('input')
                input.send_keys(elem['title'])

                send_div = driver.find_element_by_css_selector('.menu-footer')
                send_div.click()

                menu = driver.find_elements_by_css_selector('.menu')[1]
                create_div = menu.find_element_by_css_selector('.primary')
                create_div.click()


def follow_topics(username, password):
    process.crawl(get_login_class(username, password, login))
    process.start()

#follow_topics("mad_device@gravmail.com", "JzscyYVz")