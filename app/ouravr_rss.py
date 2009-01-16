# coding:utf8
# tianya rss
import datetime
import time
#from google.appengine.api import urlfetch
from tianya_rss import Obj
from tianya_rss import Visitor
from tianya_rss import toRss
from tianya_rss import httpGet

def html2post(html):
	start_h1="<body"
	vis=Visitor()
	vis.pos=0
	vis.setText(html)
	vis.confirm(start_h1)
	posts=[]
	while True :
		if not vis.confirm("<table width='100%' border='1' cellpadding='5'").found():
			break
		p=Obj()
		p.cat = vis.confirm(" target='_blank' class='tt1'>").readUntil("</a>")
		p.link = "<![CDATA[http://ouravr.com/bbs/%s]]>" % \
			vis.confirm('<a href=').readUntil(" class='tt1'")
		p.text = vis.confirm(" target='_blank'>").readUntil("</a>")
		pubDate =  vis.confirm("<td width='16%' bgcolor='#eeeeee' align='left'>").readUntil(' <a ')
		p.pubDate = datetime.datetime(*(time.strptime(pubDate,"%Y%m%d")[0:6]))
		p.author = "<![CDATA[%s]]>"%vis.confirm("user_information.jsp?user_name=").readUntil("'")
		p.title = p.text
		posts.append(p)
	return posts

def ouravrRss():
	url= "http://ouravr.com/bbs/bbs_list.jsp?bbs_id=9999"
	html = httpGet(url,"gbk")
	#print html
	posts = html2post(html)
	info=Obj()
	info.title="ourdev.cn 虚拟总论坛"
	info.site="<![CDATA[%s]]>"%url
	info.desc="虚拟总论坛（可查看所有分论坛的帖子）"
	rss = toRss(info, posts)
	return rss
	
	
if __name__=="__main__":
	print ouravrRss()
