cpp_xml = '''
#int
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    xml.append_attribute("$(FIELD)").set_value($(FIELD));
}
#without default value:
xml.append_attribute("$(FIELD)").set_value($(FIELD));

#deserialize:
#with default value:
$(FIELD) = xml.attribute("$(FIELD)").as_int($(DEFAULT_VALUE));
#without default value:
$(FIELD) = xml.attribute("$(FIELD)").as_int();


#bool
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    xml.append_attribute("$(FIELD)").set_value($(FIELD));
}
#without default value:
xml.append_attribute("$(FIELD)").set_value($(FIELD));

#deserialize:
#with default value:
$(FIELD) = xml.attribute("$(FIELD)").as_bool($(DEFAULT_VALUE));
#without default value:
$(FIELD) = xml.attribute("$(FIELD)").as_bool();


#float
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    xml.append_attribute("$(FIELD)").set_value($(FIELD));
}
#without default value:
xml.append_attribute("$(FIELD)").set_value($(FIELD));

#deserialize:
#with default value:
$(FIELD) = xml.attribute("$(FIELD)").as_float($(DEFAULT_VALUE));
#without default value:
$(FIELD) = xml.attribute("$(FIELD)").as_float();


#string
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    xml.append_attribute("$(FIELD)").set_value($(FIELD).c_str());
}
#without default value:
xml.append_attribute("$(FIELD)").set_value($(FIELD).c_str());

#deserialize:
#with default value:
$(FIELD) = xml.attribute("$(FIELD)").as_string($(DEFAULT_VALUE));
#without default value:
$(FIELD) = xml.attribute("$(FIELD)").as_string();


#serialized
#serialize:
$(FIELD).serialize(xml.append_child("$(FIELD)"));
#deserialize:
$(FIELD).deserialize(xml.child("$(FIELD)"));


#pointer
#serialize
if($(FIELD))
{
    auto child = xml.append_child("$(FIELD)");
    child.append_attribute("type").set_value($(FIELD)->get_type().c_str());
    $(FIELD)->serialize(child);
}
#deserialize:
auto xml_$(FIELD) = xml.child("$(FIELD)");
if(xml_$(FIELD))
{
    std::string type = xml_$(FIELD).attribute("type").as_string();
    $(FIELD) = Factory::shared().build<$(TYPE)>(type);
    $(FIELD)->deserialize(xml_$(FIELD));
}


#list<int>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto t : $(FIELD))
{
    arr_$(FIELD).append_child("int").append_attribute("value").set_value(t);
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(const auto& child : arr_$(FIELD))
{
    $(FIELD).push_back(child.attribute("value").as_int());
}

#list<bool>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto t : $(FIELD))
{
    arr_$(FIELD).append_child("bool").append_attribute("value").set_value(t);
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(const auto& child : arr_$(FIELD))
{
    $(FIELD).push_back(child.attribute("value").as_bool());
}
#list<float>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto t : $(FIELD))
{
    arr_$(FIELD).append_child("float").append_attribute("value").set_value(t);
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(const auto& child : arr_$(FIELD))
{
    $(FIELD).push_back(child.attribute("value").as_float());
}
#list<string>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(const auto& t : $(FIELD))
{
    arr_$(FIELD).append_child("str").append_attribute("value").set_value(t.c_str());
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(const auto& child : arr_$(FIELD))
{
    $(FIELD).push_back(child.attribute("value").as_string(""));
}

#list<serialized>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto& t : $(FIELD))
{
    t.serialize(arr_$(FIELD).append_child("item"));
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(auto child : arr_$(FIELD))
{
    $(FIELD).emplace_back();
    $(FIELD).back().deserialize(child);
}


#pointer_list
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto& t : $(FIELD))
{
    t->serialize(arr_$(FIELD).append_child(t->get_type().c_str()));
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(auto child : arr_$(FIELD))
{
    auto type = child.name();
    $(FIELD).push_back(Factory::shared().build<$(ARG_0)>(type));
    $(FIELD).back()->deserialize(child);
}


#link
#serialize:
xml.append_attribute("$(FIELD)").set_value($(FIELD)->name.c_str());
#deserialize:
auto name_$(FIELD) = xml.attribute("$(FIELD)").as_string();
$(FIELD) = DataStorage::shared().get<$(TYPE)>(name_$(FIELD));


#list<link>
#serialize:
auto arr_$(FIELD) = xml.append_child("$(FIELD)");
for(auto& t : $(FIELD))
{
    arr_$(FIELD).append_child("data").append_attribute("value").set_value(t->name.c_str());
}
#deserialize:
auto arr_$(FIELD) = xml.child("$(FIELD)");
for(auto& child : arr_$(FIELD))
{
    auto name = child.attribute("value").as_string("");
    $(FIELD).push_back(DataStorage::shared().get<$(ARG_0)>(name));
}

#map
#serialize:
auto map_$(FIELD) = xml.append_child("$(FIELD)");
for(auto& pair : $(FIELD))
{
    auto xml = map_$(FIELD).append_child("pair");
    auto& key = pair.first;
    auto& value = pair.second;
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)
}
#deserialize:
auto map_$(FIELD) = xml.child("$(FIELD)");
for(auto child : map_$(FIELD))
{
    auto xml = child;
    $(KEY)
    $(VALUE_TYPE) value;
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)
    $(FIELD)[key] = value;
}

#enum
#serialize:
xml.append_attribute("$(FIELD)").set_value($(FIELD).str().c_str());
#deserialize:
$(FIELD) = std::string(xml.attribute("$(FIELD)").as_string(""));
'''


