# -*- coding: utf-8 -*-

import copy
import os

import scrapy
from yurasic_spider.items import SongItem

SONGS_DIRECTORY = 'songs'
TAGS_KEY = 'tags'


def create_fake_item():
    i = SongItem()
    i['url'] = 'url'
    i['title'] = 'title'
    i['content'] = 'tttt'
    i['author'] = 'author'
    i['tags'] = ''
    return i


class SongSpider(scrapy.Spider):
    name = 'yurasic_spider'
    start_urls = ['http://www.yurasic.ru']
    # start_urls = ['http://www.yurasic.ru/catalog/pesni-u-kostra']

    def __init__(self, **kwargs):
        super(SongSpider, self).__init__(**kwargs)
        self.models = ''

    def parse(self, response):
        if response.css('#page_title_song'):
            i = self.parse_song(response)
            yield i
            # TODO meditate here, please!
        else:
            for entry in response.xpath('//li/a'):
                r = self.parse_list_item(entry, response)
                if r:
                    yield r
        return

    def parse_list_item(self, entry, response):
        url_list = entry.xpath('@href').extract()
        if not url_list:
            return None
        url = url_list[0]

        entry_name_list = entry.css('.textDir::text').extract()
        if not entry_name_list:
            return None
        entry_name = entry_name_list[0]

        entry_name = entry_name.strip()
        entry_name = entry_name.split(' - ')
        entry_name = list(reversed(entry_name))

        entry_name = [s.strip() for s in entry_name]

        meta_modified = copy.deepcopy(response.meta)

        if TAGS_KEY not in meta_modified:
            meta_modified[TAGS_KEY] = []

        for s in entry_name:
            meta_modified[TAGS_KEY].append(s)

        return scrapy.Request(response.urljoin(url), self.parse, meta=meta_modified)

    def parse_song(self, response):
        song_content = []
        for sub_list in response.xpath('//*[@id="songStyle"]/pre/text()').extract():
            song_content += sub_list

        song_content = u''.join(song_content)

        song_title = ''
        if response.meta and response.meta[TAGS_KEY]:
            song_title = response.meta[TAGS_KEY][-1]

        # song_dir = response.meta[TAGS_KEY][:response.meta-1]
        # SongSpider.write_to_file(song_title, song_dir, song_content)

        i = SongItem()

        i['url'] = response.url
        i['title'] = song_title
        i['content'] = song_content
        i['author'] = ''
        if response.meta and response.meta[TAGS_KEY] and len(response.meta[TAGS_KEY]) > 1:
            i['author'] = response.meta[TAGS_KEY][-2]
        i['tags'] = response.meta[TAGS_KEY]

        return i

    @staticmethod
    def write_to_file(song_title, song_dir, song_content):
        song_dir.insert(0, SONGS_DIRECTORY)
        song_dir = os.path.join(*song_dir)
        os.makedirs(song_dir, exist_ok=True)

        song_path = os.path.join(song_dir, song_title + '.txt')
        with open(song_path, 'w') as f:
            f.write(song_content.encode('utf-8'))
