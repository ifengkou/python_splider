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

class Item_Splider:
    def __init__(self):
        #属性类型不需要显示申明
        self.encoding = "utf-8"
        self.homeUrl = 'http://wiki.smzdm.com/'
        self.db = SMZDM_Mysql()
        self.myTool = HTML_Tool()
        self.thread_num = 10

        self.wiki_urls = []
        # 只抓取优选 wiki
        self.is_excellent = False

    def prepare_wiki_urls(self):
        self.wiki_urls = self.db.get_wiki_urls()

    def spider_start(self):
        print u'已经启动Wiki Item 爬虫，咔嚓咔嚓'
        self.db.init_db()
        self.prepare_wiki_urls()
        self.db.close_db()
        print u'共处理wiki_url数：'+str(len(self.wiki_urls))
        try:
            #send HTTP/1.0 request , adding this , fix the problem
            httplib.HTTPConnection._http_vsn = 10
            httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

            # 商品wiki 列表处理
            self.splide_wiki()

            #after | back to http 1.1
            httplib.HTTPConnection._http_vsn = 11
            httplib.HTTPConnection._http_vsn_str = 'HTTP/1.1'
        except Exception, e:
            print Exception,":",e
            return ''

        #self.db.close_db()
        print u'Wiki Item 爬虫服务运行结束.....'

    def splide_wiki(self):
        # 1. 将categories分为 thread_num 组
        data = self.init_group(self.thread_num,self.wiki_urls)
        pool = threadpool.ThreadPool(self.thread_num)
        #requests = threadpool.makeRequests(self.splide_wikiurl_by_cates, data,self.insert_db)
        requests = threadpool.makeRequests(self.splide_wiki_by_url, data)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def splide_wikiurl_by_cates(self,urls):
        print '---------------'
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        headers = { 'User-Agent' : user_agent }
        #一个线程一个db
        thread_db = SMZDM_Mysql()
        thread_db.init_db()

        for url in urls:
            current_cate_id = cate[1]
            current_cate_uri = cate[2]
            current_url = url[3]

            print(u'开始处理页面：%s'%current_url)
            # 加载页面
            req = urllib2.Request(current_url, headers = headers)
            myPage = urllib2.urlopen(req).read().decode(self.encoding)
            soup = BeautifulSoup(myPage,'lxml')

            # 基础 信息 splide
            # 优选 标题 短评 标签（多个） 分类 品牌  点赞数  收藏数 商品百科
            # 标签要存id 因为需要点击进入标签页
            base_info ={}

            # 图片 s

            # 商品短评 -- 最多取前3条
            comments = []
            #网友名 recommend指数 时用时长 （没用过 0, 1-3个月 1， 3-1年 2， 1年以上 3）,title,content（要带html格式） 点赞数 评论数（火热程度）
            comment ={}

            # 历史爆料 /价格
            #id 商城 关联商品id 日期 标题 价格 点赞数 点踩数 评论数（火热程度） 购买链接 点击链接


    def init_group(self,thread_num,urls):
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
