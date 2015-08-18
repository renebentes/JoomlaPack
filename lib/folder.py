# coding: utf-8

import sublime
import os

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class Folder:

    '''
    Represents a simple folder.
    '''

    def __init__(self, path):
        self.path = path

    def exists(self):
        '''
        Checks if folder already exists.
        '''
        return os.path.exists(self.path) and os.path.isdir(self.path)

    def create(self, force=False):
        '''
        Create a folder, and all necessary parent folders.
        '''
        nested = 0

        parent = Folder(os.path.dirname(self.path))
        if not parent.exists():
            # Prevent infinit loops
            nested += 1

            if nested > 20 or parent.path == self.path:
                nested -= 1
                Helper().show_message('', '[Error] Infinite loop detected.')
                return False

            if not parent.create():
                nested -= 1
                return False

            # Parent directory has been created
            nested -= 1

        if self.exists() and not force:
            return True

        try:
            os.makedirs(self.path, 0o755)
            data = ('<!DOCTYPE html>\n' +
                    '<html>\n' +
                    '<head>\n' +
                    '  <title>&nbsp;</title>\n' +
                    '</head>\n' +
                    '<body></body>\n' +
                    '</html>\n')
            File(os.path.join(self.path, 'index.html')).write(data)
            return True
        except Exception as e:
            message = '[Error] Folder %s could not be created! %s' % (
                self.path, e)
            Helper().show_message('', message)
            return False
