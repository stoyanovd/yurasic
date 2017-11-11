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

        # author_name = item['author']
        # models = spider.models
        # logging.info('models: ' + str(models))
        # author_candidates = models.Author.objects.filter(name=author_name)
        # logging.info('models: ' + str(author_candidates))
        #
        # # raise Exception(os.linesep + os.linesep +
        # #                 author_name + os.linesep +
        # #                 str(author_candidates) +
        # #                 os.linesep + os.linesep)
        #
        # if not author_candidates:
        #     author_object = models.Author(name=author_name)
        #     author_object.save()
        # else:
        #     author_object = author_candidates[0]
        #
        # title = item['title']
        # # song_object = models.Song(title=title, authors=[author_object])
        # song_object = models.Song(title=title)
        # song_object.save()
        # song_object.authors.add(author_object)
        #
        # content = item['content']
        # song_object.realization_set.create(
        #     content=content
        # )


        # realization_object = models.Realization(content=content, song=song_object)
        # realization_object.save()
        # realization_object.song = song_object

        return item

    def open_spider(self, spider):
        pass
        # spider.models = get_models_from_yurasic_django()

    def close_spider(self, spider):
        pass
        # db.connections.close_all()
