# coding:utf8
# tianya rss
import datetime
import time
#from google.appengine.api import urlfetch
from tianya_rss import Obj
from tianya_rss import Visitor
from tianya_rss import toRss
from tianya_rss import httpGet

def getJsArray(js):
	return list(eval(js.strip()))

def html2post(html):
	vis=Visitor()
	vis.pos=0
	vis.setText(html)	
	topicIDArray=getJsArray(vis.confirm("topicIDArray = new Array").readUntil('\n'))
	titleArray=getJsArray(vis.confirm("titleArray = new Array").readUntil('\n'))
	firstDateArray=getJsArray(vis.confirm("firstDateArray = new Array").readUntil('\n'))
	firstUserNameArray=getJsArray(vis.confirm("firstUserNameArray = new Array").readUntil('\n'))
	#print (topicIDArray,titleArray,firstDateArray,firstUserNameArray)
	posts=[]
	cnt=len(topicIDArray)-1
	for i in range(cnt):
		p=Obj()
		p.cat = "自然科学"
		p.link = "<![CDATA[http://sonicbbs.eastday.com/topicdisplay.asp?BoardID=22&Page=1&TopicID=%s]]>" % topicIDArray[i]
		p.text = titleArray[i]
		pubDate = firstDateArray[i]
		p.pubDate = datetime.datetime(*(time.strptime(pubDate,"%Y-%m-%d %H:%M:%S")[0:6]))
		p.author = firstUserNameArray[i]
		p.title = p.text
		posts.append(p)
	return posts

def sonicbbsRss():
	url= "http://59.173.12.109/asp_js/boarddisplay_js.asp?BoardID=22&Page=1&State=0&UserName=neoedmund"
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
