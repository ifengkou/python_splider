
## wiki list

//查询记录条数
select count(*) from wiki_url

//查询是否有重复的wiki
select url,count(url) num from wiki_url group by url HAVING count(url)>1

// 三级 下的四级领域 重复
delete from wiki_url where cate in (487,19,20,495,322,265,449,516)
delete from category where id in(487,19,20,495,322,265,449,516)

//去重，除了min(id)的其他重复ID
select t1.* from wiki_url as t1,(
	select DISTINCT MIN(`id`) AS `id`,url,count(url) num from wiki_url group by url HAVING count(url)>1
) as t2
where t1.url = t2.url
	and t1.id <> t2.id

//将需要删除的记录ID 存入 临时表
insert into temp (
  	select t1.id from wiki_url as t1,(
  		select DISTINCT MIN(`id`) AS `id`,url,count(url) num from wiki_url group by url HAVING count(url)>1
  	) as t2
  	where t1.url = t2.url
  		and t1.id <> t2.id
  )

//删除重复记录
delete  from wiki_url where id in (select * from temp)

delete from temp
