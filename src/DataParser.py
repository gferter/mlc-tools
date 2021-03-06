import xml.etree.ElementTree as ET
import fileutils
import xml.dom.minidom
from DataStorageCreators import *
from Error import Error
import json


class DataParser:

    def __init__(self, classes, format, data_directory):
        self.objects = {}
        self.format = format
        self.classes = classes

        if self.format == 'xml':
            self._parse_xml(data_directory)
        elif self.format == 'json':
            self._parse_json(data_directory)
        self._validate()

    def flush(self, out_data_directory):
        buffer = ''
        file = 'data.' + self.format
        if self.format == 'xml':
            buffer = self._flush_xml(out_data_directory)
        elif self.format == 'json':
            buffer = self._flush_json(out_data_directory)
        fileutils.write(out_data_directory + file, buffer)

    def _parse_xml(self, data_directory):
        files = fileutils.get_files_list(data_directory)
        for file in files:
            if not file.endswith('.xml'):
                continue
            file = data_directory + file
            try:
                tree = ET.parse(file)
            except ET.ParseError:
                Error.exit(Error.CANNOT_PARSE_XML, file)

            root = tree.getroot()

            def add(object):
                if object.tag not in self.objects:
                    self.objects[object.tag] = []
                self._validate_type(object.tag, file)
                self.objects[object.tag].append(object)

            if root.tag == 'data':
                for object in root:
                    add(object)
            else:
                add(root)

    def _parse_json(self, data_directory):
        files = fileutils.get_files_list(data_directory)
        for file in files:
            if not file.endswith('.json'):
                continue
            file = data_directory + file
            root = json.loads(open(file).read())

            def parse(key, dict_):
                name = key
                self._validate_type(key, file)
                if name not in self.objects:
                    self.objects[name] = []
                self.objects[name].append(dict_)
            if isinstance(root, dict):
                for key in root:
                    parse(key, root)
            elif isinstance(root, list):
                for dict_ in root:
                    for key in dict_:
                        parse(key, dict_)

    def _validate(self):
        pass

    def _validate_type(self, type, file=''):
        class_name = get_class_name_from_data_name(type)
        valid = False
        for class_ in self.classes:
            if class_.name == class_name:
                valid = class_.is_storage
                break
        if not valid:
            print 'Unknown data type [{}]->[{}]. please check configuration. File: [{}]'.format(type, class_name, file)
            exit(-1)

    def _flush_xml(self, out_data_directory):
        root = ET.Element('data')
        for type in self.objects:
            name = get_data_list_name(get_data_name(type))
            node = ET.SubElement(root, name)
            for object in self.objects[type]:
                pair = ET.SubElement(node, 'pair')
                pair.attrib['key'] = object.attrib['name']
                object.tag = 'value'
                pair.append(object)

        buffer = ET.tostring(root)
        xml_ = xml.dom.minidom.parseString(buffer)
        buffer = xml_.toprettyxml(encoding='utf-8')
        lines = buffer.split('\n')
        buffer = ''
        for line in lines:
            if line.strip():
                buffer += line + '\n'
        return buffer

    def _flush_json(self, out_data_directory):
        dict_ = {}
        for key in self.objects:
            name = get_data_list_name(get_data_name(key))
            dict_[name] = []
            for object in self.objects[key]:
                dict_obj = {}
                for obj in object:
                    dict_obj['key'] = object[obj]['name']
                    dict_obj['value'] = object[obj]
                dict_[name].append(dict_obj)
        return json.dumps(dict_, indent=2)
