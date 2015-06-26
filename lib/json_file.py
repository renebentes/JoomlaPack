# coding: utf-8

import sublime
import json

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class JsonFile(File):

    '''
    Represents a JSON file.
    '''

    def __init__(self, path, name, encoding='utf8', indent=4):
        File.__init__(self, path, name, encoding)
        self.indent = indent

    def read(self):
        '''
        Reads a JSON file.
        '''
        if File.read(self) is not None:
            return json.loads(File.read(self), encoding=self.encoding)
        else:
            Helper().show_message('error', 'File %s bad formated!' %
                                  self.fullpath)
            return None

    def save(self, data):
        '''
        Writes JSON data file on disk.
        '''
        data = json.dumps(data, sort_keys=False, indent=self.indent)
        File.save(self, data)
