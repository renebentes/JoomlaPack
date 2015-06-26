# coding: utf-8

import sublime
import os

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class File:

    '''
    Represents a simple file text.
    '''

    def __init__(self, path, name, encoding='utf8'):
        self.path = path
        self.name = name
        self.encoding = encoding
        self.fullpath = os.path.join(self.path, self.name)

    def exists(self):
        '''
        Checks if file already exists.
        '''
        return os.path.exists(self.fullpath)

    def read(self):
        '''
        Reads a file.
        '''
        if self.exists():
            try:
                with open(self.fullpath, 'r+', encoding=self.encoding) as f:
                    return f.read()
            except Exception as e:
                Helper().show_message('error', 'File %s not be read! %s' %
                                      (self.fullpath, e))
        else:
            Helper().show_message(
                'error', 'File %s not found!' % self.fullpath)
            return None

    def save(self, data):
        '''
        Writes data file on disk.
        '''
        if not self.exists():
            try:
                with open(self.fullpath, 'w+', encoding=self.encoding) as f:
                    f.write(data)
                os.chmod(self.fullpath, 0o644)
            except Exception as e:
                Helper().show_message('error', 'File %s not be write! %s' %
                                      (self.fullpath, e))

        else:
            Helper().show_message(
                'error', 'File %s already exists!' % self.fullpath)
