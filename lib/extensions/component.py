# coding: utf-8
import sublime
import os
import re

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
    from JoomlaPack.lib.extensions.base import Base
    from JoomlaPack.lib.inflector import *
else:
    from lib import *
    from lib.extensions.base import Base
    from lib.inflector import *


class Component(Base):

    '''
    Implements the Joomla's Component extension. This is default.
    '''

    def __init__(self, content=None, inflector=English):
        Base.__init__(self, inflector)

        self.prefix = 'com_'
        self.template_path = 'component/basic'

        if content is not None:
            self.name = content
            self.fullname = self.inflector.underscore(self.prefix + self.name)
        else:
            self.fullname = self.inflector.underscore(
                Project().get_project_name())
            self.name = self.inflector.humanize(self.fullname, prefix='com_')

    def rename(self):
        singular = self.inflector.singularize(self.name)
        plural = self.inflector.pluralize(self.name)

        for root, dirs, files in os.walk(self.path):
            for filename in files:
                newname = re.sub('{{component}}', self.name,
                                 re.sub('{{singular}}', singular,
                                        re.sub('{{plural}}', plural,
                                               re.sub('{{locale}}',
                                                      Helper().language(),
                                                      filename))))

                if newname != filename:
                    os.rename(os.path.join(root, filename),
                              os.path.join(root, newname))

        for root, dirs, files in os.walk(self.path):
            for folder in dirs:
                newname = re.sub('{{singular}}', singular,
                                 re.sub('{{plural}}', plural,
                                        re.sub('{{locale}}',
                                               Helper().language(),
                                               folder)))

                if newname != folder:
                    os.rename(os.path.join(root, folder),
                              os.path.join(root, newname))

    def __str__(self):
        return "JoomlaPack: Joomla Component"
