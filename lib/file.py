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

    def exists(self, path):
        '''
        Checks if file already exists.
        '''
        return os.path.exists(path)

    def read(self, path, encoding='utf8'):
        '''
        Reads a file.
        '''
        if self.exists(path):
            try:
                with open(path, 'r', encoding=encoding) as f:
                    return f.read()
            except Exception as e:
                Helper().show_message('', 'File %s not be read! %s' %
                                      (path, e))
                return None
        else:
            Helper().show_message(
                'error', 'File %s not found!' % path)
            return None

    def write(self, path, data, encoding='utf8', mode=0o644):
        '''
        Writes data file on disk.
        '''
        if not Folder().exists(os.path.dirname(path)):
            if not Folder().create(os.path.dirname(path)):
                return False

        if self.exists(path):
            return True
        else:
            oldmask = os.umask(0o000)
            try:
                with open(path, 'w', encoding=encoding) as f:
                    f.write(data)
                if oldmask == 0:
                    os.chmod(path, mode)
                os.umask(oldmask)
                return True
            except Exception as e:
                Helper().show_message('', 'File %s not be write! %s' %
                                      (path, e))
                os.umask(oldmask)
                return False
