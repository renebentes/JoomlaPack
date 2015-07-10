# coding: utf-8

import sublime
import json

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class Json(File):

    '''
    Represents a JSON file.
    '''

    def __init__(self, path, encoding='utf-8'):
        File.__init__(self, path, encoding)

    def read(self):
        '''
        Reads a JSON file.
        '''
        if File.read() is not None:
            return json.loads(File.read(self), encoding=self.encoding)
        else:
            Helper().show_message('error', 'File %s bad formated!' %
                                  self.path)
            return None

    def write(self, data, mode=0o644, indent=4):
        '''
        Writes JSON data file on disk.
        '''
        data = json.dumps(data, sort_keys=False, indent=indent)
        return File.write(self, data, mode)
