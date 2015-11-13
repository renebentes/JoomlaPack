# coding: utf-8
import sublime
import sublime_plugin
import os
import functools

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.lib import *
    from JoomlaPack.lib.extensions.base import Base
    from JoomlaPack.lib.inflector import English
else:
    from lib import *
    from lib.extensions.base import Base
    from lib.inflector import English


class NewJoomlaFolderCommand(sublime_plugin.WindowCommand):

    def run(self, paths):
        Helper().show_input_panel("Type Folder name: ", "new_folder",
                                  functools.partial(self.on_done, paths[0]),
                                  Helper().on_cancel)

    def on_done(self, path, name):
        path = path if os.path.isdir(path) else os.path.dirname(path)
        self.extension = Base(English)
        self.extension.path(path)
        self.extension.add_folder(name)