cpp_json = '''

#int, bool, float, string
#serialize:
#with default value:
if($(FIELD) != $(DEFAULT_VALUE))
{
    ::set(json,"$(FIELD)",$(FIELD));
}
#without default value:
::set(json,"$(FIELD)",$(FIELD));

#deserialize:
#with default value:
if(json.isMember("$(FIELD)"))
{
    $(FIELD) = ::get<$(TYPE)>(json["$(FIELD)"]);
}
else
{
    $(FIELD) = $(DEFAULT_VALUE);
}
#without default value:
$(FIELD) = ::get<$(TYPE)>(json["$(FIELD)"]);


#serialized
#serialize:
$(FIELD).serialize(json["$(FIELD)"]);
#deserialize:
$(FIELD).deserialize(json["$(FIELD)"]);


#pointer
#serialize
if($(FIELD))
{
    $(FIELD)->serialize(json["$(FIELD)"][$(FIELD)->get_type()]);
}
#deserialize:
if(json.isMember("$(FIELD)"))
{
    auto type_$(FIELD) = json["$(FIELD)"].getMemberNames()[0];
    $(FIELD) = Factory::shared().build<$(TYPE)>(type_$(FIELD));
    $(FIELD)->deserialize(json["$(FIELD)"][type_$(FIELD)]);
}


#list<bool>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(const auto& t : $(FIELD))
{
    arr_$(FIELD)[i_$(FIELD)++] = Json::Value(t);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back();
    $(FIELD).back() = ::get<$(ARG_0)>(arr_$(FIELD)[i]);
}

#list<int>, list<float>, list<string>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(const auto& t : $(FIELD))
{
    ::set(arr_$(FIELD)[i_$(FIELD)++], t);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back();
    $(FIELD).back() = ::get<$(ARG_0)>(arr_$(FIELD)[i]);
}


#list<serialized>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
int i_$(FIELD)=0;
for(auto& t : $(FIELD))
{
    t.serialize(arr_$(FIELD)[i_$(FIELD)++]);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(int i = 0; i < arr_$(FIELD).size(); ++i)
{
    $(FIELD).emplace_back();
    $(FIELD).back().deserialize(arr_$(FIELD)[i]);
}


#pointer_list
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(auto& t : $(FIELD))
{
    auto index = arr_$(FIELD).size();
    t->serialize(arr_$(FIELD)[index][t->get_type()]);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
auto size_$(FIELD) = arr_$(FIELD).size();
for(int i = 0; i < size_$(FIELD); ++i)
{
    auto type = arr_$(FIELD)[i].getMemberNames()[0];
    auto obj = Factory::shared().build<$(ARG_0)>(type);
    $(FIELD).emplace_back(obj);
    $(FIELD).back()->deserialize(arr_$(FIELD)[i][type]);
}


#link
#serialize:
::set(json,"$(FIELD)",$(FIELD)->name);
#deserialize:
$(FIELD) = DataStorage::shared().get<$(TYPE)>(::get<std::string>(json["$(FIELD)"]));


#list<link>
#serialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(auto& item : $(FIELD))
{
    auto index = arr_$(FIELD).size();
    arr_$(FIELD).append(item->name);
}
#deserialize:
auto& arr_$(FIELD) = json["$(FIELD)"];
for(auto item : arr_$(FIELD))
{
    auto name = ::get<std::string>(item);
    auto data = DataStorage::shared().get<$(ARG_0)>(name);
    $(FIELD).push_back(data);
}


#map
#serialize:
auto& map_$(FIELD) = json["$(FIELD)"];
for(auto& pair : $(FIELD))
{
    auto& json = map_$(FIELD)[map_$(FIELD).size()];
    auto& key = pair.first;
    auto& value = pair.second;
    $(KEY_SERIALIZE)
    $(VALUE_SERIALIZE)
}
#deserialize:
auto& map_$(FIELD) = json["$(FIELD)"];
auto size_$(FIELD)= map_$(FIELD).size();
for(unsigned int i = 0; i < size_$(FIELD); ++i)
{
    auto& json = map_$(FIELD)[i];
    $(KEY);
    $(VALUE_TYPE) value;
    $(VALUE_SERIALIZE)
    $(KEY_SERIALIZE)
    $(FIELD)[key] = value;
}


#enum
#serialize:
::set(json, "$(FIELD)", $(FIELD).str());
#deserialize:
$(FIELD) = ::get<std::string>(json["$(FIELD)"]);
'''

