import time
import requests
from bs4 import BeautifulSoup

# num:获取代理的页数


class ProxyPool(object):

    def __init__(self, num):
        self.num = num

    def fetch_proxy(self):
        url = 'http://www.xicidaili.com/nn/{}'
        headers = {
            "User-Agent": "xxx"  
        }  # User-Agent: 使用自己浏览器的即可
        proxy_list = []
        for i in range(self.num+1):
            url = url.format(1)
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")

            tr_list = soup.find_all('tr', attrs={'class': 'odd'})
            for tr in tr_list:
                td = tr.find_all('td')
                ip = td[1].get_text()
                port = td[2].get_text()
                # print(ip, port)
                proxy = 'http://'+ip+':'+port
                proxies = {'proxy': proxy}
                proxy_list.append(proxies)
                # print(proxies)
            time.sleep(2)

        return proxy_list

    def test_proxy(self, proxy_list):
        test_url = 'https://www.baidu.com'
        for proxy in proxy_list:
            response = requests.get(url=test_url, proxies=proxy)
            rsp_code = response.status_code
            print(rsp_code)
            if rsp_code == 200:
                with open('proxy_pool.txt', 'a', encoding='utf-8') as f:
                    f.write(str(proxy)+'\n')


def main():
    proxy_pool = ProxyPool(num=10)
    proxy_list = proxy_pool.fetch_proxy()
    proxy_pool.test_proxy(proxy_list=proxy_list)


if __name__ == '__main__':
    main()
