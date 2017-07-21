from abc import ABCMeta, abstractmethod
import heapq


class Decorator():
	#### Decorator Interface

	__metaclass__ = ABCMeta

	@abstractmethod
	def setText(self): pass


	@abstractmethod
	def decorate(self): pass

class HtmlDecorator(Decorator):
	#### General html decorator. Able to have the simple ability to add front and back tag

	def __init__(self):
		# super(HtmlDecorator, self).__init__()
		self.text = ""
		self.tag = ""
		self.frontTag = None
		self.endTag = None

	def setText(self, t):
		self.text = t 

	def setTag(self, tag):
		self.tag = tag

	def decorate(self):
		self.frontTag = "<"+self.tag+">"
		self.endTag = "</"+self.tag+">"
		return self.frontTag + self.text + self.endTag


class HtmlEntityDecorator(HtmlDecorator):
	#### Entity decorator inheritated from Html decorator. Add simple front and back tag

	def __init__(self):
		super(HtmlEntityDecorator, self).__init__()
		self.setTag('strong')



class HtmlLinkDecorator(HtmlDecorator):
	#### Link Decorator inheritated from Html decorator. Add <a> tag and href="url" in the front tag. decorate() overwritten

	def __init__(self):
		super(HtmlLinkDecorator, self).__init__()
		self.setTag('a')

	def decorate(self):
		self.frontTag = '<'+self.tag+' href="'+self.text+'">'
		self.endTag = '</'+self.tag+'>'
		return self.frontTag + self.text + self.endTag

class HtmlUsernameDecorator(HtmlDecorator):
	#### Link Decorator inheritated from Html decorator. Add <a> tag and href="http://twitter.com/username" in the front tag. decorate() overwritten
	def __init__(self):
		super(HtmlUsernameDecorator, self).__init__()
		self.setTag('a')

	def decorate(self):
		self.text = self.text[1:]
		self.frontTag = '@ <'+self.tag+' href="http://twitter.com/'+self.text+'">'
		self.endTag = '</'+self.tag+'>'
		return self.frontTag + self.text + self.endTag


class Element(object):
	#### Super class for all elements

	def __init__(self):
		self.fullText = None
		self.text = None
		self.start = None
		self.end = None
		self.decorator = None


	def setFullText(self, ft):
		self.fullText = ft

	def setText(self, t):
		self.text = t

	def setStart(self, s):
		if self.end and s > self.end:
			raise IndexError('start should be smaller than end, it is now larger')
			pass
		else:
			self.start = s 

	def setEnd(self, e):
		if self.start and e < self.start:
			raise IndexError('end should be larger than start, it is now smaller')
			pass
		else:
			self.end = e 

	def setDecorator(self, d):
		self.decorator = d

	def decorate(self):
		self.decorator.setText(self.text)
		return self.decorator.decorate()

	def checkRange(self):
		if self.start is None:
			raise TypeError('start is Nonetype (not yet set)')
		elif self.end is None:
			raise TypeError('end is Nonetype (not yet set)')
		elif self.start < 0 or self.start > len(self.fullText):
			raise IndexError('start is out of range')
		elif self.end < 0 or self.end > len(self.fullText):
			raise IndexError('end is out of range')
		elif self.end < self.start:
			raise IndexError('end is smaller than start')
		else:
			return True


class Entity(Element):
	#### Inheritate from Element. Values set and rules check in constrution. 
	
	def __init__(self, originalText, start, end):

		super(Entity, self).__init__()
		self.setFullText(originalText)
		self.setStart(start)
		self.setEnd(end)
		self.checkRange()

		self.setText(self.fullText[self.start:self.end])

		d = HtmlEntityDecorator()
		self.setDecorator(d)

class Username(Element):
	#### Inheritate from Element. Values set and rules check in constrution. Add method checkAt() to check the legimacy of the input
	
	def __init__(self, originalText, start, end):

		super(Username, self).__init__()
		self.setFullText(originalText)
		self.setStart(start)
		self.setEnd(end)
		self.checkRange()
		self.checkAt()

		self.setText(self.fullText[self.start:self.end])
		
		d = HtmlUsernameDecorator()
		self.setDecorator(d)

	def checkAt(self):
		if self.fullText[start:start+1] != '@':
			raise ValueError('The username does not start with "@"')


class Link(Element):
	#### Inheritate from Element. Values set and rules check in constrution. 
	
	def __init__(self, originalText, start, end):

		super(Link, self).__init__()
		self.setFullText(originalText)
		self.setStart(start)
		self.setEnd(end)
		self.checkRange()

		self.setText(self.fullText[self.start:self.end])
		
		d = HtmlLinkDecorator()
		self.setDecorator(d)


class ProccessedTweet(object):
	#### Assumed input object

	def __init__(self):
		self.fullText = None
		self.elements = list()

	def setFullText(self, t):
		self.fullText = t

	def appendElement(self, start, end, tp):
		heapq.heappush(self.elements, (start, end, tp))

	def popFrontElement(self):
		return heapq.heappop(self.elements)




if __name__ == "__main__":
	
	input = ProccessedTweet()
	input.setFullText("Obama visited Facebook headquarters: http://bit.ly/xyz @elversatile")
	input.appendElement(14,22,'Entity')
	input.appendElement(0,5,'Entity')
	input.appendElement(55,67,'Username')
	input.appendElement(37,54, 'Link')

	output = ""
	ptr = 0

	while input.elements:
		start, end, e = input.popFrontElement()

		if ptr>start:
			raise IndexError('Elements are overlapping one another')

		inbetween = input.fullText[ptr:start]
		ptr = end
		if e == "Entity":
			new = Entity(input.fullText, start, end)
		elif e == "Username":
			new = Username(input.fullText, start, end)
		elif e == "Link":
			new = Link(input.fullText, start, end)
		else:
			raise TypeError("There's an undefined type '"+ e +"'")

		output = output + inbetween + new.decorate()

	if ptr < len(input.fullText):
		output += input.fullText[ptr:]

	print output




