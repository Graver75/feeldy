from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json, time
from LoginSpider import get_login_class
from scrapy.crawler import CrawlerProcess

with open('config.json') as f:
    CONFIG = json.load(f)

with open('users.json') as f:
    users = json.load(f)

def login(response):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox()
    # driver = webdriver.Firefox(options=options, executable_path=r'/usr/local/bin/geckodriver') #headless version, disabled while developing
    driver.get(response.url)
    time.sleep(3) # loading page and getting session cookie
    follow(driver)


def follow(driver):
    urls_to_follow = CONFIG['urls']['follow']
    for elem in urls_to_follow:
        driver.get(elem["value"])
        time.sleep(9)
        feeds = driver.find_elements_by_css_selector('.DiscoverFeed')
        for feed in feeds:
            if feed.find_element_by_css_selector('.item-header').text == elem['title']:
                button = feed.find_element_by_css_selector('.follow')
                button.click()
                time.sleep(4)

                send_div = driver.find_element_by_css_selector('.menu-footer')
                send_div.click()
                time.sleep(4)

                input = driver.find_elements_by_css_selector('.fx-input')[1].find_element_by_tag_name('input')
                input.send_keys(elem['title'])
                time.sleep(4)

                menu = driver.find_elements_by_css_selector('.menu')[1]
                create_div = menu.find_element_by_css_selector('.primary')
                create_div.click()
                time.sleep(4)
    driver.close()


def follow_topics(username, password):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    d = process.crawl(get_login_class(username, password, login))
    d.addCallback(mass_follow)
    process.start(stop_after_crawl=False)


def mass_follow(a):
    for i, user in enumerate(users):
        del users[i]
        follow_topics(user['login'], user['password'])

mass_follow(None)