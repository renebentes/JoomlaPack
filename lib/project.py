# coding: utf-8
import sublime

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.extensions import *
else:
    from lib.extensions import *


class Project(object):

    '''
    Defines extensions type for Joomla.

    It provide methods to assist in the development of Joomla's extensions.
    '''

    def __init__(self, extension=Component):
        assert callable(extension), "extension should be a callable obj"
        self._extension = extension()

    def create(self):
        '''
        Creates structure to extensions.
        '''
        return self._extension.create()

    def set_attributes(self, content):
        '''
        Defines attributes to extension.
        '''
        return self._extension.set_attributes(content)

    def add_form(self, name):
        '''
        Add xml form files to extensions.
        '''
        return self._extension.add_form(name)

    def __str__(self):
        '''
        Returns the type of the Joomla's extension.
        '''
        return self._extension.__str__()
