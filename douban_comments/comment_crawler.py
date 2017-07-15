"""
爬取评论，要抓取以下几点内容．
评论人的id以及个人主页链接，打分，打分时间，评论内容，赞同数．
"""

import time
import random
import requests
import pymysql
from lxml import etree


page_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/subject/26411410/',
    'Cookie': '',  # 设置自己的Cookie, 也可以用模拟登陆，然后保存Cookie .
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}


# 设置ip pool
def proxypool(num):
    n = 1
    # os.chdir(r'/Users/apple888/PycharmProjects/proxy IP')
    fp = open('/home/fine-day/PycharmProjects/douban_comments/proxy_v3.txt', 'r')
    proxys = list()
    ips = fp.readlines()
    while n < num:
        for p in ips:
            ip = p.strip('\n').split('\t')
            proxy = 'http:\\' + ip[0] + ':' + ip[1]
            proxies = {'proxy': proxy}
            proxys.append(proxies)
            n+=1
    return proxys

pro_ip = proxypool(1500)


class CommentCrawler(object):

    def __init__(self, page_url):
        self.page_url = page_url

    def download_page(self, url):
        try:
            rsp = requests.get(url=url, headers=page_headers, proxies= random.choice(pro_ip))
            rsp_code = rsp.status_code
            # 请求响应的状态码
            while rsp_code != 200:
                rsp = requests.get(url=url, headers=page_headers, proxies=random.choice(pro_ip))
            rsp_content = rsp.content
            return rsp_content

        except Exception as e:
            print(e)
            return url

    def parse_html(self, html):
        e_html = etree.HTML(html)
        comment_list = e_html.xpath('//div[@id="comments"]/div[@class="comment-item"]/div[@class="comment"]/p/text()')
        star_list = e_html.xpath('//div[@id="comments"]/div[@class="comment-item"]/div[@class="comment"]/h3'
                                 '/span[@class="comment-info"]/span[@class="rating"]/@title')
        comment_time_list = e_html.xpath('//div[@id="comments"]/div[@class="comment-item"]/div[@class="comment"]'
                                         '/h3/span[@class="comment-info"]/span[@class="comment-time"]/@title')
        id_list = e_html.xpath('//div[@id="comments"]/div[@class="comment-item"]/div[@class="comment"]/h3'
                               '/span[@class="comment-info"]/a/text()')
        id_url_list = e_html.xpath('////div[@id="comments"]/div[@class="comment-item"]/div[@class="comment"]/h3'
                                   '/span[@class="comment-info"]/a/@href')
        vote_num_list = e_html.xpath('////div[@id="comments"]/div[@class="comment-item"]/div[@class="comment"]/h3'
                                     '/span[@class="comment-vote"]/span[@class="votes"]/text()')


class DataBase(object):

    def __init__(self, host_name, port_num, user_name, password, db_name, charset):
        self.host_name = host_name
        self.port_num = port_num
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.charset = charset

    def open_db(self):
        global conn, cursor
        conn = pymysql.connect(host=self.host_name, port=self.port_num, user=self.user_name,password=self.password,
                               db=self.db_name, charset=self.charset)

        cursor = conn.cursor()

    def get_data(self):
        get_data_sql = """ SELECT id, page_url  FROM comment_url """
        cursor.excute(get_data_sql)
        for r in cursor:



    def save_data(self):
        pass

    def close_db(self):
        cursor.close()
        conn.close()


if __name__ == '__main__':
    page_url =
    comment_crawler = CommentCrawler(page_url)



