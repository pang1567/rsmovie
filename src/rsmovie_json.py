__author__ = 'lenovo'
# -*- coding: utf-8 -*-

import config
import login_rs

if __name__ == '__main__':
    my_account = login_rs.Discuz()
    my_account.login(config.USERNAME, config.PASSWORD)
    movie = my_account._get_response('http://rs.xidian.edu.cn/bt.php?mod=browse&c=10')
    print movie.read()