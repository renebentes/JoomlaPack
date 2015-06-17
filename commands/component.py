# coding: utf-8
import sublime
import sublime_plugin

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.lib.helpers import *
    from JoomlaPack.lib.project import Project, Component
else:
    from lib.helpers import *
    from lib.project import Project, Component


class NewComponentCommand(sublime_plugin.WindowCommand):

    def run(self):
        show_input_panel("Type Component name: ", "content",
                         self.on_done, None,
                         on_cancel)

    def on_done(self, name):
        self.project = Project(Component)
        self.project.set_attributes(name)
        self.project.create()
