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
    'Cookie': 'bid=TW9FfFM6rLw; gr_user_id=29061151-bb6d-44cd-ad35-cfa8c44fad9e; ct=y; ps=y; ll="118172"; viewed="26274202_26838921_4826033_26468916_3112503_4889838_6789516_26320485"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1499574237%2C%22https%3A%2F%2Fwww.douban.com%2Faccounts%2Flogin%3Fredir%3Dhttps%253A%252F%252Fmovie.douban.com%252F%22%5D; _vwo_uuid_v2=49BFB964A55588402302EF90DE89BC30|1595871f7f79336105d5709a8b32edf3; _pk_id.100001.4cf6=4e34811c463e9043.1497948489.28.1499575920.1499570690.; _pk_ses.100001.4cf6=*; __utma=223695111.1940242653.1497948489.1499567326.1499574237.31; __utmb=223695111.0.10.1499574237; __utmc=223695111; __utmz=223695111.1499574237.31.22.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utmt=1; ue="1334968325@qq.com"; dbcl2="146515721:hbPy7u6w894"; ck=HKfg; ap=1; push_noty_num=0; push_doumail_num=0; __utma=30149280.637523572.1496852261.1499574237.1499574278.48; __utmb=30149280.21.10.1499574278; __utmc=30149280; __utmz=30149280.1499574278.48.33.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.14651',
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
        comment_time_list = e_html.xpath('//div[@id="comments"]/div[@class="comment-item"]/div[@class=]')


class DataBase(object):

    def __init__(self, host_name, port_num, user_name, password, db_name):
        self.host_name = host_name
        self.port_num = port_num
        self.user_name = user_name
        self.password = password
        self.db_name = db_name

    def open_db(self):
        global conn, cursor
        conn = pymysql.connect(host=self.host_name, port=self.port_num, user=self.user_name,password=self.password, db=self.db_name)
        cursor = conn.cursor()

    def get_data(self):
        pass

    def save_data(self):
        pass

    def close_db(self):
        cursor.close()
        conn.close()

