from scrapy import Spider, FormRequest
import json, random

with open('config.json') as f:
    CONFIG = json.load(f)


class LoginSpider(Spider):
    name = "login_feeldly_spider"
    page_url = CONFIG['urls']['log_page']
    start_urls = [page_url]

    def parse(self, response):
        login_url = response.xpath("//a/@href")[1].extract()  # feedly link
        CONFIG["urls"]["act_log_page"] = login_url
        with open('config.json', 'w') as f:
            json.dump(CONFIG, f)

    def after_login(self, response):
        pass