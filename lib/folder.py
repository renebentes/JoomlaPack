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

    def exists(self, path):
        '''
        Checks if folder already exists.
        '''
        return os.path.exists(path)

    def create(self, path, mode=0o755):
        '''
        Create a folder, and all necessary parent folders.
        '''
        nested = 0

        parent = os.path.dirname(path)
        if not self.exists(parent):
            # Prevent infinit loops
            nested += 1

            if nested > 20 or parent == path:
                nested -= 1
                Helper().show_message('', '[Error] Infinite loop detected.')
                return False

            if not self.create(parent, mode):
                nested -= 1
                return False

            # Parent directory has been created
            nested -= 1

        if self.exists(path):
            return True

        oldmask = os.umask(0o000)
        try:
            os.makedirs(path, mode)
            os.umask(oldmask)
            self._on_create(path)
        except Exception as e:
            message = '[Error] Folder %s could not be created! %s' % (
                self.path, e)
            Helper().show_message('', message)
            os.umask(oldmask)
            return False
        return True

    def _on_create(self, path):
        data = ('<!DOCTYPE html>\n' +
                '<html>\n' +
                '<head>\n' +
                '  <title>&nbsp;</title>\n' +
                '</head>\n' +
                '<body></body>\n' +
                '</html>\n')
        File().write(os.path.join(path, 'index.html'), data)
