# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2, psycopg2.extras, logging
import wpmaintenance

logger = logging.getLogger('sqlpipeline')

class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        if type(item) is wpmaintenance.items.WpmaintenanceItem:
            item.setdefault('industry', '')
            item.setdefault('zipcode', '')
            item.setdefault('url', '')
            item.setdefault('found_by_check', '')
        return item

class SqlPipeline(object):
    collection_name = 'wpmaintenance'
    
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            #uri=crawler.settings.get('MONGO_URI'),
            host='westroppfamily.com',
            database='misc_stuff',
            user='datauser',
            password='Hk8o5Qd',
            port='38774'
            #104.154.18.26
        )

    def open_spider(self, spider):
        self.conn = psycopg2.connect(host=self.host,database=self.database, user=self.user, password=self.password, port=self.port)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def process_item(self, item, spider):
        #logger.info('PROCESSING ITEM')
        sql = """INSERT INTO wpmaintenance(
                    url, industry, zipcode, 
                    found_by_check
                ) VALUES(
                    %s, %s, %s, 
                    %s
                ) returning url;"""
        try:
            if item.get('url', 'not set') == 'not set':
                #logger.info('SKIPPING ITEM')
                return
            else:
                logger.info('SAVING ITEM')
                self.cursor.execute(sql, (
                    item['url'], item['industry'], item['zipcode'], 
                    item['found_by_check'], ))
                url = self.cursor.fetchone()[0]
        except psycopg2.IntegrityError as error:
            self.conn.rollback()
            logger.info('SAVE FAILED: %s', item['url'])
        except (Exception, psycopg2.DatabaseError) as error:
            self.conn.rollback()
            logger.error('psycopg2 ERROR: %s', error)
            logger.error('OBJECT: %s', item)
        else:
            self.conn.commit()
        return item
