# coding:utf8
# rss
import datetime
import time
#from google.appengine.api import urlfetch
from tianya_rss import Obj
from tianya_rss import Visitor
from tianya_rss import toRss
from tianya_rss import httpGet

def html2post(html):
	vis=Visitor()
	vis.pos=0
	vis.setText(html)	
	vis.confirm('<div id="content"')
	vis.confirm('Files')
	posts=[]
	while 1:
		if not vis.confirm('<a href="http://ccp.vo.llnwd.net').found():
			break
		u="http://ccp.vo.llnwd.net"+vis.readUntil('">')
		u2=vis.readUntil('</A>')
		p=Obj()
		p.cat = "toolkit"
		p.link = "<![CDATA[%s]]>" % u
		p.text = u2
		p.pubDate = datetime.datetime(*(time.strptime("2009-1-1 0:0:0","%Y-%m-%d %H:%M:%S")[0:6]))
		p.author = "eve"
		p.title = u2
		posts.append(p)
	return posts

def evetoolkitRss():
	url= "http://www.eveonline.com/community/toolkit.asp"
	html = httpGet(url,"utf8")
	posts = html2post(html)
	info=Obj()
	info.title="EVE Data Export"
	info.site="<![CDATA[%s]]>"%url
	info.desc="EVE Data Export"
	rss = toRss(info, posts)
	return rss
	
	
if __name__=="__main__":
	print evetoolkitRss()