py_xml = '''
# $(0) = obj_name
# $(1) = obj_type
# $(2) = obj_value
# ??? {3} = '{}'
# $(4) = owner
# $(5) = obj_template_args[0].type if len(obj_template_args) > 0 else 'unknown_arg'

#int, bool, float, string
#serialize:
#with default value:
if $(OWNER)$(FIELD) != $(DEFAULT_VALUE): xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#without default value:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
#with default value:
$(OWNER)$(FIELD) = xml.get("$(FIELD)", default=$(DEFAULT_VALUE))
#without default value:
$(OWNER)$(FIELD) = xml.get("$(FIELD)")

#pointer
#serialize:
if $(OWNER)$(FIELD) != None:
            xml_pointer = ET.SubElement(xml, '$(FIELD)')
            xml_pointer.set('type', str($(TYPE)))
            $(OWNER)$(FIELD).serialize(xml_pointer)
#deserialize:
xml_pointer = xml.find('$(FIELD)')
        if xml_pointer != None:
            type = xml_pointer.get('type')
            $(OWNER)$(FIELD) = Factory.Factory.build(type);
            $(OWNER)$(FIELD).deserialize(xml_pointer)


#list<int>, list<bool>, list<float>, list<string>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            item = ET.SubElement(arr, 'item')
            item.set('value', str(obj))
#deserialize:
arr = xml.find('$(FIELD)')
        for obj in arr:
            $(OWNER)$(FIELD).append(obj.get('value'))


#list<serialized>
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for obj in $(OWNER)$(FIELD):
            item = ET.SubElement(arr, 'item')
            obj.serialize(item)
#deserialize:
arr = xml.find('$(FIELD)')
        for xml_child in arr:
            obj = $(TYPE)()
            obj.deserialize(xml_child)
            $(OWNER)$(FIELD).append(obj)


#serialized
#serialize:
if $(OWNER)$(FIELD) != None:
            xml_child = ET.SubElement(xml, '$(FIELD)')
            $(OWNER)$(FIELD).serialize(xml_child)
#deserialize:
xml_child = xml.find('$(FIELD)')
        if(xml_child != None):
            $(OWNER)$(FIELD) = $(TYPE)()
            $(OWNER)$(FIELD).deserialize(xml_child)


#pointer_list
#serialize:
arr = ET.SubElement(xml, '$(FIELD)')
        for t in $(OWNER)$(FIELD):
            item = ET.SubElement(arr, t.get_type())
            t.serialize(item)
#deserialize:
arr = xml.find('$(FIELD)')
        for xml_item in arr:
            type = xml_item.tag
            obj = Factory.Factory.build(type)
            obj.deserialize(xml_item)
            $(OWNER)$(FIELD).append(obj)

#link
#serialize:
if isinstance($(OWNER)$(FIELD), $(TYPE)):
            xml.set("$(FIELD)", $(OWNER)$(FIELD).name)
        else:
            xml.set("$(FIELD)", $(OWNER)$(FIELD))
#deserialize:
name_$(FIELD) = xml.get("$(FIELD)")
        $(OWNER)$(FIELD) = get_data_storage().get$(TYPE)(name_$(FIELD))

#list<link>
#serialize:
arr_$(FIELD) = ET.SubElement(xml, '$(FIELD)')
        for t in $(OWNER)$(FIELD):
            item = ET.SubElement(arr_$(FIELD), 'item')
            item.set("value", t.name)
#deserialize:
from DataStorage import DataStorage
        arr_$(FIELD) = xml.find('$(FIELD)')
        data = get_data_storage().get$(TYPE)(name_$(FIELD).get('value'))
        $(OWNER)$(FIELD).append(data)

#map
#serialize
        xml_cache = xml
        map = ET.SubElement(xml, '$(FIELD)')
        for key, value in $(OWNER)$(FIELD).iteritems():
            xml = ET.SubElement(map, 'pair')
$(KEY_SERIALIZE)
$(VALUE_SERIALIZE)
        xml = xml_cache
#deserialize
        xml_cache = xml
        map = xml.find('$(FIELD)')
        for xml_child in map:
            key = xml_child.get('key')
            type = key
            xml = xml_child
$(VALUE_SERIALIZE)
            $(OWNER)$(FIELD)[type] = _value
        xml = xml_cache

#enum
#serialize:
xml.set("$(FIELD)", str($(OWNER)$(FIELD)))
#deserialize:
$(OWNER)$(FIELD) = xml.get("$(FIELD)")
'''

py_json = '''
'''

protocols = {}
protocols['cpp'] = {'xml': cpp_xml, 'json': cpp_json}
protocols['py'] = {'xml': py_xml, 'json': py_json}
