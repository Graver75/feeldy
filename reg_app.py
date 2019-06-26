from RegisterSpider import RegisterSpider
from scrapy.crawler import CrawlerProcess
import time, json, logging

with open('config.json') as f:
    TIMEOUT = json.load(f)["timeouts"]["register"]


def register(temp=None):
    logging.getLogger('scrapy').propagate = False
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    d = process.crawl(RegisterSpider)
    d.addCallback(after_register)
    d.addErrback(handle_exception)
    process.start(stop_after_crawl=False)
    process.stop()


def after_register(temp=None):
    time.sleep(TIMEOUT)
    register()


def handle_exception(f):
    pass


register()
