# coding: utf-8
import sublime
import sublime_plugin

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.commands.plugin import *
    from JoomlaPack.lib import *
    from JoomlaPack.lib.extensions import Package
else:
    from commands.plugin import *
    from lib import *
    from lib.extensions import Package


class NewPackageCommand(sublime_plugin.WindowCommand):

    def run(self):
        Helper().show_input_panel("Type Package name: ", "package",
                                  self.on_done, None,
                                  Helper().on_cancel)

    def on_done(self, name):
        self.extension = Package(name)
        if self.extension.create():
            self.extension.set_project()
