from Class import Class
from Object import Object
from Function import Function
import constants

def get_member_name(name):
    name = name.lower()
    if name.find('data') == 0:
        name = name[4:]
        
    last = name[-1]
    if last in 'y':
        if last in 'a,e,i,o,u,y':
            name = name[0:-1] + 'ies'
        else:
            name += 's'
    elif last in 'ou':
        name += 'es'
    elif last == 'f':
        name = name[0:-1] + 'ves'
    elif name[-2:-1] == 'fe':
        name = name[0:-2] + 'ves'
    elif last in ['s', 'ss', 'x', 'sh', 'ch']:
        name += 'es'
    else:
        name += 's'

    return name


class DataStorageCpp(Class):
    
    def __init__(self, name, classes, data_file):
        Class.__init__(self)

        self.name = name
        self.is_serialized = True

        string_obj = Object()
        string_obj.type = 'string'
        for class_ in classes:
            if class_.is_storage:
                object = Object()
                object.type = 'map'
                object.name = get_member_name(class_.name)
                object.template_args.append(string_obj)
                object.template_args.append(class_)
                self.members.append(object)

        loaded = Object()
        loaded.is_runtime = True
        loaded.name = '_loaded'
        loaded.type = 'bool'
        loaded.initial_value = 'false'
        self.members.append(loaded)

        function = Function()
        function.name = 'shared'
        function.args.append(['', ''])
        function.return_type = 'const {}&'.format(self.name)
        function.is_static = True
        function.operations.append('static {} instance;'.format(self.name))
        function.operations.append('return instance;')
        self.functions.append(function)
        
        function = Function()
        function.name = 'initialize'
        function.return_type = 'void'
        function.is_const = True
        function.args.append(['buffer', 'string'])
        self.add_initialize_function_operations(function)
        self.functions.append(function)
    
    def add_initialize_function_operations(self, function):
        pass


    def get_header_getter(self):
        function = Function()
        function.name = 'get'
        function.args.append(['name', 'string'])
        function.return_type = 'template <class T> const T*'
        function.is_const = True
        function.is_template = True
        return function

    def get_source_getters(self, classes):
        string_obj = Object()
        string_obj.type = 'string'
        getters = []
        for class_ in classes:
            if class_.is_storage:
                getter = Function()
                getter.is_template = True
                getter.is_const = True
                getter.name = 'get'
                getter.args.append(['name', 'string'])
                getter.return_type = 'template <> const {}*'.format(class_.name)
                getter.operations.append('return _loaded ? &{0}.at(name) : &const_cast<{1}*>(this)->{0}[name];'.format(get_member_name(class_.name), self.name))
                getters.append(getter)
        return getters


class DataStorageCppXml(DataStorageCpp):

    def __init__(self, name, classes, data_file):
        DataStorageCpp.__init__(self, name, classes, data_file)

    def add_initialize_function_operations(self, function):
        function.operations.append('assert(!{});'.format('_loaded'))
        function.operations.append('pugi::xml_document doc;')
        function.operations.append('doc.load(buffer.c_str());')
        function.operations.append('const_cast<{}*>(this)->deserialize(doc.root().first_child());'.format(self.name))
        function.operations.append('const_cast<{}*>(this)->_loaded = static_cast<bool>(doc.root());'.format(self.name))


class DataStorageCppJson(DataStorageCpp):

    def __init__(self, name, classes, data_file):
        DataStorageCpp.__init__(self, name, classes, data_file)

    def add_initialize_function_operations(self, function):
        function.operations.append('assert(!{});'.format('_loaded'))
        function.operations.append('Json::Value json;')
        function.operations.append('Json::Reader reader;')
        function.operations.append('reader.parse(buffer, json);')
        function.operations.append('const_cast<{}*>(this)->deserialize(json);'.format(self.name))
        function.operations.append('const_cast<{}*>(this)->_loaded = true;'.format(self.name))
