# -*- coding: utf-8 -*-
#为了系统能正常显示中文
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import string
import urllib2
import json
from bs4 import BeautifulSoup
import httplib

from sys import path
path.append(r'H:\code\python')

# from smzdm_splider_category import Categories_Spider
# from smzdm_splider_mall import Mall_Spider
#
# c_spider = Categories_Spider()
# c_spider.test_print()
#
# m_spider = Mall_Spider()
# m_spider.test_print()

def init_group(thread_num,cates):
    cates_num = len(cates)
    piece_num = cates_num/thread_num
    residue_num = cates_num%thread_num
    print piece_num,residue_num
    index = 0
    result = []
    for i in range(0,thread_num):
        value = piece_num+1 if i < residue_num else piece_num
        next_index = index+value
        result.append(cates[index:next_index])
        index = next_index

    return result

results = init_group(8,range(1,65))
print results

for i in range(2,3):
    print i

print(u'共%s页，%s条记录'%(3,2))
