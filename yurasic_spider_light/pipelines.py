# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import logging

# sys.path += "main-package"

class YurasicSpiderPipeline(object):
    def process_item(self, item, spider):

        logging.info('models: ' + str(item.name))

        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass
