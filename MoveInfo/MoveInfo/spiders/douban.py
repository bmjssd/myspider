# -*- coding: utf-8 -*-
import scrapy
import json
import re


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}'
    offset = 0
    start_urls = [url.format(offset)]

    def parse(self, response):
        try:
            mv_list = json.loads(response.body)['data']
        except KeyError:
            print("问题url:{}".format(response.url))
            print(response.status)
            print(json.loads(response.body))
            return
        if not mv_list:
            print("没有内容:{}".format(response.url))
            exit()
        for li in mv_list:
            item = {}
            item["title"] = li['title']
            item["directors"] = li['directors']
            item["rate"] = li['rate']
            item['image_url'] = li['cover']

            yield scrapy.Request(
                li["url"],
                callback=self.detai,
                meta={'item': item}
            )
        self.offset += 20
        print("url:{}爬取完毕".format(response.url))
        yield scrapy.Request(
            self.url.format(self.offset),
            callback=self.parse,
        )
    def detai(self, response):
        item = response.meta['item']
        item['star'] = response.xpath("//span[text()='主演']/following::span[1]/a/text()").extract()
        item['country'] = response.xpath("//span[text()='制片国家/地区:']/following::text()[1]").extract_first().strip()
        item['release_date'] = response.xpath("//span[text()='上映日期:']/following::span[1]/text()").extract_first().strip()
        item['type'] = response.xpath("//span[text()='类型:']/following::span[@property='v:genre']/text()").extract()
        item['other_names'] = response.xpath("//span[text()='又名:']/following::text()[1]").extract_first().strip() if response.xpath("//span[text()='又名:']/following::text()[1]").extract_first() else ""
        if item['other_names'].count(" / ") > 0:
            item['other_names'] = item['other_names'].split(" / ")
        item['hot'] = re.findall(r'全部 (\d+?) 条', response.body.decode())[0] if re.findall(r'全部 (\d+?) 条', response.body.decode()) else None
        # print(response.request.headers['User-Agent'])
        yield item
