from pathlib import Path

import scrapy


class GenreSpider(scrapy.Spider):
    name = "genre"
    allowed_domains = ["www.everynoise.com"]
    start_urls = ["http://www.everynoise.com/"]

    def parse(self, response):
        
        Path("genres.html").write_bytes(response.body)