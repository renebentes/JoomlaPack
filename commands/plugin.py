# coding: utf-8
import sublime
import sublime_plugin

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.lib.helpers import *
    from JoomlaPack.lib.project import Project, Plugin
else:
    from lib.helpers import *
    from lib.project import Project, Plugin


class NewPluginCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.counter = 0
        self.keys = ['name', 'group']
        self.options = {
            'name': ['Type Plugin Name:', 'vote'],
            'group': ['Type Plugin Group:', 'content']
        }

        self.show_input_panel()

    def show_input_panel(self):
        show_input_panel(self.options[self.keys[self.counter]][0],
                         self.options[self.keys[self.counter]][1],
                         self.on_done, None, on_cancel)

    def on_done(self, content):
        self.options[self.keys[self.counter]][1] = content
        self.counter += 1
        if self.counter < (len(self.options)):
            self.show_input_panel()
        else:
            self.project = Project(Plugin)
            self.project.set_attributes(self.options)
            self.project.create()


class AddFormToPluginCommand(sublime_plugin.WindowCommand):

    def run(self):
        if not directories():
            message = ('[Info] Plugin folder not found! ' +
                       'Please, create a Joomla Plugin first.')
            show_message('info', message)
        else:
            show_input_panel("Type Form name: ", "content",
                             self.on_done, None,
                             on_cancel)

    def on_done(self, name):
        self.project = Project(Plugin)
        self.project.add_form(name)


class AddFieldToPluginCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.project = Project(Plugin)
        if directories():
            show_input_panel("Type Field name: ", "title",
                             self.project.on_done, None,
                             project.on_cancel)
        else:
            message = '''[Error] Project folder not found! Please,
            create a Joomla plugin first.'''
            show_message('error', message)
