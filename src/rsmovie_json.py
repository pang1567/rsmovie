__author__ = 'lenovo'
# -*- coding: utf-8 -*-

import config
import login_rs
import sys
import re
import urllib2
from bs4 import BeautifulSoup
from operator import itemgetter
reload(sys)
sys.setdefaultencoding("utf-8")


class Movie():
    """
    核心类，将睿思电影列表取出，分别搜索豆瓣的分数，每一个电影为一个元组，所有电影元组存放在movie_list[]列表中
    """

    """
    @:param初始化函数，定义了存储最终结果的列表movie_list
    """
    def __init__(self):
        self.movie_list = []

    """
    @:param str1表示完整的电影名字符串（例如：棋神/神的一步/神之一手(台)），此函数提取第一个(棋神)作为搜索豆瓣的电影名
    """
    def extract_movie_name(self, str1):
        list = str1.split('[')
        if list[3][0:-1].isdigit():
            name = list[4]
        else:
            name = list[3]

        if name.find('/') < name.find(']'):
            name = name[0:name.find('/')]
        else:
            name = name[0:name.find(']')]
        return name

    """
    @:param url某个电影在豆瓣的搜索页，可以通过请求此页面得到豆瓣分数
    """
    def douban_score(self, url):
        # print url
        try:
            response = urllib2.urlopen(url)
        except urllib2.URLError, e:
            print e.reason
            return 0
        html = response.read()
        soup = BeautifulSoup(html)
        # print html
        scores = soup.select("[class~=rating_nums]")
        if scores.__len__() != 0:
            score_str = str(scores[0])
        else:
            score_str = ''
        b = re.compile(r"(\d+)\.(\d)")
        # print score_str.__sizeof__(), score_str, b.match(score_str[26:29]).group()
        if score_str.__sizeof__() == 57 and b.match(score_str[26:29]):
            score = b.match(score_str[26:29]).group()
        else:
            score = 0
        return score
    """
    @:param html为睿思电影某一个page，一个page有五十部电影列表，
    此函数作用检索电影
    """
    def parse_movie(self, html):
        soup = BeautifulSoup(html)
        html_tbody = soup.find_all('tbody')

        for tbody in html_tbody:
        #for i in range(0, 10):
            #soup_tmp = BeautifulSoup(str(html_tbody[i]))
            soup_tmp = BeautifulSoup(str(tbody))
            herf = soup_tmp.find('tbody').find('tr').find('td', class_='common').find('a').get('href')
            name_tmp = soup_tmp.find('tbody').find('tr').find('td', class_='common').find('a').string
            movie_name = self.extract_movie_name(name_tmp)
            # print movie_name
            #movie_name.encode()

            score = self.douban_score(
                u'http://movie.douban.com/subject_search?search_text=' + movie_name + u'&cat=1002')
            if float(score) > 5.0:
                #print '|', movie_name, '|', float(score), '|', config.DOMAIN + herf[2:], '|'
                each_movie = (movie_name, score, config.DOMAIN + herf[2:])
                #print each_movie
                self.movie_list.append(each_movie)
    """
    将得到的结果一markdown表格格式写入data.md文件中，方便保存和发布文章
    """
    def write_result(self):
        self.movie_list.sort(key=itemgetter(1), reverse=True)
        '''
        for i in self.movie_list:
            print i[1]
        '''
        output = open('data.md', 'w')
        for tup in self.movie_list:
            str = '|' + tup[0] + '|' + tup[1] + '|' + '[' + tup[2] + ']' + '(' + tup[2] + ')' + '|'
            str1 = str.encode('gbk')
            output.write(str1)
            output.write('\n')
        output.close()


if __name__ == '__main__':
    my_account = login_rs.Discuz()
    my_account.login(config.USERNAME, config.PASSWORD)
    movie = Movie()
    for page in range(1, 5):
        #检索第一到第四页睿思电影列表
        rs_html = my_account._get_response('http://rs.xidian.edu.cn/bt.php?mod=browse&c=10&page=' + str(page))
        movie.parse_movie(rs_html)
    movie.write_result()




