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

    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.fullpath = os.path.join(self.path, self.name)

    def exists(self):
        '''
        Checks if folder already exists.
        '''
        return os.path.exists(self.fullpath)

    def read(self):
        pass

    def save(self, data):
        '''
        Writes a folder on disk.
        '''
        if not self.exists():
            if os.makedir(self.path, 0o755):
                self.on_save()
            else:
                Helper().show_message("error",
                                      "[Error] Folder %s could not be created!"
                                      % self.fullpath)
        else:
            Helper().show_message("error", "[Error] Folder %s already exists!"
                                  % self.fullpath)

        def on_save(self):
            data = ('<!DOCTYPE html>' +
                    '<html>' +
                    '<head>' +
                    '  <title>&nbsp;</title>' +
                    '</head>' +
                    '<body></body>' +
                    '</html>')
            File(self.fullpath, 'index.html').save(data)
