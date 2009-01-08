#coding=UTF-8
#
import cgi
import datetime
import wsgiref.handlers
import time

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

import icons

class Post(db.Model):
	pubDate = db.DateTimeProperty(auto_now_add=True)
	author = db.StringProperty()
	title=db.StringProperty()
	cat = db.StringProperty()	
	text = db.TextProperty()

htmlhead="""<html><head><title>neoe-blog@gae</title>
<link rel="alternate" type="application/rss+xml" title="neoedmund Blog - RSS" href="http://neoe-blog.appspot.com/?rss=1" />
<style id='page-skin-1' type='text/css'><!--
body {
margin:10;
font:normal normal 73% Verdana, sans-serif;
background:#ffffff;
color:#000000;
}
a:link {
color:#5588aa;
text-decoration:none;
}
a:visited {
color:#999999;
text-decoration:none;
}
a:hover {
color:#000000;
text-decoration:underline;
}
a img {
border-width:0;
}
#outer-wrapper {
margin-top: 0px;
margin-right: 3em;
margin-bottom: 0;
margin-left: 3em;
}
h1 {
border-bottom:dotted 1px #999999;
margin-bottom:0px;
color: #000000;
font: normal bold 162% Georgia,Serif;
}
h1 a, h1 a:link, h1 a:visited {
color: #000000;
}
h2 {
margin:0px;
padding: 0px;
}
#main .widget {
padding-bottom:10px;
margin-bottom:20px;
border-bottom:dotted 1px #999999;
clear: both;
}
#main .Header {
border-bottom-width: 0px;
}
.date-header {
padding-top:15px;
color:#555555;
padding-bottom:0px;
margin-bottom:0px;
font-size: 90%;
}
.post-title {
font-size: 140%;
font-weight: bold;
color: green;
}
.post {
padding-left:5%;
padding-right:10%;
}
.xauthor {
color:#555555;
font-style: italic;
}
.xcat {
color:#555555;
font-weight: bold;
}

.copyright {
text-align: right;
color:green;
font-size: 70%;
}


--></style></head><body>
<h1><a href="/">neoedmund</a>&#160;
<a href="/?rss=1"><img src="/rss16.png" height=16 width=16></img></a></h1>"""
htmlfoot="""<div class="copyright">(C)2009 neoedmund</div></html>"""
class MainPage(webapp.RequestHandler):
	def post(self): self.get()
	def get(self):
		if self.req("a")=="1":
			self.addPost()
		elif self.req("rss")=="1":
			self.rss()
		elif self.req("w")=="1":
			self.postPage()
		elif len(self.req("p"))>0:
			self.showPost(self.req("p"))
		elif self.req("icon")=="1":
			self.showIcon()
		else:
			self.showPagedPosts()
	def showIcon(self):
		k=self.req("k")
		name=icons.getName(hash(k))
		self.redirect(name)
	def showPagedPosts(self):
		offset = 0
		count = 10
		x=self.request.get('offset')
		if x: offset=int(x)
		x=self.request.get('count')
		if x: count=int(x)
		offset1=offset-count
		if offset1<0 :offset1=0
		offset2=offset+count
		t = []
		t.append(htmlhead)
		t.append('''<script>
function prev(){
	document.xform.offset.value=document.xform.offset1.value
	document.xform.submit()
}
function next(){
	document.xform.offset.value=document.xform.offset2.value
	document.xform.submit()
}
</script>
<p><a href="javascript:prev(%d)">&lt;&lt;newer</a>&#160;&#160;&#160;
<a href="javascript:next(%d)">older&gt;&gt;</a><br>
<form action="/" method="get" name=xform>
<input type=hidden name=offset value=%d><input type=hidden name=count value=%d>
<input type=hidden name=offset1 value=%d><input type=hidden name=offset2 value=%d>''' 
% (offset1, offset2,offset, count, offset1, offset2))
		posts = db.GqlQuery("SELECT * "
				"FROM Post "
				"ORDER BY pubDate DESC LIMIT %s,%s"%(offset,count))
		for p in posts:
			t.append(self.getPostHtml(p))
		t.append("""<p><a href="javascript:prev(%d)">&lt;&lt;newer</a>&#160;&#160;&#160;
<a href="javascript:next(%d)">older&gt;&gt;</a><br>"""%(offset1, offset2))
		t.append("""<a href="http://www4.clustrmaps.com/user/1e76c8bf"><img src="http://www4.clustrmaps.com/stats/maps-no_clusters/neoe-blog.appspot.com-thumb.jpg" alt="Locations of visitors to this page" /></a>""")
		t.append(htmlfoot)
		self.resp("".join(t))	
		
	def postPage(self):
		t=[]
		p = None
		if self.req("p"):
			p = db.get(self.req("p"))
			if not p : return
		t.append(htmlhead)
		if users.get_current_user():
			author=users.get_current_user().nickname()			
		else:
			author=""			
		if p:
			param = (p.title, p.author, p.cat, p.text)
		else:
			param = ("", author, "", "")
		t.append("""
<form method=post>
<input type=hidden name=a value=1>
title:<input type=text name=title value='%s'>
author:<input type=text name=author value='%s'>
catalog:<input type=text name=cat value='%s'>
pass:<input type=password name=pass>
content:<br><textarea cols=120 rows=20 name=text>%s</textarea>
<BR>
<input type=checkbox name=autoBR value=1>autoBR&#160;&#160;
<input type=submit>
"""%param)
		if p:
			t.append("<input type=hidden name=p value='%s'>"% p.key())
		t.append(htmlfoot)
		self.resp("".join(t))	
		
	def getPostHtml(self, p):
		return """<p class=post-title><img src="%s"></img>%s<a href="/?p=%s"><img src="/open.png"></img></a></p>
<span class=xauthor>%s</span>&#160;&#160;&#160;<span class=date-header>%s</span>&#160;&#160;&#160;<span class=xcat>%s</span>
<p class=post>%s</p>"""%(icons.getName(p.key().id()), p.title,p.key(),p.author,p.pubDate.strftime("%a, %d %b %Y %H:%M:%S +0000"),p.cat,p.text)

	def showPost(self,key):
		p = db.get(key)
		t=[]
		if p:
			t.append(htmlhead)
			t.append(self.getPostHtml(p))
			t.append(htmlfoot)
		self.resp("".join(t))	
		
	def addPost(self):
		req = self.req
		if req("pass")!="p":return
		if req("p"):
			p = db.get(req("p"))
			if not p :return
		else:
			p=Post()
		if req("pubDate"): 
			p.pubDate=datetime.datetime(*(time.strptime(req("pubDate"),"%Y-%m-%d %H:%M:%S")[0:6]))
		p.author = req("author")
		p.title=req("title")
		p.cat = req("cat")
		text = req("text")
		if req("autoBR"):
			text = text.replace("\n","\n<BR>")
		p.text=text
		p.put()
		db.put(p)
		self.resp("".join(["added or updated, <a href='/?p=%s'>view</a>"%(p.key())]))	
		
	def rss(self):
		posts = db.GqlQuery("SELECT * "
				"FROM Post "
				"ORDER BY pubDate DESC LIMIT %s,%s"%(0,5))
		t = []
		#site = "http://localhost:8080"
		site = "http://neoe-blog.appspot.com"
		t.append("""<?xml version="1.0" encoding="UTF-8" ?><rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel><title>neoedmund's blog</title><link>%s/</link>
<description>neoedmund</description>""" % site)
		for p in posts:
			text = p.text
			if len(text)>150:
				text = text[:150]+" ... "
			t.append("""<item><title>%s</title>
<link>%s/?p=%s</link>
<pubDate>%s</pubDate>
<dc:creator>%s</dc:creator>
<category>%s</category>
<description><![CDATA[%s]]></description></item>""" % (p.title, site, p.key(), 
p.pubDate.strftime("%a, %d %b %Y %H:%M:%S +0000"),p.author,p.cat,text))
		t.append("</channel></rss>")
		self.response.headers['content-type']="application/xml"
		self.response.headers['content-encoding']="UTF-8"
		self.resp("".join(t).encode("utf8"))
		
	def req(self,k): return self.request.get(k)
	def resp(self, t):self.response.out.write(t)
		
	


application = webapp.WSGIApplication([
	('/', MainPage),
], debug=True)


def main():
	wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
	main()
