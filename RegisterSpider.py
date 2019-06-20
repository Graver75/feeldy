from scrapy import Spider, FormRequest
from utils import get_email_by_uname, get_random_pass, get_random_uname
import json


with open('config.json') as f:
    CONFIG = json.load(f)


class RegisterSpider(Spider):
    name = "register_feeldly_spider"
    page_url = CONFIG['urls']['page']
    start_urls = [page_url]

    def parse(self, response):
        register_url = response.xpath("//a/@href")[1].extract() # feedly link

        name = get_random_uname()
        data = {
            "name": name,
            "login": get_email_by_uname(name),
            "password": get_random_pass()
        }

        proxy = CONFIG["proxy"]
        yield FormRequest(
            url=register_url,
            formdata=data,
            callback=self.after_register(data),

            meta={
                "proxy_info": proxy,
                "proxy": "http://%s:%s" % (proxy["ip"], proxy["port"])
            }
        )

    def after_register(self, data):
        with open('users.json', 'r') as f:
            users = json.load(f)
            users.append(data)

        with open('users.json', 'w') as f:
            json.dump(users, f)

        return (
            lambda response: self.logger.info('Success.')
        )