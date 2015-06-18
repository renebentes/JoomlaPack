# coding: utf-8
import sublime
import os

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.extensions.base import Base
    from JoomlaPack.lib.inflector import *
else:
    from lib.extensions.base import Base
    from lib.inflector import *


class Package(Base):

    '''
    Implements the Joomla's Package of extensions.
    '''

    def __init__(self, content=None, inflector=English):
        Base.__init__(self, inflector)

        self.prefix = 'pkg_'
        self.template_path = 'package'

        if content is not None:
            self.name = content
            self.fullname = self.inflector.underscore(self.prefix + content)
        else:
            pass

    def rename(self):
        name = self.inflector.humanize(self.name, self.prefix)

        for root, dirs, files in os.walk(self.path):
            for filename in files:
                newname = filename.replace('{{package}}', name)

                if newname != filename:
                    os.rename(os.path.join(root, filename),
                              os.path.join(root, newname))

    def __str__(self):
        return "JoomlaPack: Joomla Package"
