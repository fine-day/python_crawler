import datetime
import json
from pymongo import MongoClient
import requests

# 连接mongodb
MONGO_CONN = MongoClient(host='localhost', port=27017)
db = MONGO_CONN['crawler_data']
collection = db['movie_name']

page_url = 'https://movie.douban_movie.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=0&limit=700'

page_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Cookie': 'bid=TW9FfFM6rLw; gr_user_id=29061151-bb6d-44cd-ad35-cfa8c44fad9e; viewed="26320485"; ll="118172"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1494685854%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D2_KzZmOYx-nQGHTbLUZxLs2A2giBgQaw_4jBZXhoI-3T1yiblqj-0LBCFuAv_Hwi%26wd%3D%26eqid%3Dfc68b48f00081c7e0000000259171888%22%5D; _vwo_uuid_v2=2E583273E29B238DD800CDE6F2297EC8|56495192db8a4ad249e21c8e7fe81468; ap=1; __utma=30149280.1222714027.1493947656.1494296325.1494685854.4; __utmb=30149280.0.10.1494685854; __utmc=30149280; __utmz=30149280.1494685854.4.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1916477627.1494685854.1494685854.1494685854.1; __utmb=223695111.0.10.1494685854; __utmc=223695111; __utmz=223695111.1494685854.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_id.100001.4cf6=f047baabb3046834.1494685854.1.1494689835.1494685854.; _pk_ses.100001.4cf6=*',
    'Host':'movie.douban_movie.com',
    'Referer': 'https://movie.douban_movie.com/typerank?type_name=%E5%89%A7%E6%83%85&type=11&interval_id=100:90&action=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def download_page(url):
    page_data = requests.get(url=url, headers=page_headers).content
    page_data_list = json.loads(page_data)
    return page_data_list


def save_data(data):
    data['date'] = datetime.datetime.utcnow()
    data['_id'] = data['id']
    post_id = collection.insert_one(data).inserted_id
    print(post_id)


if __name__ == '__main__':
    movie_data_list = download_page(page_url)
    for movie_data in movie_data_list:
        save_data(movie_data)
        #
