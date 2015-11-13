# coding: utf-8

import sublime
import re
from xml.dom import minidom

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class Manifest(File):

    """Represents a Manifest XML file."""

    def __init__(self, path, encoding='utf-8'):
        """Initialize the object Manifest

        Args:
            path (str): Path to XML file
            encoding (str, optional): Encoding of file.
        """
        File.__init__(self, path, encoding)

    def read(self):
        """Reads a Manifest XML file.

        Returns:
            minidom.DocumentElement: The root element from XML, None otherwise
        """
        try:
            return minidom.parseString(File.read(self))
        except Exception as e:
            Helper().show_message('',
                                  'Manifest XML file %s not be valid! %s' %
                                  (self.path, e))
            return None

    def write(self, data, force=False):
        """Writes data Manifest XML file on disk.

        Args:
            data (minidom.DocumentElement): The root element from XML.
            force (bool, optional): Force the file creation

        Returns:
            bool: True on success, false otherwise
        """
        self._update_version(data)

        data = str(data.toprettyxml(encoding=self.encoding),
                   encoding=self.encoding)
        rc = []
        for line in data.split('\n'):
            if line.strip():
                rc.append(line)

        data = re.sub(r'\]\>\t\<', ']><',
                      re.sub(r'\>\n\<\!', '><!', '\n'.join(rc)))

        return File.write(self, data, True)

    def is_manifest(self):
        """Checks if a Manifest XML file is valid.

        Returns:
            bool: True if XML file is manfest valid, false otherwise.
        """
        xml = self.read()
        return xml is not None \
            and xml.documentElement.tagName == 'extension'

    def type(self):
        xml = self.read()
        return xml.documentElement.getAttribute('type') if xml is not None \
            else None

    def add_child(self, parent, child, childRef=None):
        """Adds element on Manifest XML.

        Args:
            parent (str): The parent element tag
            child (dict): The new element
            childRef (dict, optional): The references element.

        Returns:
            bool: True on success, false otherwise
        """
        if parent is not None and not isinstance(parent, str):
            raise TypeError('parent must be a string!')
            return False

        if child is None or not isinstance(child, dict) \
                or not all(k in child for k in ('tag', 'text')):
            raise TypeError('child parameter is invalid!')
            return False

        if childRef is not None \
            and (not isinstance(childRef, dict)
                 or not all(k in childRef for k in ('tag', 'text'))):
            raise TypeError('childRef parameter is invalid!')
            return False

        xml = self.read()
        if xml is None:
            return False

        if parent is None or parent == '':
            parent = xml.getElementsByTagName('extension')
        else:
            parent = xml.getElementsByTagName(parent)
            if parent.length == 0:
                print('Parent element %s not found!' % parent)
                return False

        found = False
        for node in parent[0].childNodes:
            if node.nodeType == node.ELEMENT_NODE \
                    and node.tagName == child['tag']:
                for childNode in node.childNodes:
                    if childNode.nodeType == childNode.TEXT_NODE \
                            and childNode.data == child['text']:
                        found = True
            if found:
                break

        if not found:
            node = xml.createElement(child['tag'])
            node.appendChild(xml.createTextNode(child['text']))

            if childRef is None:
                self._insert(parent[0], node)
            else:
                found = False
                for nodeRef in parent[0].childNodes:
                    if nodeRef.nodeType == nodeRef.ELEMENT_NODE \
                            and nodeRef.tagName == childRef['tag']:
                        for childNode in nodeRef.childNodes:
                            if childRef['text'] is None or \
                                    childNode.nodeType == childNode.TEXT_NODE \
                                    and childNode.data == childRef['text']:
                                found = True
                    if found:
                        break
                if found:
                    self._insert(parent[0], node, nodeRef)
                else:
                    self._insert(parent[0], node)

        if 'attribs' in child.keys():
            for key in child['attribs'].keys():
                node.setAttribute(key, child['attribs'][key])

        return self.write(xml)

    def _update_version(self, xml):
        """Updates version elementent on Manifest XML.

        Args:
            xml (minidom.DocumentElement): The root element from XML.

        Returns:
            bool: True on success, false otherwise.
        """
        if xml is None:
            return False

        version = xml.getElementsByTagName('version')
        if version.length > 0:
            version_list = self._get_text(version[0].childNodes).split('.')
            if len(version_list) >= 2:
                major = version_list[0]
                minor = version_list[1]
                patch = '0'
            else:
                major = self._get_text(version)
                minor = '0'
                patch = '0'
            minor = int(minor) + 1
            self._set_text(version[0].childNodes,
                           '.'.join([major, str(minor), patch]))
        else:
            version = xml.createElement('version')
            version.appendChild(xml.createTextNode('0.1.0'))
            description = xml.getElementsByTagName('description')
            if description.lenght > 0:
                self._insert(xml.documentElement, version, description[0])
            else:
                self._insert(xml.documentElement, version)
        return True

    def _insert(self, parent, child, childRef=None):
        """Alias to insert elements on XML structure.

        If childRef is None, call function appendChild from xml.dom.minidom
        library, otherwise insertBefore.

        Args:
            parent (minidom.Element): The parent element.
            child (minidom.Element): The new element.
            childRef (minidom.Element, optional): The reference element.

        Returns:
            bool: True on success, false otherwise
        """
        if not isinstance(parent, minidom.Element):
            raise TypeError('parent must be minidom.Element instance!')
            return False

        if not isinstance(child, minidom.Element):
            raise TypeError('child must be a minidom.Element instance!')
            return False

        if childRef is not None and not isinstance(childRef, minidom.Element):
            raise TypeError('childRef must be a minidom.Element instance!')

        if childRef is None:
            parent.appendChild(child)
        else:
            parent.insertBefore(child, childRef)

    def _get_text(self, nodelist):
        """Returns the text from nodelist elements.

        Args:
            nodelist (minidom.NodeList): The element

        Returns:
            str: The text
        """
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def _set_text(self, nodelist, text):
        """Defines the text of nodelist elements.

        Args:
            nodelist (minidom.NodeList): The element
            text (str): The text
        """
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                node.data = text
