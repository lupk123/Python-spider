#-*-coding:utf-8-*- 
__author__ = 'Administrator'
import requests
from lxml import etree
import time
import os

class Weibo:
    def __init__(self):
        pass

    def getHtml(self, url):
        html = requests.get(url).content
        return html

    def postHtml(self, url, url_login, html):
        selector = etree.HTML(html)
        password = selector.xpath('//input[@type="password"]/@name')[0]
        vk = selector.xpath('//input[@name="vk"]/@value')[0]
        action = selector.xpath('//@action')[0]
        url_login += action

        data = {
            'mobile': '15764236710',
             password: '1314vae1121',
             'remember': 'on',
             'backURL': url,
             'backTitle': '手机新浪网',
             'tryCount': '',
             'vk': vk,
             'submit': '登录'
        }
        html = requests.post(url_login, data=data).content
        return html

    def getContent(self, html):
        selector = etree.HTML(html)
        content = selector.xpath('//span[@class="ctt"]/text()')[0]
        print content
        return content

    def saveToFile(self, content):
        if not os.path.exists('weibo.txt'):
            return True
        else:
            f = open('weibo.txt', 'wr')
            txt = f.readlines()
            if content+'\n' in txt:
                f.close()
                return False
            else:
                f.writelines(txt)
                f.close()
                return True

if __name__ == '__main__':
    url = 'http://weibo.cn/3036975625/profile?vt=4'
    url_login = 'https://login.weibo.cn/login/'
    weibo = Weibo()
    while True:
        html = weibo.getHtml(url_login)
        posthtml = weibo.postHtml(url, url_login, html)
        content = weibo.getContent(posthtml)
        weibo.saveToFile(content)
        time.sleep(30)








