# coding: utf-8
import sublime
import sublime_plugin

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.lib import *
    from JoomlaPack.lib.extensions import Plugin
else:
    from lib import *
    from lib.extensions import Plugin


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
        Helper().show_input_panel(self.options[self.keys[self.counter]][0],
                                  self.options[self.keys[self.counter]][1],
                                  self.on_done, None, Helper().on_cancel)

    def on_done(self, content):
        self.options[self.keys[self.counter]][1] = content
        self.counter += 1
        if self.counter < (len(self.options)):
            self.show_input_panel()
        else:
            self.project = Plugin(self.options)
            self.project.create()


class AddFormToPluginCommand(sublime_plugin.WindowCommand):

    def run(self):
        Helper().show_input_panel("Type Form name: ", "content",
                                  self.on_done, None, Helper().on_cancel)

    def on_done(self, name):
        self.project = Plugin()
        # self.project.add_form(name)

    def is_enabled(self):
        return Project().has_directories()


class AddFieldToPluginCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.project = Plugin()
        if Project().directories():
            Helper().show_input_panel("Type Field name: ", "title",
                                      self.project.on_done, None,
                                      Helper().on_cancel)
        else:
            message = '''[Error] Project folder not found! Please,
            create a Joomla plugin first.'''
            Helper().show_message('error', message)

    def is_enabled(self):
        return Project().has_directories()
