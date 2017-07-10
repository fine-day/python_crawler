"""
  此部分代码，是将comment_url.py中生成的txt文件写入数据库．（可以将此部分代码和comment_url.py进行合并，删去中间
  生成txt文件的过程，直接将数据存入数据库．
"""


import pymysql
import time
from datetime import datetime
from multiprocessing import Pool

next_page_url_list = []
url_list = []


class DataBae(object):

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
        f = open('page_url.txt', 'r')
        lines = f.readlines()
        for line in lines:
            next_page_url = line.strip('\n')
            next_page_url_list.append(next_page_url)

        d＿next_page_url_list = list(set(next_page_url_list))
        return d＿next_page_url_list

    def save_data(self, page_url):
        id = url_list.index(page_url) + 1
        s_time = str(datetime.now())
        param = (id, page_url, s_time)
        sql = """INSERT INTO comment_url(id, page_url, submission) VALUES ('%s', '%s', '%s') """ % param

        try:
            cursor.execute(sql)
            conn.commit()

        except Exception as e:
            print(e)
            conn.rollback()

        time.sleep(0.3)

    def close_db(self):
        cursor.close()
        conn.close()


if __name__ == '__main__':
    db = DataBae(host_name='localhost', port_num=3306, user_name='root', password='root', db_name='douban_movie')
    db.open_db()
    url_list = db.get_data()

    pool = Pool()
    for page_url in url_list:
        pool.apply_async(db.save_data, args=(page_url,))
    pool.close()
    pool.join()

    db.close_db()
