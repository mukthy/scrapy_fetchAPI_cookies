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
