import scrapy
import datetime
import time
import json
import logging  # Step 1: Import the logging module

class FlatSpider(scrapy.Spider):
    name = "flats"
    max_page = 25

    # Step 2: Create a logger instance
    logger = logging.getLogger('FlatSpider')

    def get_cur_timestamp(self):
        return int(time.mktime(datetime.datetime.now().timetuple())*1000)

    @property
    def start_urls(self):
        self.timestamp = self.get_cur_timestamp()
        url = f"https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=20&tms={self.timestamp}"
        return [url]

    def create_request_url(self, page_number):
        return f'https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_type_cb=1&page={page_number}&per_page=20&tms={self.timestamp}'

    def parse(self, response):
        # self.logger.info("Response text: %s", response.text)
        for result in self.parse_listings_page1(response):
            yield result

    def parse_listings_page1(self, response):
        """
        here parse first page, schedule all other pages at once!
        """
        total_pages = 25

        self.logger.info(f"HELLO WORLD")
        # schedule every page at once!
        for page in range(2, total_pages + 1):
            next_page_url = self.create_request_url(page)
            yield scrapy.Request(next_page_url, callback=self.parse_estate)
        # don't forget to also parse listings on first page!
        yield from self.parse_estate(response)

    def parse_estate(self, response):
        data = json.loads(response.text)
        estates = data['_embedded']['estates']

        # Step 3: Use the logger instance to log the scraped data
        self.logger.info(f"Scraped data: {len(estates)}")

        yield {'estates': estates}
