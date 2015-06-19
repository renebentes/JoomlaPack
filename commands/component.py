# coding: utf-8
import sublime
import sublime_plugin

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
        self.project = Component(name)
        self.project.create()
