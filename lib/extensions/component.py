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


class Component(Base):

    '''
    Implements the Joomla's Component extension. This is default.
    '''

    def set_attributes(self, name):
        self.inflector = Inflector(English)
        self.prefix = 'com_'
        self.name = name
        self.fullname = self.inflector.underscore(self.prefix + self.name)
        self.template_path = 'component/basic'

    def rename(self):
        singular = self.inflector.singularize(
            self.name) if not self.inflector.is_singular(
                self.name) else self.name

        plural = self.inflector.pluralize(
            self.name) if not self.inflector.is_plural(
                self.name) else self.name

        for root, dirs, files in os.walk(self.path):
            for filename in files:
                newname = re.sub('{{component}}', self.name,
                                 re.sub('{{singular}}', singular,
                                        re.sub('{{plural}}', plural,
                                               re.sub('{{locale}}',
                                                      language(), filename))))

                if newname != filename:
                    os.rename(os.path.join(root, filename),
                              os.path.join(root, newname))

        for root, dirs, files in os.walk(self.path):
            for folder in dirs:
                newname = re.sub('{{singular}}', singular,
                                 re.sub('{{plural}}', plural,
                                        re.sub('{{locale}}', language(),
                                               folder)))

                if newname != folder:
                    os.rename(os.path.join(root, folder),
                              os.path.join(root, newname))

    def __str__(self):
        return "JoomlaPack: Joomla Component"
