# coding:utf8
# rss
import datetime
import time
#from google.appengine.api import urlfetch
from tianya_rss import Obj
from tianya_rss import Visitor
from tianya_rss import toRss
from tianya_rss import httpGet
from google.appengine.api import mail
from google.appengine.ext import db

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
		if not existed(p):
			mailme(p)
	return posts
class RssFeed(db.Model):
	data = db.StringProperty()

def existed(p):
	feed=RssFeed.gql("WHERE data = :1 ", p.title).get()
	if feed:
		return True
	else:
		feed=RssFeed(data=p.title)
		feed.put()
		return False

def mailme(p):	
	mail.send_mail(sender="neoedmund@gmail.com",
		      to="neoedmund@gmail.com",
		      subject="%s"%p.text,
		      body="%s"%p.link)
	
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
