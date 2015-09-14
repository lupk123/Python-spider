#-*-coding:utf-8-*- 
__author__ = 'Administrator'
import requests
from lxml import etree

class Weibo:
    def __init__(self):
        pass

    # 获取登录界面的源代码
    def getHtml(self, url):
        html = requests.get(url).content
        return html

    # 登录微博并获取想要页面的源代码
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
             'backTitle': '�ֻ�������',
             'tryCount': '',
             'vk': vk,
             'submit': '��¼'
        }
        html = requests.post(url_login, data=data).content
        return html

    #每一个table块
    def getTable(self, html):
        selector = etree.HTML(html)
        tables = selector.xpath('//table')[0]
        return tables

    # 获取想要的内容
    def getContent(self, table):
        #/html/body/table[5]/tbody/tr/td[1]/a/text()
        content = table.xpath('//tr/td/a[1]/text()')

        return content

    # 输出并保存
    def saveToFile(self, content):
        f = open('weibo.txt', 'a')
        for each in content:
            print each
            f.writelines('%s\n' % each.encode('utf-8'))
        f.close()


if __name__ == '__main__':
    link = 'http://weibo.cn/1251000504/follow?vt=4&page='
    links = []
    for i in range(1, 20):
        url = link + str(i)
        links.append(url)

    url_login = 'https://login.weibo.cn/login/'
    weibo = Weibo()
    html = weibo.getHtml(url_login)

    for each in links:
        posthtml = weibo.postHtml(each, url_login, html)
        tables = weibo.getTable(posthtml)
        for table in tables:
            content = weibo.getContent(tables)
            weibo.saveToFile(content)









