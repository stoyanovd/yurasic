# -*- coding: utf-8 -*-

import copy
import os
import yaml

import scrapy
from yurasic_spider_light.items import SongItem

SONGS_DIRECTORY = 'songs_download'
TAGS_KEY = 'tags'
HIERARCHY_KEY = 'hierarchy'


class Node:
    def __init__(self, url, name, children, parent):
        self.url = url
        self.name = name
        self.children = children
        self.parent = parent


class SongSpider(scrapy.Spider):
    name = 'yurasic_spider_light'
    start_urls = ['http://www.yurasic.ru']
    # start_urls = ['http://www.yurasic.ru/catalog/pesni-u-kostra']

    def __init__(self, **kwargs):
        super(SongSpider, self).__init__(**kwargs)
        self.root_node = Node(self.start_urls[0], 'root', [], None)
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
            n = Node(url, entry_name, [], self.root_node)
            self.hierarchy[n.url] = n

            self.root_node.children.append(n)
        else:
            parent = meta_modified[HIERARCHY_KEY]
            assert isinstance(parent, Node)

            n = Node(url=response.url, name=entry_name, children=[], parent=parent)
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
        song_title = u''.join(song_content)

        assert HIERARCHY_KEY in response.meta
        parent = response.meta[HIERARCHY_KEY]
        assert isinstance(parent, Node)

        n = Node(url=response.url, name=song_title, children=[], parent=parent)
        self.hierarchy[n.url] = n

        parent.children.append(n)

        i = SongItem()

        i['url'] = response.url
        i['title'] = song_title
        i['content'] = song_content
        i['author'] = '-empty-author-'
        i['tags'] = '-empty-tags-'

        self.write_to_file(i, response.meta[HIERARCHY_KEY])

        return i

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

