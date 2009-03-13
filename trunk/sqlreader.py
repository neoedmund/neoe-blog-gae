# coding:utf-8
# old blog content reader from dump of mysql table from b2evo
# datetime, title, user, text, 
#   5         14     n     13
import gblog
import time
USER="neoedmund@gmail.com"
def run():
	recs = []
	for line in file("etc/blog.txt"):
		recs.extend(parse(line))
	print "size ", len(recs)
	#outputBlogger(recs)
	#outputRSS(recs)
	#outputPost(recs)
def outputPost(posts):
	import httplib, urllib, time
	#site = "neoe-blog.appspot.com"
	site = "localhost:8080"
	print "add to ", site
	idx=0
	for p in posts[idx:]:
		retry=5
		ok=False
		text = p[13].replace("\\n","\n").replace("\\r","").replace("\n\n","\n").replace('\\"','"').replace("\\'","'").replace("\n","<BR>")
		while retry>0:
			retry-=1			
			params = urllib.urlencode({'a': 1, 'title': p[14], 'author': "neoed",
				'cat':"neoe", "pass":"p", "text":text, "pubDate":p[5]})
			headers = {"Content-type": "application/x-www-form-urlencoded",
				   "Accept": "text/plain"}
			conn = httplib.HTTPConnection(site)
			conn.request("POST", "/", params, headers)
			response = conn.getresponse()					
			data = response.read()
			print idx, response.status, response.reason
			conn.close()
			if response.status==200 and data.startswith("added"):
				ok=True
				break
		if not ok:
			print "stop at ", idx
			raise Exception("cannot post %d"%idx)
		idx+=1
	print "finish at ", idx	
		
		
def outputRSS(posts):
	t = []
	t.append("""<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:admin="http://webns.net/mvcb/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel><title>neoedmund's blog</title><link>http://blog-neoedmund.appspot.com/</link>
<description>neoedmund</description>""")
	for p in posts[:3]:
		title=p[14]
		postid="111"
		date822=time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.strptime(p[5],"%Y-%m-%d %H:%M:%S"))
		text = p[13].replace("\\n","\n").replace("\\r","").replace("\n\n","\n").replace('\\"','"').replace("\\'","'")
		content=text
		t.append("""<item><title>%s</title>
<link>http://blog-neoedmund.appspot.com/p=%s</link>
<pubDate>%s</pubDate>
<dc:creator>neoedmund</dc:creator>
<category domain="main">neoe</category>
<description>%s</description></item>""" % (title, postid, date822, content))
	t.append("</channel></rss>")	
	open("c:/tmp/blog.rss", "wb").write("\n".join(t))
def outputBlogger(posts):	
	gb = gblog.BloggerExample(USER, readPassword())	
	idx=10
	for p in posts[idx:]:
		t = chgDateFmt (p[5])
		print "posting #%d at %s"% (idx,t)
		idx +=1				
		#"2003-12-13T18:30:02+01:00
		text = p[13].replace("\\n","\n").replace("\\r","").replace("\n\n","\n").replace('\\"','"').replace("\\'","'")
		ret = gb.CreatePost(p[14],text,"neoe", False, t)
		
	
def chgDateFmt(t):
	x = t.index(" ")
	if x<0: raise Exception("bad format "+t)
	t = t[0:x]+"T"+t[x+1:]+"+08:00"
	return t
def parse(line):
	pos = line.index("VALUES")
	if pos<0:
		print "values not found"
		return
	pos += 7
	p =pos
	recs=[]
	while 1:		
		p=confirm(line,p,"(")
		rec=[]
		while 1:			
			if line[p]=="'":
				word,p =readWord(line,p+1,"'")
				rec.append(word)				
			else:
				word,p =readWord(line,p,",")
				rec.append(word)
				p-=1
			if line[p]==")":
				recs.append(list(rec))
				p+=1
				break
			else:	
				p=confirm(line,p,",")
				
		if line[p]==";":
			#push2(recs)
			break
		else:
			p=confirm(line,p,",")

	return recs		
			
def readWord(line, p, ch):
	w=[]
	while 1:
		if line[p]==ch or (ch=="," and line[p]==")"):
			p +=1		
			break
		if line[p]=="\\":
			w.append(line[p]+line[p+1])
			p+=2
		else:
			w.append(line[p])
			p+=1
	return "".join(w), p

def confirm(line,p,ch):
	if line[p]==ch:
		return p+1
	else:
		raise Exception("expected at %d %s but got %s"%(p,ch,line[p]))

def readPassword():
	from getpass import getpass
	return getpass("pass:")
def gbDeleteAll():
	gb = gblog.BloggerExample(USER, readPassword())
	feed = gb.service.GetFeed('/feeds/' + gb.blog_id + '/posts/default')
	print "["+gb.blog_id+"]"
	# Print the results.

	for entry in feed.entry:
		print entry.title.text
		gb.service.Delete(entry.GetEditLink().href)
#gbDeleteAll()
run()

