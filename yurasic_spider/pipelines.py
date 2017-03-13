# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import django
import logging
from django import db


# from songsapp import models


# sys.path += "main-package"

# from songsapp.models import Author, Song, Realization

class YurasicSpiderPipeline(object):
    def process_item(self, item, spider):

        author_name = item['author']
        models = spider.models
        logging.info('models: ' + str(models))
        author_candidates = models.Author.objects.filter(name=author_name)
        logging.info('models: ' + str(author_candidates))

        # raise Exception(os.linesep + os.linesep +
        #                 author_name + os.linesep +
        #                 str(author_candidates) +
        #                 os.linesep + os.linesep)

        if not author_candidates:
            author_object = models.Author(name=author_name)
            author_object.save()
        else:
            author_object = author_candidates[0]

        title = item['title']
        # song_object = models.Song(title=title, authors=[author_object])
        song_object = models.Song(title=title)
        song_object.save()
        song_object.authors.add(author_object)

        content = item['content']
        song_object.realization_set.create(
            content=content
        )
        # realization_object = models.Realization(content=content, song=song_object)
        # realization_object.save()
        # realization_object.song = song_object

        return item

    def open_spider(self, spider):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yurasic.settings")
        django.setup()
        spider.models = __import__('songsapp.models').models

    def close_spider(self, spider):
        db.connections.close_all()

        ############
        # Outdated

        # def insert_item(self, table_name, item):
        #     # print_item(item)
        #     keys = item.keys()
        #     data = [item[k] for k in keys]  # make a list of each key
        #     instr = 'INSERT INTO {table} ({keys}) VALUES ({placeholders});'.format(
        #         # Assemble query string
        #         table=table_name,  # table to insert into, provided as method's argument
        #         keys=", ".join(keys),  # iterate through keys, seperated by comma
        #         placeholders=", ".join("%s" for d in data)  # create a %s for each key
        #     )
        #     self.cur.execute(instr, data)  # Combine the instructions and data
        #     self.conn.commit()
        #     # log.msg("Successfully inserted \"%s - %s\" into database." % (
        #     #     item['artist'], item['songtitle']), level=log.DEBUG)
        #     #     print
        #     # "Successfully inserted \"%s: %s - %s\" into database table \"%s\"." % (
        #     # item['playid'], item['artist'], item['songtitle'], self.databaseTable)
        #
        #     self.inserts += 1


# not used, only for hints
def psql_startup():
    import os
    import psycopg2
    import urlparse

    # import urllib.parse

    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
