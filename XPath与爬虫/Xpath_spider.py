from lxml import etree
from multiprocessing.dummy import Pool
import json
import requests

class Spider:
    def __init__(self):
        print 'start...'

    def getLinks(self, url, end):
        links = []
        for i in range(1, end):
            link = url
            link += str(i)
            links.append(link)
        return links

    def getSource(self, url):
        html = requests.get(url)
        # f = open('source.txt', 'a')
        # f.write(html.text.encode('utf-8'))
        # f.close()
        return html

    def getEveryMod(self, html):
        #//*[@id="j_p_postlist"]
        selector = etree.HTML(html.text)
        EveryMod = selector.xpath('//div[@class="l_post l_post_bright j_l_post clearfix  "]')
        # EveryMod = selector.xpath('//div/@class')
        return EveryMod

    def getDetails(self, content):
        #//*[@id="j_p_postlist"]/div[1]
        data_filed = json.loads(content.xpath('@data-field')[0].replace('&quot', ''))
        # data_filed = content.xpath('//@data-field')
        author = data_filed['author']['user_name']
        print author
        # details = content.xpath('div[@class="d_post_content_main"]/div/cc/div[@class="d_post_content j_d_post_content"]/text()')
        details = data_filed['content']['content']
        print details
        print '<br\>'
        # time = content.xpath('//span[@class="tail-info"][2]/text()')
        # print time

if __name__ == '__main__':
    url = 'http://tieba.baidu.com/p/4033191329?pn='
    spider = Spider()
    links = spider.getLinks(url, 3)
    for link in links:
        print 'start with '+link
        html = spider.getSource(link)
        EveryMod = spider.getEveryMod(html)
        # print EveryMod
        for each in EveryMod:
            spider.getDetails(each)
