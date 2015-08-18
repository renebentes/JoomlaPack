# coding: utf-8

import sublime
import os

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class File():

    '''
    Represents a simple file text.
    '''

    def __init__(self, path, encoding='utf-8'):
        self.path = path
        self.encoding = encoding

    def exists(self):
        '''
        Checks if file already exists.
        '''
        return os.path.exists(self.path) and os.path.isfile(self.path)

    def read(self):
        '''
        Reads a file.
        '''
        if self.exists():
            try:
                with open(self.path, 'r', encoding=self.encoding) as f:
                    return f.read()
            except Exception as e:
                Helper().show_message('', 'File %s not be read! %s' %
                                      (self.path, e))
                return None
        else:
            Helper().show_message(
                'error', 'File %s not found!' % self.path)
            return None

    def write(self, data, force=False):
        '''
        Writes data file on disk.
        '''
        if not isinstance(data, str):
            raise TypeError('data must be a string!')
            return False

        if not Folder(os.path.dirname(self.path)).exists():
            if not Folder(os.path.dirname(self.path)).create():
                return False

        if self.exists() and not force:
            return True
        else:
            try:
                with open(self.path, 'w', encoding=self.encoding) as f:
                    f.write(data)
                os.chmod(self.path, 0o644)
                return True
            except Exception as e:
                Helper().show_message('', 'File %s not be write! %s' %
                                      (self.path, e))
                return False
