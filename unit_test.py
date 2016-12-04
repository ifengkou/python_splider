# -*- coding: utf-8 -*-
import string
import urllib2
import json
from bs4 import BeautifulSoup
import httplib

from sys import path
path.append(r'H:\code\python')

from smzdm_splider_category import Categories_Spider
from smzdm_splider_mall import Mall_Spider

c_spider = Categories_Spider()
c_spider.test_print()

m_spider = Mall_Spider()
m_spider.test_print()

class Unit_test:
    def splider_all_tags(self):

        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        headers = { 'User-Agent' : user_agent }
        print u'已经启动get_tags....'
        _x_200 = range(100,200)
        tagUrl = 'http://wiki.smzdm.com/t'
        tags = []
        for x in _x_200:
            t_url = tagUrl + str(x)
            print t_url
            try:
                req = urllib2.Request(t_url, headers = headers)
                myPage = urllib2.urlopen(req).read().decode('utf-8')
                soup = BeautifulSoup(myPage,'lxml')

                dom_tag_a = soup.select('div[class*="right_wrap"] > div[class*="right_top_title"] > div[class*="lFloat"] > a')
                if not dom_tag_a:
                    continue
                tag ={'hot':0,'hot_tag':0}
                tag['name'] = dom_tag_a[0].get_text().replace("\n","")

                dom_tag_hotnumb_div = soup.select('div[class*="right_wrap"] > div[class*="right_top_title"] > div[class="total_pro"]')
                if dom_tag_hotnumb_div:
                    hot_numb_text = dom_tag_hotnumb_div[0].get_text()
                    print hot_numb_text
                    tag['hot_tag'] = int(hot_numb_text.replace('共','').replace('条产品',''))

                if tag['hot_tag'] == 0:
                    continue
                print(u'增加" %s "tag'%tag['name'])
                tags.append(tag)
            except:
                print u'当前page 没有tag 存在'
                continue

            # 按照类别 分批入库
        print json.dumps(tags,ensure_ascii=False)

test = Unit_test()
test.splider_all_tags()
