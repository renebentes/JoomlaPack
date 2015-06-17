# coding: utf-8
import sublime
import os
import re

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.helpers import *
    from JoomlaPack.lib.extensions.base import Base
    from JoomlaPack.lib.inflector import Inflector, English
else:
    from lib.helpers import *
    from lib.extensions.base import Base
    from lib.inflector import Inflector, English


class Plugin(Base):

    '''
    Implements the Joomla's Plugin extension.
    '''

    def set_attributes(self, content):
        self.inflector = Inflector(English)
        self.prefix = 'plg_'
        self.group = content['group'][1]
        self.name = content['name'][1]
        self.fullname = self.inflector.underscore(self.inflector.variablize(
            self.prefix + self.group + ' ' + self.name))
        self.template_path = 'plugin'

    def rename(self):
        for root, dirs, files in os.walk(self.path):
            for filename in files:
                newname = re.sub('{{name}}', self.name,
                                 re.sub('{{group}}', self.group,
                                        re.sub('{{locale}}', language(),
                                               filename)))

                if newname != filename:
                    os.rename(os.path.join(root, filename),
                              os.path.join(root, newname))

        for root, dirs, files in os.walk(self.path):
            for folder in dirs:
                newname = folder.replace(
                    '{{locale}}', language())

                if newname != folder:
                    os.rename(os.path.join(root, folder),
                              os.path.join(root, newname))

    def add_form(self, name):
        self.path()
        print(self.path)

    def __str__(self):
        return "JoomlaPack: Joomla Plugin"
