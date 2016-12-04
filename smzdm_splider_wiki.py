# -*- coding: utf-8 -*-

优选商品列表 http://wiki.smzdm.com/diannaoshuma/you/

    列表要选取 三级列表进行 查询

    category_id
    title tags # 已经爬取 1-200 ，800-900 明天爬


主商品wiki

    商品名称/title 描述 品类（字符） 品牌 点赞数 收藏数
    title,description,class_name,brand,thumbs-up,favorites,wiki

    规格/版本列表 spec list
    images list [一般是4张  url , ismain

值友点评：http://wiki.smzdm.com/p/2njw9k/dianping/
    点评list
    网友名 recommend指数 时用时长 （没用过 0, 1-3个月 1， 3-1年 2， 1年以上 3）,title,content（要带html格式） 点赞数 评论数（火热程度）
    netman  recommend use_duration title content thumbs-up_numb comment_numb

价格参考：http://wiki.smzdm.com/p/2njw9k/jiage/
    price_list
    商城 日期 标题 价格 点赞数 评论数（火热程度）
    mall date title price thumbs-up_numb comment_numb


值友原创：http://wiki.smzdm.com/p/2njw9k/yuanchuang/
    不爬取
