# coding: utf-8
import sublime
import sublime_plugin
import os
import re
import functools

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.lib import *
    from JoomlaPack.lib.extensions import Plugin, Package
else:
    from lib import *
    from lib.extensions import Plugin, Package


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
            self.extension = Plugin(self.options)
            if Project().type() == 'package':
                self.package = Package()
                if self.extension.create():
                    Manifest(os.path.join(self.package.path,
                                          '%s.xml' % self.package.name)) \
                        .add_child('files', {
                            'tag': 'file',
                            'text': '%s.zip' % self.extension.fullname,
                            'attribs': {
                                'type': 'plugin',
                                'id': self.extension.name,
                                'group': self.extension.group
                            }
                        })
                    Project().refresh()
            else:
                if self.extension.create():
                    self.extension.set_project()


class AddFormToPluginCommand(sublime_plugin.WindowCommand):

    def run(self, dirs):
        print(dirs)
        Helper().show_input_panel("Type Form name: ", "content",
                                  self.on_done, None, Helper().on_cancel)

    def on_done(self, name):
        name = name if name.endswith('.xml') else name + '.xml'
        self.extension = Plugin()

        if self.extension.add_folder('forms') \
            and self.extension.add_file(os.path.join('forms', name),
                                        'joomla-add-form-simple'):

            Manifest(os.path.join(self.extension.path,
                                  '%s.xml' % self.extension.name)) \
                .add_child('files',
                           {'tag': 'folder', 'text': 'forms'},
                           {'tag': 'folder', 'text': 'tmpl'})
        Project().refresh()

    def is_enabled(self, dirs):
        if len(dirs) == 1:
            for f in os.listdir(dirs[0]):
                if f.endswith('.xml'):
                    return Manifest(os.path.join(dirs[0], f)).is_manifest() \
                        and Manifest(os.path.join(dirs[0],
                                                  f)).type() == 'plugin'
        return Project().has_directories() and Project().has_valid_manifest() \
            and Project().type() == 'plugin'


class AddFieldToPluginCommand(sublime_plugin.WindowCommand):

    def run(self):
        Helper().show_input_panel("Type Field name: ", "title",
                                  self.on_done, None, Helper().on_cancel)

    def on_done(self, name):
        name = name if name.endswith('.php') else name + '.php'
        self.extension = Plugin()

        if self.extension.add_folder('fields') \
            and self.extension.add_file(os.path.join('fields', name),
                                        'joomla-field-custom'):

            Manifest(os.path.join(self.extension.path,
                                  '%s.xml' % self.extension.name)) \
                .add_child('files',
                           {'tag': 'folder', 'text': 'fields'},
                           {'tag': 'folder', 'text': 'forms'})
        Project().refresh()

    def is_enabled(self):
        return Project().has_directories() and Project().has_valid_manifest() \
            and Project().type() == 'plugin'


class AddInstallScriptToPluginCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.extension = Plugin()
        if self.extension.add_file('script.php',
                                   'joomla-header\njoomla-installer-script'):

            Manifest(os.path.join(self.extension.path,
                                  '%s.xml' % self.extension.name)) \
                .add_child('',
                           {'tag': 'scriptfile', 'text': 'script.php'},
                           {'tag': 'files', 'text': None})
        Project().refresh()

    def is_enabled(self):
        return Project().has_directories() and Project().has_valid_manifest() \
            and Project().type() == 'plugin'


class AddTemplateToPluginCommand(sublime_plugin.WindowCommand):

    def run(self):
        Helper().show_input_panel("Type Template name: ", "default",
                                  self.on_done, None, Helper().on_cancel)

    def on_done(self, name):
        name = name if name.endswith('.php') else name + '.php'
        self.extension = Plugin()

        if self.extension.add_folder('tmpl') \
            and self.extension.add_file(os.path.join('tmpl', name),
                                        'joomla-header'):

            Manifest(os.path.join(self.extension.path,
                                  '%s.xml' % self.extension.name)) \
                .add_child('files',
                           {'tag': 'folder', 'text': 'tmpl'},
                           {'tag': 'filename',
                            'text': '%s.php' % self.extension.name})
        Project().refresh()

    def is_enabled(self):
        return Project().has_directories() and Project().has_valid_manifest() \
            and Project().type() == 'plugin'


class AddLayoutToPluginCommand(sublime_plugin.WindowCommand):

    def run(self):
        Helper().show_input_panel("Type Layout context: ",
                                  "joomla.edit.title_alias",
                                  self.on_done, None, Helper().on_cancel)

    def on_done(self, name):
        name = re.sub('\.php$', '', re.sub('\.', '/', name))
        self.extension = Plugin()

        if self.extension.add_folder('layouts') \
            and self.extension.add_file(os.path.join('layouts', name),
                                        'joomla-header'):

            Manifest(os.path.join(self.extension.path,
                                  '%s.xml' % self.extension.name)) \
                .add_child('files',
                           {'tag': 'folder', 'text': 'layouts'},
                           {'tag': 'folder', 'text': 'tmpl'})
        Project().refresh()

    def is_enabled(self):
        return Project().has_directories() and Project().has_valid_manifest() \
            and Project().type() == 'plugin'
