# coding: utf-8

import sublime
import xml.etree.ElementTree as ET

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class Xml(File):

    '''
    Represents a XML file.
    '''

    def is_valid(self, path):
        '''
        Checks if a XML file is valid.
        '''
        return True if ET.parse(path) else False

    def add_child(self, path, parent=None, child={}):
        '''
        Adds childs element on XML.
        '''
        if child is None or type(child) is not dict or \
                not child.keys() & {'tag', 'text'}:
            print('child parameter invalid')
            return False

        data = self.read(path)

        if data is None:
            return False

        if parent is None:
            parent = data.tag

        parent = data.find(parent)
        for node in parent:
            if node.tag == child['tag'] and node.text == child['text']:
                if 'attribs' in child.keys():
                    for k in child['attribs']:
                        node.set(k, child['attribs'][k])

                return True

        node = Element(child['tag'])
        node.text = child['text']
        if 'attribs' in child.keys():
            for k in child['attribs']:
                node.set(k, child['attribs'][k])
        parent.append(node)

        print(ET.tostring(data.find(parent)))

        return True

    def read(self, path):
        '''
        Reads a XML file.
        '''
        if self.exists(path):
            if not self.is_valid(path):
                return None

            return ET.parse(path).getroot()
        else:
            Helper().show_message(
                'error', 'XML file %s not found!' % path)
            return None

    def write(self, path, data):
        '''
        Writes XML data file on disk.
        '''
        return True
