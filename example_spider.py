from scrapy import Spider, FormRequest


class RegisterSpider(Spider):
    name = 'loging-spider'
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        # extract the CSRF token (selector depending on context)
        token = response.css("input[name='csrf_token']::attr(value)").extract_first()
        # create a python dict with form values
        data = {
            'csrf_token': token,
            'username': 'whatever',
            'password': 'whatever',
        }
        # submit a POST request to web (url may differ from login page)
        yield FormRequest(url=self.login_url, formdata=data, callback=self.parse_quotes)

    def parse_quotes(self, response):
        """Parse the main page after the spider logged in"""
        for q in response.css('div.quote'):
            yield {
                'author_name': q.css('small.author::text').extract_first(),
                'author_url': q.css('small.author ~ a[href*="goodreads.com"]::attr(href)').extract_first()
            }