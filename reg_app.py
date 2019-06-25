from RegisterSpider import RegisterSpider
from scrapy.crawler import CrawlerProcess
import time, json, logging

with open('config.json') as f:
    TIMEOUT = json.load(f)["register_timeout"]



def register(temp=None):
    logging.getLogger('scrapy').propagate = False
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    d = process.crawl(RegisterSpider)
    d.addCallback(after_register)
    process.start(stop_after_crawl=False)


def after_register(temp=None):
    time.sleep(TIMEOUT)
    register()

register()