__author__ = 'lenovo'
# -*- coding: utf-8 -*-

import config
import login_rs
import sys
import re
import urllib2
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding( "utf-8" )


class Movie():
    def __init__(self):
        self.htm = 0

    def extract_movie_name(self,str1):
        #str(str1)
        list = str1.split('[')
        #for str in list:
            #print str
        if list[3][0:-1].isdigit():
            name = list[4]
        else:
            name = list[3]

        if name.find('/') < name.find(']'):
            name = name[0:name.find('/')]
        else:
            name = name[0:name.find(']')]

        #name = name[0:name.find('/')]
        #print '电影名为',name
        return name

    def douban_score(self,url):
        #print url
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)
        #print html
        scores = soup.select("[class~=rating_nums]")
        score = str(scores[0])
        #print score[26:29]
        return score[26:29]

    def parse_movie(self,html):
        soup = BeautifulSoup(html)
        html_tbody = soup.find_all('tbody')

        for tbody in html_tbody:
            soup_tmp = BeautifulSoup(str(tbody))
            herf = soup_tmp.find('tbody').find('tr').find('td',class_='common').find('a').get('href')
            name_tmp = soup_tmp.find('tbody').find('tr').find('td',class_='common').find('a').string
            movie_name = self.extract_movie_name(name_tmp)
            #print movie_name
            #movie_name.encode()

            score = self.douban_score(u'http://movie.douban.com/subject_search?search_text=' + movie_name + u'&cat=1002')
            #if !socre.isdigit():
            print movie_name, score,config.DOMAIN + herf[2:]








if __name__ == '__main__':
    my_account = login_rs.Discuz()
    my_account.login(config.USERNAME, config.PASSWORD)
    rs_html = my_account._get_response('http://rs.xidian.edu.cn/bt.php?mod=browse&c=10')
    movie = Movie()
    movie.parse_movie(rs_html)
    # print movie.read()



