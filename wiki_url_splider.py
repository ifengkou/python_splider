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
        self.thread_num = 4

        self.page_item_size = 20
        self.wiki_items =[]

        # 只抓取优选 wiki
        self.is_excellent = False

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

            # 商品wiki 列表处理
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
        # 1. 将categories分为 thread_num 组
        data = self.init_group(self.thread_num,self.categories)
        pool = threadpool.ThreadPool(self.thread_num)
        #requests = threadpool.makeRequests(self.splide_wikiurl_by_cates, data,self.insert_db)
        requests = threadpool.makeRequests(self.splide_wikiurl_by_cates, data)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def splide_wikiurl_by_cates(self,cates):
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        headers = { 'User-Agent' : user_agent }
        #wiki_results = []
        for cate in cates:
            current_cate_uri = cate[2]
            current_cate_id = cate[0]
            page_url = self.homeUrl+current_cate_uri
            if self.is_excellent:
                page_url = self.homeUrl+current_cate_uri+'/you'
            print(u'开始处理页面：%s'%page_url)
            # 加载页面
            req = urllib2.Request(page_url, headers = headers)
            myPage = urllib2.urlopen(req).read().decode(self.encoding)
            soup = BeautifulSoup(myPage,'lxml')

            # 计算分页数
            item_num = 0
            dom_item_numb_div = soup.select('div[class*="right_wrap"] > div[class*="right_top_title"] > div[class="total_pro"]')
            if dom_item_numb_div:
                item_numb_text = dom_item_numb_div[0].get_text()
                #print item_numb_text
                if self.is_excellent:
                    item_num = int(item_numb_text.replace('共','').replace('条优选产品',''))
                else:
                    item_num = int(item_numb_text.replace('共','').replace('条产品',''))

            if not item_num:
                continue

            page_numb = (item_num  +  self.page_item_size  - 1) / self.page_item_size
            print(u'%s,共%s页，%s条记录'%(current_cate_uri,page_numb,item_num))
            # 用于存储wiki_item 的url
            page_urls = []
            # 当前页 也就是第一页
            page_urls.extend(self.splide_wiki_list_item_url(soup))
            # 后面的页
            for i in range(2,page_numb+1):
                #print u'开始处理第%s页'%i
                other_page_url = page_url +'/p' + str(i)
                other_req = urllib2.Request(other_page_url, headers = headers)
                other_page = urllib2.urlopen(other_req).read().decode(self.encoding)
                other_soup = BeautifulSoup(other_page,'lxml')
                page_urls.extend(self.splide_wiki_list_item_url(other_soup))

            # 当前cate 的所有wiki_item
            wiki_items = []
            for item in page_urls:
                wiki_u = {}
                wiki_u['url'] = item
                wiki_u['cate'] = current_cate_id
                wiki_u['cate_uri'] = current_cate_uri
                wiki_items.append(wiki_u)

            print(u'%s,开始入库,共计%s条记录'%(current_cate_uri,len(wiki_items)))
            self.insert_db({},wiki_items)
            #wiki_results.extend(wiki_items)

        #return wiki_results

    def splide_wiki_list_item_url(self,soup):
        dom_wiki_list_a = soup.select('div[class*="right_wrap"] > div[class*="zk_new"] > a[class="pic_box"]')
        # 采集 url
        urls = []
        for a in dom_wiki_list_a:
            urls.append(a['href'])
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

    def insert_db(self,request,wiki_results):
        #print json.dumps(wiki_items,ensure_ascii=False)
        if not wiki_results:
            return ''
        sqlvalues = []
        for bean in wiki_results:
            sqlvalues.append((bean['cate'],bean['cate_uri'],bean['url']))

        # 批量插入 商城
        #print sqlvalues
        self.db.insert_wiki_urls(sqlvalues)
        self.db.commit()

w_splider = Wiki_Splider()
w_splider.spider_start()
