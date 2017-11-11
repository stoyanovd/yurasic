# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import django
import logging
from django import db


# sys.path += "main-package"

class YurasicSpiderToDbPipeline(object):
    def process_item(self, item, spider):
        logging.info('models: ' + str(item['title']))

        return item

    def open_spider(self, spider):
        from utils.import_models import get_models_from_yurasic_django
        spider.models = get_models_from_yurasic_django()

        h = spider.models.HierarchyItem(parent=None, name='root')
        h.save()
        spider.root_node.pointer_to_db = h

    def close_spider(self, spider):
        db.connections.close_all()
