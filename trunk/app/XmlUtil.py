from xml.parsers import expat


def getXMLTree(xml):
	t = XmlTree(None)
	_getTreeObj(xml, XmlVisitor(t))
	return t

class XmlTree:
	def __init__(self, p):
		self._parent=p
		self._cdata=None
	def __eq__(self,other):
		return self._cdata==other
	def __str__(self):
		return self._cdata.__str__()


def _getTreeObj(s,vis):
	p = expat.ParserCreate()
	p.StartElementHandler = vis.tag_start
	p.CharacterDataHandler = vis.tag_cdata
	p.EndElementHandler = vis.tag_end
	p.ordered_attributes = True
	p.buffer_text = True
	p.Parse(s, True)

class XmlVisitor:
	def __init__(self, o):
		self.o=o
	def tag_start(self, name, attributes):
		sub=XmlTree(self.o)

		if not hasattr(self.o, name):
			setattr(self.o, name, [sub])
		else :
			x = getattr(self.o, name)
			if type(x)==list:
				x.append(sub)
			else: # combine with attribute
				setattr(self.o, name, [x,sub])
		if attributes:
			sub._attrcnt=len(attributes)
		for x in range(0,len(attributes), 2):
			setattr(sub, attributes[x],attributes[x+1])
		self.o=sub
	def tag_cdata(self, data):
		data=data.strip()
		if not data:return
		setattr(self.o,"_cdata",data)
	def tag_end(self, name):
		self.o = self.o._parent

if __name__=="__main__":
	fn="C:/tmp/eve-skills2.xml"
	s=open(fn,"rb").read()
	#print(len(s))
	t1=getXMLTree(s)
	print(t1.skills[0].c[0].n)
