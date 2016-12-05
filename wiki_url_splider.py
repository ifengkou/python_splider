# -*- coding: utf-8 -*-
#为了系统能正常显示中文
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import string
import urllib2
import json
# 一个python 爬虫库
from bs4 import BeautifulSoup
import httplib
import time,random
import threadpool

from html_tool import HTML_Tool
from smzdm_mysql import SMZDM_Mysql
from file_tool import File_Tool

class Wiki_Splider:
    def __init__(self):
        #属性类型不需要显示申明
        self.encoding = "utf-8"
        self.homeUrl = 'http://wiki.smzdm.com/'
        self.db = SMZDM_Mysql()
        self.myTool = HTML_Tool()
        self.categories = []
        self.thread_num = 8
    def prepare_categories(self):
        _categories = self.db.get_categories(2)
        for category in _categories:
            self.categories.append(category)

    def spider_start(self):
        print u'已经启动Wiki 爬虫，咔嚓咔嚓'
        self.db.init_db()
        self.prepare_categories()
        print u'共处理category数：'+str(len(self.categories))
        try:
            #send HTTP/1.0 request , adding this , fix the problem
            httplib.HTTPConnection._http_vsn = 10
            httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
            # 处理热门标签
            #self.splider_hot_tags(headers)

            # 处理一般标签，轮询url
            self.splide_wiki()

            #after | back to http 1.1
            httplib.HTTPConnection._http_vsn = 11
            httplib.HTTPConnection._http_vsn_str = 'HTTP/1.1'
        except Exception, e:
            self.db.close_db()
            print Exception,":",e
            return ''

        self.db.close_db()
        print u'Wiki 爬虫服务运行结束.....'

    def splide_wiki(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        headers = { 'User-Agent' : user_agent }

        # 1. 将categories分为 thread_num 组
        data = self.init_group(self.thread_num,self.categories)
        pool = threadpool.ThreadPool(self.thread_num)
        requests = threadpool.makeRequests(self.splide_wikiurl_by_cates, data,self.insert_db)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def splide_wikiurl_by_cates(self,cates):
        urls = []
        for cate in cates:
            current_cate_uri = cate[2]
            page_url = self.homeUrl+current_cate_uri+'/you'
            urls.append(page_url)
        time.sleep(2)
        return urls

    def init_group(self,thread_num,cates):
        cates_num = len(cates)
        piece_num = cates_num/thread_num
        residue_num = cates_num%thread_num
        #print piece_num,residue_num
        index = 0
        result = []
        for i in range(0,thread_num):
            value = piece_num+1 if i < residue_num else piece_num
            next_index = index+value
            result.append(cates[index:next_index])
            index = next_index
        return result

    def insert_db(self,request,wiki_urls):
        print json.dumps(wiki_urls,ensure_ascii=False)

w_splider = Wiki_Splider()
w_splider.spider_start()
