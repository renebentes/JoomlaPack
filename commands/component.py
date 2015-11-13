# coding: utf-8
import sublime
import sublime_plugin
import os

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.lib import *
    from JoomlaPack.lib.extensions import Component
else:
    from lib import *
    from lib.extensions import Component


class NewComponentCommand(sublime_plugin.WindowCommand):

    def run(self):
        Helper().show_input_panel("Type Component name: ", "content",
                                  self.on_done, None,
                                  Helper().on_cancel)

    def on_done(self, name):
        self.extension = Component(name)

        if Project().type() == 'package':
            self.package = Package()
            self.extension.path(os.path.join(self.package.path,
                                             'packages',
                                             self.extension.fullname))

            if self.extension.create():
                Manifest(os.path.join(self.package.path,
                                      '%s.xml' % self.package.name)) \
                    .add_child('files', {
                        'tag': 'file',
                        'text': '%s.zip' % self.extension.fullname,
                        'attribs': {
                            'type': 'component',
                            'id': self.extension.fullname,
                        }
                    })
                Project().refresh()
        else:
            self.extension.path(os.path.join(Project().root(),
                                             self.extension.fullname))

            if self.extension.create():
                self.extension.set_project()
