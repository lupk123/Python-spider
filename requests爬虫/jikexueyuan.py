import requests
import re

class Spider:
    def __init__(self):
        print('start...: \n')

#获取所有连接（不止爬一页）
    def setLinkList(self, url, end):
        links = []
        page = int(re.search('pageNum=(\d)', url, re.S).group(1))
        for i in range(page, end+1):
           link = re.sub('pageNum=\d+', 'pageNum=%s'%i, url, re.S)
           links.append(link)
        return links

#获得网页源代码
    def getSource(self, url):
        html = requests.get(url)
        return html

#获取页面的课程块
    def getCourse(self, html):
        course = re.findall('<li id="\d{4}" test="[01]" deg="[01]".*?>(.*?)</li>', html.text, re.S)
        return course

#获取每个课程块的课程详细信息
    def getContent(self, course):
        info = {}
        reg_title = '<h2 class="lesson-info-h2"><a.*?>(.*?)</a></h2>'
        reg_content = '<p.*?>(.*?)</p>'
        reg_time = '<i class="time-icon"></i><em>(.*?)</em>'
        reg_level = '<i class="xinhao-icon\d?"></i><em>(.*?)</em>'
        reg_people = 'class="learn-number">(.*?)</em>'
        info['title'] = re.search(reg_title, course, re.S).group(1)
        info['time'] = re.search(reg_time, course, re.S).group(1)
        info['content'] = re.search(reg_content, course, re.S).group(1)
        info['level'] = re.search(reg_level, course, re.S).group(1)
        info['people'] = re.search(reg_people, course, re.S).group(1)
        return info

#将获取的课程信息保存到文件中
    def saveFile(self, classInfo):
        f = open('result.txt', 'a')
        for info in classInfo:
            f.writelines('title:'+info['title']+'\n')
            f.writelines('content:'+info['content']+'\n')
            f.writelines('time:'+info['time']+'\n')
            f.writelines('level:'+info['level']+'\n')
            f.writelines('people:'+info['people']+'\n\n')


if __name__ == '__main__':
    classInfo = []
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    spider = Spider()
    links = spider.setLinkList(url, 2)
    for link in links:
        print('get rid of '+link)
        html = spider.getSource(link)
        course = spider.getCourse(html)
        for each in course:
            info = spider.getContent(each)
            # print(info['title'])
            classInfo.append(info)
    spider.saveFile(classInfo)
