# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import shutil
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class MangaCollecterPipeline(object):
    def process_item(self, item, spider):
        return item


class MangaCollectorPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if 'img_url' in item:
            yield scrapy.Request(item['img_url'])
        if 'image_urls' in item:
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if 'chapter' not in item:
            chapter = item['chapter']
            chapter_name = '%03d-%s/' % (chapter['chapter_no'], chapter['title'])
            page_name = '%03dp.jpg' % item['page_no']
            image_dir = os.path.join(chapter['store_dir'], chapter['book'],
                                     chapter['version'], chapter_name)

            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            out_image_paths = []
            for img_path in image_paths:
                out_img_path = os.path.join(image_dir, page_name)
                shutil.copy(img_path, out_img_path)
                out_image_paths.append(out_img_path)
            image_paths = out_image_paths

        return {
            'image_paths': image_paths
        }
