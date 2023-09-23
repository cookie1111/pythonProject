# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
logger = logging.getLogger('FlatSpider')


import psycopg2

class PostgreSQLPipeline:
    def open_spider(self, spider):
        # Establish a connection to the PostgreSQL database
        self.connection = psycopg2.connect(
            host='db',
            user='root',
            password='pass',
            dbname='listings'
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        # Close the database connection
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        # Insert the item into the database
        for i in item['estates']:
            href = str.split(i['_links']['self']['href'], '/')[-1]
            logger.info(f"Inserting: {(href,i['name'], i['_links']['images'][0]['href'])}")

            self.cursor.execute("SELECT 1 FROM listings WHERE href = %s", (href,))
            exists = self.cursor.fetchone()


            if not exists:
                self.cursor.execute(
                    "INSERT INTO listings (href, title, image_url) VALUES (%s, %s, %s)",
                    (href, i['name'], i['_links']['images'][0]['href'])
                )
            else:
                logger.info(f"Listing already exists: {(href, i['name'], i['_links']['images'][0]['href'])}")

        self.connection.commit()
        return item
