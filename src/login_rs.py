__author__ = 'lenovo'
# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import re

import config


class Discuz(object):
    def __init__(self):
        self.operate = ''  # response的对象（不含read）
        self.formhash = ''  # 没有formhash不能发帖

        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

        self.formhash_pattern = re.compile(r'<input type="hidden" name="formhash" value="([0-9a-zA-Z]+)" />')

    def login(self, username, password, questionid=0, answer=''):
        postdata = {
            #'loginfield': config.LOGINFIELD,
            'username': username,
            'password': password,
            'questionid': questionid,
            'answer': answer,
            'referer' : 'http://rs.xidian.edu.cn/'
            #'cookietime': config.COOKIETIME,
        }

        # 取得登录成功/失败的提示信息
        self.operate = self._get_response(config.LOGINURL, postdata)
        '''
        print self.operate.read()
        reqmovie = urllib2.Request(
            url="http://rs.xidian.edu.cn/bt.php?mod=browse&c=10"
        )
        MOVIE = self.opener.open(reqmovie).read()
        print  MOVIE
        '''
        login_tip_page = self.operate.read()

        # 显示登录成功/失败信息
        if 'succeedhandle_login' in login_tip_page:
            self.formhash = self._get_formhash(self._get_response(config.HOMEURL).read())
            print '登录成功'
            return True
        else:
            print '无法获取登录状态'

        return False

    def _get_response(self, url, data=None):
        if data is not None:
            req = urllib2.Request(url, urllib.urlencode(data))
        else:
            req = urllib2.Request(url)

        response = self.opener.open(req)
        return response

    def _get_formhash(self, page_content):
        self.formhash = self.formhash_pattern.search(page_content.decode('utf-8')).group(1)
        return self.formhash