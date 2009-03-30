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
import httplib, urllib
import logging
from XmlUtil import getXMLTree
from google.appengine.api.urlfetch import fetch
from urllib import quote_plus
import simplejson as json

implpaths=[#"/char/WalletJournal",\
		"/char/WalletTransactions","/char/SkillQueue","/char/IndustryJobs","/char/MarketOrders"]
def html2post(xml,path,cid):
	t=getXMLTree(xml)
	posts=[]
	cnt=0
	if not hasattr(t.eveapi[0],"result"):
		logging.debug(xml[:200])
		return []
	if path=="/char/IndustryJobs":
		#mycat='IndustryJobs.%s'%cid
		#query = Story.all().filter('xcat =', mycat)
		#oldkeys=[]
		#oldvalues=[]
		#for row in query.fetch():
		#	oldkeys.append(row.xkey)
		#	oldvalues.append(row.xvalue)
		for r in t.eveapi[0].result[0].rowset[0].row:
			newvalue='jobID="%s" assemblyLineID="%s" containerID="%s" installedItemID="%s" installedItemLocationID="%s" installedItemQuantity="%s" installedItemProductivityLevel="%s" installedItemMaterialLevel="%s" installedItemLicensedProductionRunsRemaining="%s" outputLocationID="%s" installerID="%s" runs="%s" licensedProductionRuns="%s" installedInSolarSystemID="%s" containerLocationID="%s" materialMultiplier="%s" charMaterialMultiplier="%s" timeMultiplier="%s" charTimeMultiplier="%s" installedItemTypeID="%s" outputTypeID="%s" containerTypeID="%s" installedItemCopy="%s" completed="%s" completedSuccessfully="%s" installedItemFlag="%s" outputFlag="%s" activityID="%s" completedStatus="%s" installTime="%s" beginProductionTime="%s" endProductionTime="%s" pauseProductionTime="%s"'\
			    %(r.jobID, r.assemblyLineID, r.containerID, r.installedItemID, r.installedItemLocationID, r.installedItemQuantity, r.installedItemProductivityLevel, r.installedItemMaterialLevel, r.installedItemLicensedProductionRunsRemaining, r.outputLocationID, r.installerID, r.runs, r.licensedProductionRuns, r.installedInSolarSystemID, r.containerLocationID, r.materialMultiplier, r.charMaterialMultiplier, r.timeMultiplier, r.charTimeMultiplier, r.installedItemTypeID, r.outputTypeID, r.containerTypeID, r.installedItemCopy, r.completed, r.completedSuccessfully, r.installedItemFlag, r.outputFlag, r.activityID, r.completedStatus, r.installTime, r.beginProductionTime, r.endProductionTime, r.pauseProductionTime)
			#newfeed=XFeed(xkey=newkey, xvalue=newvalue, xcat=mycat)
			#newfeed.put()
			p=Obj()
			p.cat = path
			p.link = ""
			p.text = newvalue
			p.pubDate = datetime.datetime(*(time.strptime(r.beginProductionTime,"%Y-%m-%d %H:%M:%S")[0:6]))
			p.author = "eve"
			p.title ="IndustryJobs: ID %s runs:%s (%s-%s),completed=%s,completedStatus=%s" % (r.jobID, r.runs, r.beginProductionTime, r.endProductionTime,r.completed, r.completedStatus)
			posts.append(p)
			cnt+=1
			if cnt>20:break


	elif path=="/char/MarketOrders":
		typeids=[]
		for r in t.eveapi[0].result[0].rowset[0].row:
			typeids.append(r.typeID)
			cnt+=1
			if cnt>20:break			
		cnt=0	
		typeNameMap=getTypeNameMap(typeids)
		for r in t.eveapi[0].result[0].rowset[0].row:
			s  = 'orderID="%s" charID="%s" stationID="%s" volEntered="%s" volRemaining="%s" minVolume="%s" orderState="%s" typeID="%s" range="%s" accountKey="%s" duration="%s" escrow="%s" price="%s" bid="%s" issued="%s"'\
			    %(r.orderID, r.charID, r.stationID, r.volEntered, r.volRemaining, r.minVolume, r.orderState, r.typeID, r.range, r.accountKey, r.duration, r.escrow, r.price, r.bid, r.issued)
			p=Obj()
			p.cat = path
			p.link = ""
			p.text = s
			p.pubDate = datetime.datetime(*(time.strptime(r.issued,"%Y-%m-%d %H:%M:%S")[0:6]))
			p.author = "eve"
			p.title ="MarketOrders: orderID=%s,typeID=%s(%s),vol=%s/%s" \
			    % (r.orderID, r.typeID, typeNameMap[int(r.typeID)], r.volRemaining, r.volEntered)
			if  int(r.duration<=1):
				p.title ="[expiring]"+p.title
			posts.append(p)
			cnt+=1
			if cnt>20:break
	else:
		for r in t.eveapi[0].result[0].rowset[0].row:
			if path=="/char/WalletJournal":
				key="WalletJournal.%s.%s"%(cid, r.refID)
				#if existed(key):continue
				s='date="%s" refID="%s" refTypeID="%s" ownerName1="%s" ownerID1="%s" ownerName2="%s" ownerID2="%s" argName1="%s" argID1="%s" amount="%s" balance="%s" reason="%s"' \
				   %(r.date, r.refID, r.refTypeID, r.ownerName1, r.ownerID1, r.ownerName2, r.ownerID2, r.argName1, r.argID1, r.amount, r.balance, r.reason)
				p=Obj()
				p.cat = path
				p.link = ""
				p.text = s
				p.pubDate = datetime.datetime(*(time.strptime(r.date,"%Y-%m-%d %H:%M:%S")[0:6]))
				p.author = "eve"
				p.title = "WalletJournal: %s" %r.amount
				posts.append(p)
			elif path=="/char/WalletTransactions":
				key="WalletTransactions.%s.%s"%(cid, r.transactionID)
				#if existed(key):continue
				s='transactionDateTime="%s" transactionID="%s" quantity="%s" typeName="%s" typeID="%s" price="%s" clientID="%s" clientName="%s" stationID="%s" stationName="%s" transactionType="%s" transactionFor="%s"' \
				    %(r.transactionDateTime, r.transactionID, r.quantity, r.typeName, r.typeID, r.price, r.clientID, r.clientName, r.stationID, r.stationName, r.transactionType, r.transactionFor)
				p=Obj()
				p.cat = path
				p.link = ""
				p.text = s
				p.pubDate = datetime.datetime(*(time.strptime(r.transactionDateTime,"%Y-%m-%d %H:%M:%S")[0:6]))
				p.author = "eve"
				p.title = "WalletTransactions: %s" %"%s %s * %s at isk %s" % (r.transactionType, r.typeName, r.quantity, r.price)
				posts.append(p)
			elif path=="/char/SkillQueue":
				key="SkillQueue.%s.%s.%s.%s"%(cid, r.typeID,r.level,r.startSP )
				#if existed(key):continue
				s='queuePosition="%s" typeID="%s" level="%s" startSP="%s" endSP="%s" startTime="%s" endTime="%s"' \
				    %(r.queuePosition, r.typeID, r.level, r.startSP, r.endSP, r.startTime, r.endTime)
				p=Obj()
				p.cat = path
				p.link = ""
				p.text = s
				p.pubDate = datetime.datetime(*(time.strptime(r.startTime,"%Y-%m-%d %H:%M:%S")[0:6]))
				p.author = "eve"
				p.title ="SkillQueue: %s" % "%s lv %s (%s-%s)" % (r.typeID, r.level, r.startTime, r.endTime)
				posts.append(p)
			else:
				logging.debug("unkown path:%s" % path)
				break
			cnt+=1
			if cnt>20:break

	return posts
