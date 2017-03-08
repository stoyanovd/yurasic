import copy
import os

import scrapy
from yurasic_spider.items import SongItem

SONGS_DIRECTORY = 'songs'
TAGS_KEY = 'tags'


class SongSpider(scrapy.Spider):
    name = 'yurasic_spider'
    start_urls = ['http://www.yurasic.ru']

    def parse(self, response):
        if not response.css('#page_title_song'):
            # print('RESPONSE li a:', response.xpath('//li/a').extract())
            for entry in response.xpath('//li/a'):  # .extract():
                url_list = entry.xpath('@href').extract()
                if url_list:
                    url = url_list[0]
                else:
                    continue
                entry_name_list = entry.css('.textDir::text').extract()
                if entry_name_list:
                    entry_name = entry_name_list[0]
                else:
                    continue

                # print('-------------  ENTRY NAME ---------')
                # print(entry_name.encode('utf-8  '))
                entry_name = entry_name.strip().encode('utf-8')
                # print(url)
                # print(entry_name)

                entry_name = entry_name.split(' - ')
                entry_name = list(reversed(entry_name))

                entry_name = [s.strip() for s in entry_name]

                meta_modified = copy.deepcopy(response.meta)

                if TAGS_KEY not in meta_modified:
                    meta_modified[TAGS_KEY] = []

                for s in entry_name:
                    meta_modified[TAGS_KEY].append(s)

                # print('META', meta_modified)
                # for s in meta_modified[TAGS_KEY]:
                #     print(s)
                # print('__________')

                yield scrapy.Request(response.urljoin(url), self.parse, meta=meta_modified)
        else:
            # print('____get song inner', response.url)
            i = self.parse_song(response)
            yield i
            # yield scrapy.Request(response.url, self.parse_song)

    def parse_song(self, response):
        song_content = u''
        for content in response.xpath('//*[@id="songStyle"]/pre/text()').extract():
            song_content = content

        song_title = response.meta[TAGS_KEY][-1]

        # song_dir = response.meta[TAGS_KEY][:-1]
        # SongSpider.write_to_file(song_title, song_dir, song_content)

        i = SongItem()

        i['url'] = response.url
        i['title'] = song_title
        i['content'] = song_content
        if len(response.meta[TAGS_KEY]) > 1:
            i['author'] = response.meta[TAGS_KEY][-2]
        else:
            i['author'] = ''
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
