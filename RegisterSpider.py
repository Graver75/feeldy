from scrapy import Spider, FormRequest
from utils import get_email_by_uname, get_random_pass, get_random_uname
import json, random, logging

logger = logging.getLogger("register")
logger.setLevel(logging.INFO)

with open('config.json') as f:
    CONFIG = json.load(f)


class RegisterSpider(Spider):
    name = "register_feeldly_spider"
    page_url = CONFIG['urls']['reg_page']
    start_urls = [page_url]
    data = None

    def parse(self, response):
        register_url = response.xpath("//a/@href")[1].extract() # feedly link

        name = get_random_uname()
        self.data = {
            "name": name,
            "login": get_email_by_uname(name),
            "password": get_random_pass()
        }

        proxy = random.choice(CONFIG["proxy"])

        yield FormRequest(
            url=register_url,
            formdata=self.data,
            callback=self.after_register,

            meta={
                "proxy_info": proxy,
                "proxy": "http://%s:%s" % (proxy["ip"], proxy["port"])
            }
        )

    def after_register(self, response):
        if "Login successful" in response._cached_ubody :
            with open('users.json', 'r') as f:
                users = json.load(f)
                users.append(self.data)

            with open('users.json', 'w') as f:
                json.dump(users, f)
            logger.info("User " + self.data["name"] + " has been created.")
        else:
            logger.info("Error creating user " + self.data["name"] + ": " + str(response.status))