def getTypeNameMap(typeids):
	m={}
	if len(typeids)==0:return m
	gql="SELECT * FROM eve_invTypes where typeID in (%s)"%(",".join(typeids))	
	logging.debug("query %s"%gql)
	resp=fetch("http://neoe-table.appspot.com/a?i=%s"%quote_plus(gql))
	if resp.status_code==200:
		o=json.loads(resp.content)
		if o[0]=="0":
			r=o[3]
			p1=r[0].index('typeID')
			p2=r[0].index('typeName')
			for x in r[1:]:
				m[int(x[p1])]=x[p2]
	else: logging.debug("errorcode:%s"%(resp.status_code))
	return m
class XFeed(db.Model):
	xkey = db.StringProperty()
	xvalue = db.StringProperty()
	xcat = db.StringProperty()

class RssFeed(db.Model):
	data = db.StringProperty()

def existed(key):
	feed=RssFeed.gql("WHERE data = :1 ", key).get()
	if feed:
		logging.debug("existed:%s" % key)
		return True
	else:
		feed=RssFeed(data=key)
		feed.put()
		logging.debug("new:%s" % key)
		return False

def rss(cid, uid, k):
	posts=[]
	for path in implpaths:
		posts.extend(getposts(cid, uid, k,path))
	info=Obj()
	info.title="EVE API Data of %s" %(uid)
	info.site="http://www.eveonline.com/api"
	info.desc=info.title
	rss = toRss(info, posts)
	return rss
def getposts(cid, uid, k, path):
	if path not in implpaths: return []
	params = urllib.urlencode({'characterID':cid, 'userid': uid, 'apikey': k})
	headers = {"Content-type": "application/x-www-form-urlencoded",
	           "Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.eve-online.com:80")
	conn.request("POST", "%s.xml.aspx"%path, params, headers)
	response = conn.getresponse()
	#print response.status, response.reason
	if response.status!=200:
		posts=[]
		logging.debug("response.status(%s)"%response.status)
	else:
		data = response.read()
		conn.close()
		posts = html2post(data, path, cid)
	return posts



if __name__=="__main__":
	print rss("","","")
