from WriterCpp import WriterCpp
from WriterCpp import SERIALIZATION
from WriterCpp import DESERIALIZATION
from WriterCpp import FLAG_HPP
from WriterCpp import FLAG_CPP
from Object import Object
from Class import Class


class WriterCppSerializatorXml(WriterCpp):
	def __init__(self, outDirectory, parser, createTests):
		WriterCpp.__init__(self, outDirectory, parser, createTests)

	def create_serialization_patterns(self):
		self.serialize_formats[SERIALIZATION]['simple'] = []
		self.serialize_formats[SERIALIZATION]['simple'].append( 'if({0} != {2}) \n__begin__\n::set(xml,"{0}",{0});\n__end__' )
		self.serialize_formats[SERIALIZATION]['simple'].append( '::set(xml,"{0}",{0});' )
		self.serialize_formats[DESERIALIZATION]['simple'] = []
		self.serialize_formats[DESERIALIZATION]['simple'].append( '''auto attr_{0} = xml.attribute("{0}"); 
																	if(attr_{0}) 
																	{3}
																		{0} = ::get<{1}>(attr_{0});
																	{4}
																	else
																	{3}
																		{0} = {2};
																	{4}''' )
		self.serialize_formats[DESERIALIZATION]['simple'].append( '{0} = ::get<{1}>( xml, "{0}" );' )
		
		self.serialize_formats[SERIALIZATION]['serialized'] = []
		self.serialize_formats[SERIALIZATION]['serialized'].append( 'static_assert(0, "field "{0}" not should have a initialize value");' )
		self.serialize_formats[SERIALIZATION]['serialized'].append( '{0}.serialize(xml.append_child("{0}"));' )
		self.serialize_formats[DESERIALIZATION]['serialized'] = []
		self.serialize_formats[DESERIALIZATION]['serialized'].append( 'static_assert(0, "field "{0}" not should have a initialize value");' )
		self.serialize_formats[DESERIALIZATION]['serialized'].append( '{0}.deserialize(xml.child("{0}"));' )
		
		self.serialize_formats[SERIALIZATION]['pointer'] = []
		self.serialize_formats[SERIALIZATION]['pointer'].append( 'static_assert(0, "field "{0}" not should have a initialize value");' )
		self.serialize_formats[SERIALIZATION]['pointer'].append( '''
																	if({0})
																	{3}
																		auto child = xml.append_child("{0}");
																		child.append_attribute("type").set_value({0}->getType().c_str());
																		{0}->serialize(child);
																	{4}''' )
		self.serialize_formats[DESERIALIZATION]['pointer'] = []
		self.serialize_formats[DESERIALIZATION]['pointer'].append( 'static_assert(0, "field "{0}" not should have a initialize value");' )
		self.serialize_formats[DESERIALIZATION]['pointer'].append( '''
																	auto xml_{0} = xml.child("{0}");
																	if(xml_{0})
																	{3}
																		std::string type = xml_{0}.attribute("type").as_string();
																		{0} = Factory::shared().build<{1}>( type );
																		{0}->deserialize(xml_{0});
																	{4}''')
		
		self.serialize_formats[SERIALIZATION]['list<simple>'] = []
		self.serialize_formats[SERIALIZATION]['list<simple>'].append( 'static_assert(0, "list "{0}" not should have a initialize value");' )
		self.serialize_formats[SERIALIZATION]['list<simple>'].append( '''auto arr_{0} = xml.append_child("{0}");
																		 for( auto& t : {0} )
																		 {3}
																			auto attr = arr_{0}.append_child("{5}").append_attribute("value");
																			set(attr, t);
																		 {4}''' )
		self.serialize_formats[DESERIALIZATION]['list<simple>'] = []
		self.serialize_formats[DESERIALIZATION]['list<simple>'].append( 'static_assert(0, "list "{0}" not should have a initialize value");' )
		self.serialize_formats[DESERIALIZATION]['list<simple>'].append( '''auto arr_{0} = xml.child("{0}");
																		for( auto child : arr_{0} )
																		{3}
																			{0}.emplace_back();
																			{0}.back() = get<{5}>(child, "value");
																		{4}''' )
		
		self.serialize_formats[SERIALIZATION]['serialized_list'] = []
		self.serialize_formats[SERIALIZATION]['serialized_list'].append( 'static_assert(0, "list "{0}" not should have a initialize value");' )
		self.serialize_formats[SERIALIZATION]['serialized_list'].append( '''auto arr_{0} = xml.append_child("{0}");
																		 for( auto& t : {0} )
																		 {3}
																		 	t.serialize(arr_{0}.append_child(t.getType().c_str())); 
																		 {4}''' )
		self.serialize_formats[DESERIALIZATION]['serialized_list'] = []
		self.serialize_formats[DESERIALIZATION]['serialized_list'].append( 'static_assert(0, "list "{0}" not should have a initialize value");' )
		self.serialize_formats[DESERIALIZATION]['serialized_list'].append( '''auto arr_{0} = xml.child("{0}");
																		for( auto child : arr_{0} )
																		{3}
																			{0}.emplace_back();
																			{0}.back().deserialize(child);
																		{4}''' )

		self.serialize_formats[SERIALIZATION]['pointer_list'] = []
		self.serialize_formats[SERIALIZATION]['pointer_list'].append( 'static_assert(0, "list "{0}" not should have a initialize value");' )
		self.serialize_formats[SERIALIZATION]['pointer_list'].append( '''auto arr_{0} = xml.append_child("{0}");
																		 for( auto& t : {0} )
																		 {3}
																			t->serialize(arr_{0}.append_child(t->getType().c_str())); 
																		 {4}''' )
		self.serialize_formats[DESERIALIZATION]['pointer_list'] = []
		self.serialize_formats[DESERIALIZATION]['pointer_list'].append( 'static_assert(0, "list "{0}" not should have a initialize value");' )
		self.serialize_formats[DESERIALIZATION]['pointer_list'].append( '''auto arr_{0} = xml.child("{0}");
																		for( auto child : arr_{0} )
																		{3}
																			auto type = child.name();
																			auto obj = Factory::shared().build<{5}>( type );
																			{0}.emplace_back(obj);
																			{0}.back()->deserialize( child );
																		{4}''' )

		self.simple_types = ["int", "float", "bool", "string", "cc.point"]
		for i in range(2):
			for type in self.simple_types:
				self.serialize_formats[i][type] = []
				self.serialize_formats[i][type].append( self.serialize_formats[i]["simple"][0] )
				self.serialize_formats[i][type].append( self.serialize_formats[i]["simple"][1] )
				list_type = "list<{0}>".format(type)
				self.serialize_formats[i][list_type] = []
				self.serialize_formats[i][list_type].append( self.serialize_formats[i]["list<simple>"][0] )
				self.serialize_formats[i][list_type].append( self.serialize_formats[i]["list<simple>"][1] )

			self.serialize_formats[i]["list<serialized>"] = []
			self.serialize_formats[i]["list<serialized>"].append( self.serialize_formats[i]["serialized_list"][0] )
			self.serialize_formats[i]["list<serialized>"].append( self.serialize_formats[i]["serialized_list"][1] )

	def getSerializationObjectArg(self, serialization_type):
		if serialization_type == SERIALIZATION:
			return ["xml","pugi::xml_node"]
		if serialization_type == DESERIALIZATION:
			return ["xml", "const pugi::xml_node&"]
		return ["", ""]

	def getBehaviorCallFormat(self):
		return "{0}::{1}(xml);"

	def buildMapSerialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):
		key = obj_template_args[0]
		value = obj_template_args[1]
		key_type = key.name if isinstance(key, Class) else key.type
		value_type = value.name if isinstance(value, Class) else value.type
		str = '''
		auto map_{0} = xml.append_child("{0}");
		for( auto pair : {0} )
		__begin__
			auto xml = map_{0}.append_child("pair");
			auto& key = pair.first; {1}
			auto& value = pair.second; {2}
		__end__
		'''
		_value_is_pointer = value.is_pointer
		a0 = obj_name
		a1 = self._buildSerializeOperation("key", key_type, None, False, [], SERIALIZATION)
		a2 = self._buildSerializeOperation("value", value_type, None, _value_is_pointer, [], SERIALIZATION)
		return str.format( a0, a1, a2)
		#a1 = serialize key /simple, serialized
		#a2 = serialize value /simple, serialized, pointer,

	def buildMapDeserialization(self, obj_name, obj_type, obj_value, obj_is_pointer, obj_template_args):	
		key = obj_template_args[0]
		value = obj_template_args[1]
		key_type = key.name if isinstance(key, Class) else key.type
		value_type = value.name if isinstance(value, Class) else value.type
		str = '''
		auto map_{0} = xml.child("{0}");
		for( auto child : map_{0} )
		__begin__
			auto xml = child;
			{3} key; {1}
			{4} value; {2}
			{0}[key] = value;
		__end__
		'''
		_value_is_pointer = value.is_pointer if isinstance(value, Object) else false
		a0 = obj_name
		a1 = self._buildSerializeOperation("key", key_type, None, False, [], DESERIALIZATION)
		a2 = self._buildSerializeOperation("value", value_type, None, _value_is_pointer, [], DESERIALIZATION)
		a3 = key_type
		a4 = value_type
		if value.is_pointer:
			a4 = "IntrusivePtr<{}>".format(value_type)
		return str.format( a0, a1, a2, a3, a4 )
