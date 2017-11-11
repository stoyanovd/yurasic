# -*- coding: utf-8 -*-

import copy
import os

import logging
import yaml

import scrapy
from yurasic_spider_light.items import SongItem

SONGS_DIRECTORY = 'songs_download'
TAGS_KEY = 'tags'
HIERARCHY_KEY = 'hierarchy'


class Node:
    def __init__(self, url, name, children, parent, models):
        self.url = url
        self.name = name
        self.children = children
        self.parent = parent
        if self.parent:
            self.pointer_to_db = models.HierarchyItem(parent=self.parent.pointer_to_db, name=self.name)
            self.pointer_to_db.save()
        else:
            self.pointer_to_db = None


class SongSpider(scrapy.Spider):
    name = 'yurasic_spider_to_db'
    # start_urls = ['http://www.yurasic.ru']
    start_urls = ['http://www.yurasic.ru/catalog/pesni-u-kostra']

    def __init__(self, **kwargs):
        super(SongSpider, self).__init__(**kwargs)
        self.models = ''
        self.root_node = Node(self.start_urls[0], 'root', [], None, self.models)

        # url -> Node
        self.hierarchy = {self.root_node.url: self.root_node}

        self.storage = dict()

    def parse(self, response):
        if response.css('#page_title_song'):
            i = self.parse_song(response)
            yield i
            # TODO meditate here, please!
            # it is important that there is 'yield'!
        else:
            for entry in response.xpath('//li/a'):
                r = self.parse_list_item(entry, response)
                if r:
                    yield r
        return

    def parse_list_item(self, entry, response):
        url_list = entry.xpath('@href').extract()
        assert url_list
        url = url_list[0]

        entry_name_list = entry.css('.textDir::text').extract()
        assert entry_name_list
        entry_name = entry_name_list[0]
        entry_name = entry_name.strip()

        meta_modified = copy.deepcopy(response.meta)

        if HIERARCHY_KEY not in meta_modified:
            n = Node(url, entry_name, [], self.root_node, self.models)
            self.hierarchy[n.url] = n

            self.root_node.children.append(n)
        else:
            parent = meta_modified[HIERARCHY_KEY]
            assert isinstance(parent, Node)

            n = Node(url=response.url, name=entry_name, children=[], parent=parent,
                     models=self.models)
            self.hierarchy[n.url] = n

            parent.children.append(n)

        meta_modified[HIERARCHY_KEY] = n

        return scrapy.Request(response.urljoin(url), self.parse, meta=meta_modified)

    def parse_song(self, response):
        song_content = []
        for sub_list in response.xpath('//*[@id="songStyle"]/pre/text()').extract():
            song_content += sub_list
        song_content = u''.join(song_content)

        song_title = []
        for sub_list in response.xpath('//*[@id="page_title_song"]/h1/text()').extract():
            song_title += sub_list
        song_title = u''.join(song_title)

        assert HIERARCHY_KEY in response.meta
        parent = response.meta[HIERARCHY_KEY]
        assert isinstance(parent, Node)

        n = Node(url=response.url, name=song_title, children=[], parent=parent,
                 models=self.models)

        self.hierarchy[n.url] = n

        parent.children.append(n)

        song_item = SongItem()

        song_item['url'] = response.url
        song_item['title'] = song_title
        song_item['content'] = song_content
        song_item['author'] = '-empty-author-'
        song_item['tags'] = '-empty-tags-'

        self.insert_song_to_db(n, song_item)

        # self.write_to_file(i, response.meta[HIERARCHY_KEY])

        return song_item

    def write_to_file(self, song, node):
        if not node in self.storage:
            hierarchy_path = []
            temp_node = node
            while temp_node is not None:
                hierarchy_path += [temp_node.name]
                temp_node = temp_node.parent

            song_dir = os.path.join(SONGS_DIRECTORY, *reversed(hierarchy_path))
            os.makedirs(song_dir, exist_ok=True)
            self.storage[node] = song_dir

        song_dir = self.storage[node]

        song_text_path = os.path.join(song_dir, 'text.txt')
        with open(song_text_path, 'wb') as f:
            f.write(song['content'].encode('utf-8'))

        song_path = os.path.join(song_dir, 'song.yaml')
        yaml.dump(dict(song), open(song_path, 'w'), allow_unicode=True)

    def insert_song_to_db(self, node, song_item):

        models = self.models
        logging.info('models: ' + str(models))
        # from songsapp import models

        # author_candidates = models.Author.objects.filter(name=author_name)
        # logging.info('models: ' + str(author_candidates))

        # raise Exception(os.linesep + os.linesep +
        #                 author_name + os.linesep +
        #                 str(author_candidates) +
        #                 os.linesep + os.linesep)

        # if not author_candidates:
        #     author_object = models.Author(name=author_name)
        #     author_object.save()
        # else:
        #     author_object = author_candidates[0]

        title = song_item['title']
        assert len(title) < 200
        # song_object = models.Song(title=title, authors=[author_object])
        song_object = models.Song(title=title, node=node.pointer_to_db)
        song_object.save()
        # song_object.authors.add(author_object)

        content = song_item['content']
        song_object.realization_set.create(
            content=content
        )

        pass
