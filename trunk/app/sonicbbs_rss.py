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
	start_h1="<body>"
	vis=Visitor()
	vis.pos=0
	vis.setText(html)
	vis.confirm(start_h1)
	posts=[]
	while True :
		if not vis.confirm("<td class=\"listbody\">").found():
			break
		p=Obj()
		p.cat = "自然科学"
		p.link = "<![CDATA[http://sonicbbs.eastday.com/topicdisplay_safe.asp?BoardID=22&Page=1&TopicID=%s]]>" % vis.confirm('<a href="topicdisplay.asp?BoardID=22&Page=1&TopicID=').readUntil('">')
		p.text = vis.readUntil("</a>")
		pubDate =  vis.confirm("发表时间：").readUntil('">')
		p.pubDate = datetime.datetime(*(time.strptime(pubDate,"%Y-%m-%d %H:%M:%S")[0:6]))
		p.author = "<![CDATA[%s]]>"%vis.confirm("UserName=").readUntil('">')
		p.title = p.text
		posts.append(p)
	return posts

def sonicbbsRss():
	url= "http://sonicbbs.eastday.com/boarddisplay.asp?BoardID=22"
	html = httpGet(url,"gbk")
	posts = html2post(html)
	info=Obj()
	info.title="sonicbbs 自然科学[1]"
	info.site="<![CDATA[%s]]>"%url
	info.desc="自然科学[1]"
	rss = toRss(info, posts)
	return rss
	
	
if __name__=="__main__":
	print sonicbbsRss()
