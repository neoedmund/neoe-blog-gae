# coding:utf8
# tianya rss
import datetime
import time
from google.appengine.api import urlfetch

def toRss(info, posts):
	t = []
	t.append("""<?xml version="1.0" encoding="UTF-8" ?><rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel><title>%s</title><link>%s/</link>
<description>%s</description>""" % (info.title, info.site, info.desc))
	#if len(posts)>0:
		#t.append("<pubDate>%s</pubDate>"%posts[0].pubDate.strftime("%a, %d %b %Y %H:%M:%S +0000"))
	for p in posts:
		text = p.text.decode("utf8","ignore")
		if len(text)>1500:
			text = text[:1500]+" ... "
		t.append("""<item><title><![CDATA[%s]]></title>
<link>%s</link>
<pubDate>%s</pubDate>
<dc:creator>%s</dc:creator>
<category>%s</category>
<description><![CDATA[%s]]></description></item>""" % (p.title, p.link, 
p.pubDate.strftime("%a, %d %b %Y %H:%M:%S +0000"),p.author,p.cat,text.encode("utf8")))
	t.append("</channel></rss>")
	return "".join(t)
class Visitor:
	pos=0
	def setText(self, txt):
		self.txt=txt
	def confirm(self, s):
		self.pos = self.txt.find(s,self. pos)
		if self.pos>=0 :  self.pos += len(s)
		return self
	def readUntil(self, s):
		p1=self.pos
		self.pos=self.txt.find(s, self.pos)
		if self.pos>=0 and p1>=0 : 
			rs = self.txt[p1:self.pos]
			self.pos += len(s)
			return rs
		return ""
	def found(self):
		return self.pos >= 0
class Obj:pass
def html2post(html):
	start_h1="<table width=640 border=0 cellspacing=0>"
	vis=Visitor()
	vis.pos=0
	vis.setText(html)
	vis.confirm(start_h1)
	posts=[]
	while True :
		if not vis.confirm("<tr><td width=80><font color=").found():
			break
		p=Obj()
		p.cat = vis.confirm(">").readUntil("</font>")
		p.link = "<![CDATA[http://www.tianya.cn/new/publicforum/%s]]>" % vis.confirm("</td><td width=335><a href='").readUntil("'")
		p.text = vis.confirm("target='_blank'>").readUntil("</a>")
		p.author = "<![CDATA[%s]]>"%vis.confirm("<td width=90><a href='/browse/listwriter.asp").confirm("target=_blank>").readUntil("</a>")
		size = vis.confirm("<td width=55><font size='-1'>").readUntil("</font>")
		p.text = p.text + "(%s)"%size
		p.title = p.text
		pubDate =  vis.confirm("<td width=90><font size='-1'>").readUntil("</font>")
		try:
			p.pubDate = datetime.datetime(*(time.strptime(pubDate,"%m-%d %H:%M")[0:6]))
		except:
			p.pubDate = datetime.datetime.now()
		posts.append(p)
	return posts

def tianyaRss():
	url= "http://www.tianya.cn/new/publicforum/PageDefault.asp?idWriter=0&Key=0"
	html = httpGet(url,"gbk")
	posts = html2post(html)
	info=Obj()
	info.title="天涯社区"
	info.site="<![CDATA[%s]]>"%url
	info.desc="最新论题"
	rss = toRss(info, posts)
	return rss
	
	
	
def 	httpGet(url,encoding):
	# return a sample for test
	h={"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6"}
	c=urlfetch.fetch(url,headers=h).content
	return c.decode(encoding,"ignore").encode("utf8")
	import urllib2
	f = urllib2.urlopen(url)
	return f.read().decode(encoding).encode("utf8")
	return """<HTML>sample!!!"""
	
if __name__=="__main__":
	print tianyaRss()
