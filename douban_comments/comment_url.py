"""
  此部分代码，是用来获取所有评论页面的url.url,有规律可循，其实可以根据信息生成，但是此部还是解析页面获取next_page
  中的href再拼接而成．所得到的page_url_list是实际所有评论页面的url.
"""


import time
import datetime
import random
import requests
from lxml import etree
import pymysql
import codecs

page_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'movie.douban.com',
    'Referer': 'https://movie.douban.com/subject/26411410/',
    'Cookie': '', # 此处用自己的Cookie , 也可以模拟登陆后保存Cookie的方式。
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}
# u-a list
u_a_list = [
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    '​Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.96 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    # 'Googlebot-Image/1.0',
    # 'Googlebot-Video/1.0',
    # 'Mediapartners-Google',
    # 'AdsBot-Google-Mobile-Apps'
]

# cookie_list
cookie_list = [
    'bid=TW9FfFM6rLw; gr_user_id=29061151-bb6d-44cd-ad35-cfa8c44fad9e; ct=y; ps=y; ll="118172"; viewed="26274202_26838921_4826033_26468916_3112503_4889838_6789516_26320485"; ue="1334968325@qq.com"; _vwo_uuid_v2=49BFB964A55588402302EF90DE89BC30|1595871f7f79336105d5709a8b32edf3; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1499574278%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dkvdmirs22OQAj10KSbGstQqMKXoquaLus76T94c1ss3%26wd%3D%26eqid%3De253b57901020fa9000000025961a215%22%5D; __utmt=1; ap=1; dbcl2="163539032:KqcOMIK+2ZU"; ck=QcXf; _pk_id.100001.8cb4=a278823aa2b4b9d9.1493947655.26.1499574533.1499571496.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utma=30149280.637523572.1496852261.1499574237.1499574278.48; __utmb=30149280.5.10.1499574278; __utmc=30149280; __utmz=30149280.1499574278.48.33.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16353'
]
basic_url = 'https://movie.douban.com/subject/26411410/comments'
start_page_url = 'https://movie.douban.com/subject/26411410/comments?start=54124&limit=20&sort=new_score&status=P'


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

# 连接数据库
conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='douban_movie', charset='utf8')
cursor = conn.cursor()


# 设计下载next_page_url的类
class DownloadNextPageUrl(object):

    def __init__(self, start_page_url):
        self.start_page_url = start_page_url

    # 下载页面
    def download_page(self, page_url):
        try:
            # r_proxy = eval(random.choice(proxy_list))
            # user-agent 自动更换
            # page_headers['User-Agent'] = random.choice(u_a_list)
            # print(page_headers)

            # # Cookie 自动切换
            # page_headers['Cookie'] = cookie_list[0]

            rsp = requests.get(url=page_url, headers=page_headers, proxies=random.choice(pro_ip))
            print(rsp.status_code)
            while rsp.status_code != 200:
                # r_proxy = eval(random.choice(proxy_list))
                # # user-agent 自动更换
                # page_headers['User-Agent'] = random.choice(u_a_list)

                # # Cookie 自动切换
                # page_headers['Cookie'] = cookie_list[0]

                rsp = requests.get(url=page_url, headers=page_headers, proxies=random.choice(pro_ip))
            rsp_content = rsp.content
            return rsp_content

        except Exception as e:
            print(e)
            with open('unparse_url.text', 'a+', encoding='utf-8') as fp:
                fp.write(page_url+'\n')

        time.sleep(random.choice(range(1, 7)))

    # 提取页面中next_page的href
    def get_url(self, html):
        e_html = etree.HTML(html)
        if e_html != None:
            next_page_url = basic_url + e_html.xpath('//a[@class="next"]/@href')[0]
            if next_page_url:
                print(next_page_url)
                return next_page_url
            else:
                print(e_html)


if __name__ == '__main__':
    # 生成download_next_paged对象
    download_next_page = DownloadNextPageUrl(start_page_url)

    # page_url为page_url.txt中最后一条url, 也就是开始爬取时的页面．
    # page_url_list = []
    # fu = open('page_url.txt', 'r')
    # page_url_lines = fu.readlines()
    # for page_url_line in page_url_lines:
    #     p_url = page_url_line.strip('\n')
    #     page_url_list.append(p_url)
    #
    # # print(len(page_url_list)-1)
    # page_url = page_url_list[1991]
    page_url = start_page_url

    # 当page_url 存在时，获取next_page_url
    while page_url:
        # 写入文件
        with open('page_url.txt', 'a', encoding='utf-8') as f:
            f.write(page_url+'\n')
        # 下载页面内容，并经过etree.HTML()处理．
        e_html = download_next_page.download_page(page_url)
        # 获取页面中的nxet_page的href,并返回．
        page_url = download_next_page.get_url(e_html)

# # 获取下一页标签中的href
# def get_url(e_html):
#     next_page_url = basic_url + e_html.xpath('//a[@class="next"]/@href')[0]
#     """如果next_page的标签存在，那么采集放入数据库"""
#     if next_page_url:
#         print(next_page_url)
#         parm = (next_page_url, datetime.datetime.utcnow())
#         sql = """ INSERT INTO comment_next_page_url(next_page_url) VALUES('%s', '%s') """ % parm
#         try:
#             cursor.execute(sql)
#             conn.commit()
#         except Exception as e:
#             print(e)
#             conn.rollback()
#
#         return next_page_url
