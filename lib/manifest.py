# coding: utf-8

import sublime
import os
import xml.etree.ElementTree as ET

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class Manifest(File):

    '''
    Represents a Manifest XML file.
    '''

    def __init__(self, path, encoding='utf-8'):
        File.__init__(self, path, encoding)

    def is_manifest(self):
        '''
        Checks if a Manifest XML file is valid.
        '''
        xml = self.read()
        return True if xml is not None and xml.tag == 'extension' else False

    def add_child(self, parent, child, childRef=''):
        '''
        Adds elements on Manifest XML.
        '''
        if parent is None or not isinstance(parent, str):
            Helper().show_message('', 'parent must be a string!')
            return False

        if child is None or not isinstance(child, dict) \
                or not all(k in child for k in ('tag', 'text')):
            Helper().show_message('', 'child parameter is invalid!')
            return False

        xml = self.read()
        if xml is None:
            return False

        if parent == '':
            parent = xml
        else:
            parent = xml.find(parent)
            if parent is None:
                Helper().show_message('',
                                      'Parent element %s not found!' % parent)
                return False

        found = False
        for node in parent.iterfind(child['tag']):
            if node.text == child['text']:
                found = True
                break

        if not found:
            node = ET.Element(child['tag'])
            node.text = child['text']
            self._insert(parent, node, childRef)

        if 'attribs' in child.keys():
            for key in child['attribs'].keys():
                node.set(key, child['attribs'][key])

        self._update_version(xml)
        self.write(xml)

    def read(self):
        '''
        Reads a Manifest XML file.
        '''
        try:
            return ET.fromstring(File.read(self))
        except Exception as e:
            Helper().show_message('',
                                  'Manifest XML file %s not be valid! %s' %
                                  (self.path, e))
            return None

    def write(self, data, mode=0o644):
        '''
        Writes data Manifest XML file on disk.
        '''
        if not Folder(os.path.dirname(self.path)).exists():
            if not Folder(os.path.dirname(self.path)).create():
                return False

        oldmask = os.umask(0o000)
        try:
            ET.ElementTree(data).write(self.path,
                                       encoding=self.encoding,
                                       xml_declaration=True)
            if oldmask == 0:
                os.chmod(self.path, mode)
            os.umask(oldmask)
            return True
        except Exception as e:
            Helper().show_message('', 'Manifest XML file %s not be write! %s' %
                                  (self.path, e))
            os.umask(oldmask)
            return False

    def _update_version(self, xml):
        '''
        Updates version element on Manifest XML.
        '''
        if xml is None:
            return False

        version = xml.find('version')
        if version is not None:
            version_list = version.text.split('.')
            if len(version_list) >= 2:
                major = version_list[0]
                minor = version_list[1]
                patch = '0'
            else:
                major = version.text
                minor = '0'
                patch = '0'
            minor = int(minor) + 1
            version.text = '.'.join([major, str(minor), patch])
        else:
            version = ET.Element('version')
            version.text = '0.1.0'
            self._insert(xml, version, 'description')
        return True

    def _insert(self, parent, child, childRef=''):
        '''
        Alias to insert elements on XML structure.

        If childRef empty string, call function append() from
        xml.etree.ElementTree library, otherwise insert() instead.
        '''
        if not isinstance(parent, ET.Element):
            Helper().show_message('', 'parent must be ElementTree.Element!')
            return False

        if not isinstance(child, ET.Element):
            Helper().show_message('', 'child must be a ElementTree.Element!')
            return False

        if not isinstance(childRef, str):
            Helper().show_message('', 'childRef must be a string!')
            return False

        if childRef == '':
            parent.append(child)
            return True
        else:
            index = 0
            for node in parent.iter():
                if node.tag == childRef:
                    break
                index += 1
            parent.insert(index - 1, child)
            return True
