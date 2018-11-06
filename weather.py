# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def get_province_data():
    url = "http://flash.weather.com.cn/wmaps/xml/china.xml"
    html = requests.get(url, headers=headers).content.decode("utf-8")
    soup = BeautifulSoup(html,'lxml')
    province_dicts = {}
    for province in soup.find_all("city"):
        province_dicts.update({
            province['quname']: province['pyname']
            })
    province_names = list(province_dicts.keys())
    for j in range(len(province_names)):
        output = str(j+1) + '. ' + province_names[j]
        if j < 9:
            output = ' ' + output
        print("{:<10}".format(output), end='')
        if (j+1)%5 == 0:
            print('')
    print('')
    province_num = int(input('请输入相应序号: '))
    new_url = 'http://flash.weather.com.cn/wmaps/xml/' + province_dicts[province_names[province_num - 1]] + '.xml'
    return new_url 

def get_city_data():
    url = get_province_data()
    html = requests.get(url, headers=headers).content.decode("utf-8")
    soup = BeautifulSoup(html,'lxml')
    city_dicts = {}
    for city in soup.find_all("city"):
        city_dicts.update({
            city['cityname']: [city['statedetailed'], city['tem2'], city['tem1'], city['windstate'],city['humidity'], city['url']]
            })
    city_names = list(city_dicts.keys())
    for j in range(len(city_names)):
        output = str(j+1) + '. ' + city_names[j]
        print("{:<10}".format(output), end='')
        if (j+1)%5 == 0:
            print('')
    print('')
    city_num = int(input('请输入相应序号: '))
    return city_dicts[city_names[city_num-1]]

def print_weather():
    weather = get_city_data()

    print(
        '*------------------------------*\n',
        "天气: " + weather[0] + '\n',
        "气温: " + weather[2] + '°C ~ ' + weather[1] + '°C \n',
        "详情请点击: http://www.weather.com.cn/weather1d/" + weather[5] + '.shtml'
    )

if __name__ == "__main__":
    print_weather()