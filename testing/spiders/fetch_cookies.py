import scrapy
from scrapy.http import JsonRequest


class ScrapyFetchApiSpider(scrapy.Spider):
    name = "scrapy_fetch_api"
    allowed_domains = ["httpbin.org"]
    start_urls = ["https://httpbin.org"]

    def start_requests(self):
        for url in self.start_urls:
            headers = {"Content-Type": "application/json"}
            yield scrapy.Request(
                url=url,
                meta={
                    "crawlera_fetch": {
                        "args": {
                            "script": "",
                            "screenshot": False,
                            "render": False,
                            "parameters": {"debug": True,},
                        }
                    }
                },
                headers=headers,
                callback=self.cookies,
            )

    def cookies(self, response):
        # this below Cookie works when you want to use the requests module.
        # cookie = response.meta['crawlera_fetch']['upstream_response']['body']['custom_data']['cookies']['cookies']
        # r = json.dumps(cookie[0])
        # with open('resoponse.txt', 'w') as file:
        #     file.write(str(r))

        # API_URL = "http://fetch.crawlera.com:8010/fetch/v2/"
        # API_KEY = "API-KEY"
        # response = requests.post(API_URL, auth=(API_KEY, ''), json={
        #     "url": "https://httpbin.org/ip",
        #     #  "render" : False,
        #     "script": "",
        #     "parameters": {
        #         #   "debug": True,
        #         "cookies": cookie}})
        # print(response.text)

        # The below part of the snipit will work if you want to make the request to site with Scrapy JsonRequest.
        data = response.meta["crawlera_fetch"]["upstream_response"]["body"][
            "custom_data"
        ]["cookies"]["cookies"]
        print(data)
        with open("cookies.txt", "w") as file:
            file.write(str(data))
        yield scrapy.Request(
            url="https://httpbin.org/ip",
            meta={
                "crawlera_fetch": {
                    "args": {
                        "script": "",
                        "screenshot": False,
                        "render": False,
                        "parameters": {"cookies": data},
                    }
                }
            },
            callback=self.parse,
        )

    def parse(self, response):
        result = response.text
        # saving the response file as HTML.
        with open("resoponse.html", "w") as file:
            file.write(result)
        print(result)
