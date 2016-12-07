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

class Cate_Node_Splider:
    def __init__(self):
        #属性类型不需要显示申明
        self.encoding = "utf-8"
        self.homeUrl = 'http://wiki.smzdm.com/'
        self.db = SMZDM_Mysql()
        self.myTool = HTML_Tool()
        self.categories = []
        self.thread_num = 10

    def prepare_categories(self):
        _categories = self.db.get_categories(2)
        for category in _categories:
            self.categories.append(category)

    def spider_start(self):
        print u'已经启动 四级分类 爬虫，咔嚓咔嚓'
        self.db.init_db()
        self.prepare_categories()
        self.db.close_db()
        print u'共处理category数：'+str(len(self.categories))
        try:
            #send HTTP/1.0 request , adding this , fix the problem
            httplib.HTTPConnection._http_vsn = 10
            httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

            # 商品wiki 列表处理
            self.splide_cate_level3()

            #after | back to http 1.1
            httplib.HTTPConnection._http_vsn = 11
            httplib.HTTPConnection._http_vsn_str = 'HTTP/1.1'
        except Exception, e:
            print Exception,":",e
            return ''

        #self.db.close_db()
        print u'四级分类 爬虫服务运行结束.....'

    def splide_cate_level3(self):
        # 1. 将categories分为 thread_num 组
        data = self.init_group(self.thread_num,self.categories)
        pool = threadpool.ThreadPool(self.thread_num)
        #requests = threadpool.makeRequests(self.splide_wikiurl_by_cates, data,self.insert_db)
        requests = threadpool.makeRequests(self.splide_catenode_by_cate2, data)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def splide_catenode_by_cate2(self,cates):
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        headers = { 'User-Agent' : user_agent }
        #一个线程一个db
        thread_db = SMZDM_Mysql()
        thread_db.init_db()
        node_results = []
        for cate in cates:
            current_cate_uri = cate[2]
            current_cate_id = cate[0]
            page_url = self.homeUrl+current_cate_uri
            print(u'开始处理页面：%s'%page_url)
            # 加载页面
            req = urllib2.Request(page_url, headers = headers)
            myPage = urllib2.urlopen(req).read().decode(self.encoding)
            soup = BeautifulSoup(myPage,'lxml')

            dom_node_a = soup.select('ul[class="search_result_ul"] > li[class="current"] > ul > li > a ')

            if dom_node_a:
                print(u'%s ,存在 %s 个四级分类'%(current_cate_uri,len(dom_node_a)))
                for item in dom_node_a:
                    node = {}
                    _href = item['href'].replace('/you','').replace('/','')
                    node['uri'] = _href
                    _text = self.myTool.Replace_Char(item.get_text().replace("\n","").encode(self.encoding))
                    _pos = _text.find('(')
                    node['name'] =_text[:_pos]
                    node['parent_id'] = current_cate_id
                    node['level'] = 3
                    node_results.append(node)

        #print json.dumps(node_results,ensure_ascii=False)
        #print node_results
        self.insert_db(node_results,thread_db)
        thread_db.close_db()

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

    def insert_db(self,node_results,db):
        #print json.dumps(wiki_items,ensure_ascii=False)
        if not node_results:
            return ''
        sqlvalues = []
        for bean in node_results:
            #(name,parent_id,level,uri)
            sqlvalues.append((bean['name'],bean['parent_id'],bean['level'],bean['uri']))

        # 批量插入 商城
        #print sqlvalues
        db.insert_categories(sqlvalues)
        db.commit()

splider = Cate_Node_Splider()
splider.spider_start()
