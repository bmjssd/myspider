# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

# class MoveinfoPipeline(object):
#     def process_item(self, item, spider):
#         print(item)
#         return item


class DoubanPipeline(object):
    def __init__(self):
        dbname = 'douban'
        sheetname = 'move'
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient()
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        self.post.insert(item)
        return item

