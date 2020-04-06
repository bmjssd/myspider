import requests
from fake_useragent import UserAgent
from lxml import etree
import redis


class GetIP(object):
    def __init__(self):
        self.useragent = UserAgent()
        dbname = 'douban'
        sheetname = 'ip'
        # 创建MONGODB数据库链接
        client = pymongo.MongoClient()
        # 指定数据库
        mydb = client[dbname]
        # 存放数据的数据库表名
        self.post = mydb[sheetname]

    def geturl(self):
        headers = {"User-Agent": self.useragent.random}
        response = requests.get(url="https://www.kuaidaili.com/free/inha/", headers=headers)
        if response.status_code != 200:
            print(type(response.status_code))
            return None
        response = response.content.decode()
        html = etree.HTML(response)
        return html

    def parse(self, html):
        if html is None:
            return print("html失败")
        list_ip = html.xpath("//table[@class='table table-bordered table-striped']/tbody/tr")
        print(list_ip)
        print(len(list_ip))
        for li in list_ip:
            ip = li.xpath("./td[1]/text()")[0]
            ip_port = li.xpath("./td[2]/text()")[0]
            data = "{}:{}".format(ip, ip_port)
            self.post.

    def workon(self):
        # 发送url请求
        html = self.geturl()
        # 获取数据
        self.parse(html)
        # 保存redis



if __name__ == '__main__':
    spider = GetIP()
    spider.workon()