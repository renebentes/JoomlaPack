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

    def read(self, path, encoding='utf8'):
        '''
        Reads a JSON file.
        '''
        if File.read(path, encoding) is not None:
            return json.loads(File.read(path, encoding),
                              encoding=encoding)
        else:
            Helper().show_message('error', 'File %s bad formated!' %
                                  path)
            return None

    def write(self, path, data, encoding='utf8', mode=0o644, indent=4):
        '''
        Writes JSON data file on disk.
        '''
        data = json.dumps(data, sort_keys=False, indent=indent)
        return File().write(path, data, encoding, mode)
