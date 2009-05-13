# coding=utf8
# -*- coding:utf8 -*- 
# baidu tieba rss
import datetime
import time

from tianya_rss import Obj
from tianya_rss import Visitor
from tianya_rss import toRss
from tianya_rss import httpGet

def html2post(html):
	start_h1='<div id="topic_list">'
	vis=Visitor()
	vis.pos=0
	vis.setText(html)
	vis.confirm(start_h1)
	posts=[]
	while True :
		if not vis.confirm('<td class="s">').found():
			break
		p=Obj()
		p.cat = "None"
		p.link = "<![CDATA[http://tieba.baidu.com%s]]>" % \
			vis.confirm('href="').readUntil('"')
		p.text = vis.confirm("target=_blank > ").readUntil("</a>")
		#pubDate =  vis.confirm("<td width='16%' bgcolor='#eeeeee' align='left'>").readUntil(' <a ')
		p.pubDate = datetime.datetime.now()
		p.author = "<![CDATA[%s]]>"%vis.confirm("<font color='#000000'>").readUntil("</font>")
		p.title = p.text
		posts.append(p)
	return posts

def baidurss(ba):
	url= "http://tieba.baidu.com/f?kw=%s"%ba
	html = httpGet(url,"gbk")
	posts = html2post(html)
	info=Obj()
	info.title="百度贴吧_%s吧".decode("utf8")%ba
	info.site="<![CDATA[%s]]>"%url
	info.desc="Rss %s"%info.title
	rss = toRss(info, posts)
	return rss
	
