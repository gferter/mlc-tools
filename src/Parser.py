from Object import Object
from Class import Class
from Function import Function
from  WriterCpp import WriterCpp
from  WriterJava import WriterJava

def throw_error( msg ):
	print msg
	exit(-1)

class Parser:
	def __init__(self):
		self.classes=[]
		self.objects=[]
		self.functions=[]
		return
	
	def parse(self, text):
		text = text.strip()
		while len(text) > 0:
			text = text.strip()
			if self._is_class(text):
				text = self._createClass(text)
			elif self._is_functon(text):
				text = self._createFunction(text)
			else:
				text = self._createDeclaration(text)

		self._find_dependences()
	
	def _is_class(self,line):
		return line.strip().find("class") == 0
	def _is_functon(self,line):
		return line.strip().find("function") == 0
	
	def _findBody(self, text):
		text = text.strip()
		body = ""
		header = text[0:text.find("\n")]
		if header.find(":external") == -1:
			text = text[text.find("{"):]
			counter = 0
			index = 0
			for ch in text:
				index += 1
				if counter == 0 and ch == '{':
					counter += 1
					continue
				if ch == '{':
					counter += 1
				if ch == '}':
					counter -= 1
				if counter == 0:
					text = text[index:]
					break
				body += ch
		else:
			text = text[len(header):].strip()
		return body, header, text
	def _createClass(self, text):
		body, header, text = self._findBody(text)
		cls = Class()
		cls.parse(header)
		cls.parseBody( Parser(), body )
		self.classes.append(cls)
		return text

	def _createDeclaration(self, text):
		lines = text.split("\n")
		line = lines[0]
		if len(lines) > 1:
			text = text[text.find("\n")+1:]
		else:
			text = ""
		obj = Object()
		obj.parse(line)
		self.objects.append(obj)
		return text

	def _createFunction(self, text):
		body, header, text = self._findBody(text)
		function = Function()
		function.parse(header)
		function.parseBody(body)
		self.functions.append(function)
		return text

	def _findClass(self, name):
		for cls in self.classes:
			if cls.name == name:
				return cls
		return None

	def _find_dependences(self):
		for cls in self.classes:
			if cls.is_visitor and self.getVisitorType(cls) != cls.name:
				if cls.name.find( "IVisitor" ) != 0:
					self.createVisitor(cls)

			behaviors = []
			for name in cls.behaviors:
				c = self._findClass(name)
				if c == None:
					throw_error( "cannot find behavior class: {0}<{1}>".format(cls.name, name) );
				behaviors.append( c )
			cls.behaviors = behaviors
			cls.is_serialized = self.isSerialised(cls)
			cls.is_visitor = self.isVisitor(cls)
			if cls.is_visitor and cls.name != self.getVisitorType(cls):
				self.appendVisitor(cls)

	def isSerialised(self, cls):
		if cls.is_serialized:
			return True
		is_seriazed = False
		for c in cls.behaviors:
			is_seriazed = is_seriazed or self.isSerialised(c)
		return is_seriazed

	def isVisitor(self, cls):
		if cls.is_visitor:
			return True
		is_visitor = False
		for c in cls.behaviors:
			is_visitor = is_visitor or self.isVisitor(c)
		return is_visitor

	def isFunctionOverride(self, cls, function):
		for c in cls.behaviors:
			for f in c.functions:
				if f.name == function.name and f.return_type == function.return_type and f.args == function.args:
					return True
		is_override = False
		for c in cls.behaviors:
			is_override = is_override or self.isFunctionOverride(c, function)
		return is_override

	def getVisitorType(self, cls):
		if not cls.is_visitor:
			return None

		if cls.name.find( "IVisitor" ) == 0:
			return cls.name

		for c in cls.behaviors:
			if not isinstance(c, Class):
				return "IVisitor" + cls.name
			if c.is_visitor:
			    return self.getVisitorType(c)
		return "IVisitor" + cls.name

	def createVisitor(self, cls):
		visitorName = self.getVisitorType(cls)
		visitor = self._findClass( visitorName )
		if visitor == None:
			visitor = Class()
			visitor.name = visitorName
			visitor.type = "class"
			visitor.is_abstract = True
			visitor.is_visitor = True
			self.classes.append( visitor )

	def appendVisitor(self, cls):
		visitorName = self.getVisitorType(cls)
		visitor = self._findClass( visitorName )
		function = Function()
		function.name = "visit"
		function.return_type = "void"
		function.args.append(["ctx", cls.name + "*"])
		visitor.functions.append(function)
		
