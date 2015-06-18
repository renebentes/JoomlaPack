# coding: utf-8
import sublime
import sublime_plugin

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.lib.helpers import *
    from JoomlaPack.lib.extensions import Component
else:
    from lib.helpers import *
    from lib.extensions import Component


class NewComponentCommand(sublime_plugin.WindowCommand):

    def run(self):
        show_input_panel("Type Component name: ", "content",
                         self.on_done, None,
                         on_cancel)

    def on_done(self, name):
        self.project = Component(name)
        self.project.create()
