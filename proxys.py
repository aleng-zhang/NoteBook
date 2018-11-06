# -*- coding:utf-8 -*-

import lxml
import time
import requests
import threading
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
}

def get_ip():
    url = "http://www.xicidaili.com/nn/"
    html = requests.get(url, headers=headers).content.decode("utf-8")
    soup = BeautifulSoup(html, "lxml")
    ips = soup.find_all('tr')
    proxys = []
    for i in range(1,len(ips)):
        ip_info = ips[i].find_all('td')
        proxys.append({ip_info[5].text: ip_info[1].text + ":" + ip_info[2].text})
    return proxys

def check_ip(proxy):
    url = "http://www.baidu.com"
    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
        time.sleep(5)
        if response.status_code == 200:
            print(proxy, '----Pass!')
            proxys_pool.write("%s\n" %str(proxy))
        else:
            print(proxy, '----Fail!')
    except Exception as e:
        print(proxy, e)
        time.sleep(5)

if __name__ == "__main__":
    proxys = get_ip()
    print(proxys)
    proxys_pool = open(".\proxys_pool.txt", "w")
    '''单线程版本
    for i in range(len(proxys)):
        check_ip(proxys[i])
    '''
    lock = threading.Lock()
    threads = []
    try:
        for i in range(len(proxys)):
            thread = threading.Thread(target=check_ip, args=[proxys[i]])
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    except Exception as e:
        print(e)
    proxys_pool.close()