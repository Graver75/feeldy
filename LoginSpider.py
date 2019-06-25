from scrapy import Spider, FormRequest, Request
import json, random

with open('config.json') as f:
    CONFIG = json.load(f)


def get_login_class(login, password, callback):
    class LoginSpider(Spider):
        name = "login_feeldly_spider"
        page_url = CONFIG['urls']['log_page']
        start_urls = [page_url]

        def parse(self, response):
            login_url = response.xpath("//a/@href")[1].extract()  # feedly link
            data = {
                "login": login,
                "password": password
            }

            proxy = random.choice(CONFIG["proxy"])
            yield FormRequest(
                url=login_url,
                formdata=data,
                callback=callback(data["login"]),

                meta={
                    "proxy_info": proxy,
                    "proxy": "http://%s:%s" % (proxy["ip"], proxy["port"])
                }
            )
    return LoginSpider