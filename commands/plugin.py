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
            self.extension = Plugin(self.options['group'][1] + '_'
                                    + self.options['name'][1])

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
                                'type': 'plugin',
                                'id': self.extension.name,
                                'group': self.extension.group
                            }
                        })
                    Project().refresh()
            else:
                self.extension.path(os.path.join(Project().root(),
                                                 self.extension.fullname))

                if self.extension.create():
                    self.extension.set_project()


class AddFormToPluginCommand(sublime_plugin.WindowCommand):

    def run(self, paths):
        Helper().show_input_panel("Type Form name: ", "content",
                                  functools.partial(self.on_done, paths[0]),
                                  None, Helper().on_cancel)

    def on_done(self, path, name):
        name = name if name.endswith('.xml') else name + '.xml'
        path = None if Project().type() == 'plugin' else path

        if path is not None:
            path = path if os.path.isdir(path) else os.path.dirname(path)
            self.extension = Plugin(os.path.basename(path))
            self.extension.path(path)
        else:
            self.extension = Plugin()
            self.extension.path(os.path.join(Project().root(),
                                             self.extension.fullname))

        if self.extension.add_folder('forms') \
            and self.extension.add_file(os.path.join('forms', name),
                                        'joomla-add-form-simple'):

            Manifest(os.path.join(self.extension.path,
                                  '%s.xml' % self.extension.name)) \
                .add_child('files',
                           {'tag': 'folder', 'text': 'forms'},
                           {'tag': 'folder', 'text': 'tmpl'})
        Project().refresh()

    def is_enabled(self, paths):
        if Project().type() == 'plugin':
            return True
        elif Project().type() == 'package':
            if len(paths) == 1:
                path = paths[0] if os.path.isdir(paths[0]) \
                    else os.path.dirname(paths[0])
                for f in os.listdir(path):
                    if f.endswith('.xml') and \
                            Manifest(os.path.join(path, f)).is_manifest() and \
                            Manifest(os.path.join(path, f)).type() == 'plugin':
                        return True

        return False


class AddFieldToPluginCommand(sublime_plugin.WindowCommand):

    def run(self, paths):
        Helper().show_input_panel("Type Field name: ", "title",
                                  functools.partial(self.on_done, paths[0]),
                                  None, Helper().on_cancel)

    def on_done(self, path, name):
        name = name if name.endswith('.php') else name + '.php'
        path = None if Project().type() == 'plugin' else path

        if path is not None:
            path = path if os.path.isdir(path) else os.path.dirname(path)
            self.extension = Plugin(os.path.basename(path))
            self.extension.path(path)
        else:
            self.extension = Plugin()
            self.extension.path(os.path.join(Project().root(),
                                             self.extension.fullname))

        if self.extension.add_folder('fields') \
            and self.extension.add_file(os.path.join('fields', name),
                                        'joomla-header\n' +
                                        'joomla-field-custom'):

            Manifest(os.path.join(self.extension.path,
                                  '%s.xml' % self.extension.name)) \
                .add_child('files',
                           {'tag': 'folder', 'text': 'fields'},
                           {'tag': 'folder', 'text': 'forms'})
        Project().refresh()

    def is_enabled(self, paths):
        if Project().type() == 'plugin':
            return True
        elif Project().type() == 'package':
            if len(paths) == 1:
                path = paths[0] if os.path.isdir(paths[0]) \
                    else os.path.dirname(paths[0])
                for f in os.listdir(path):
                    if f.endswith('.xml') and \
                            Manifest(os.path.join(path, f)).is_manifest() and \
                            Manifest(os.path.join(path, f)).type() == 'plugin':
                        return True

        return False


class AddInstallScriptToPluginCommand(sublime_plugin.WindowCommand):

    def run(self, paths):
        path = None if Project().type() == 'plugin' else paths[0]

        if path is not None:
            path = path if os.path.isdir(path) else os.path.dirname(path)
            self.extension = Plugin(os.path.basename(path))
            self.extension.path(path)
        else:
            self.extension = Plugin()
            self.extension.path(os.path.join(Project().root(),
                                             self.extension.fullname))

        if self.extension.add_file('script.php',
                                   'joomla-header\njoomla-installer-script'):

            Manifest(os.path.join(self.extension.path,
                                  '%s.xml' % self.extension.name)) \
                .add_child('',
                           {'tag': 'scriptfile', 'text': 'script.php'},
                           {'tag': 'files', 'text': None})
        Project().refresh()

    def is_enabled(self, paths):
        if Project().type() == 'plugin':
            return True
        elif Project().type() == 'package':
            if len(paths) == 1:
                path = paths[0] if os.path.isdir(paths[0]) \
                    else os.path.dirname(paths[0])
                for f in os.listdir(path):
                    if f.endswith('.xml') and \
                            Manifest(os.path.join(path, f)).is_manifest() and \
                            Manifest(os.path.join(path, f)).type() == 'plugin':
                        return True

        return False


class AddTemplateToPluginCommand(sublime_plugin.WindowCommand):

    def run(self, paths):
        Helper().show_input_panel("Type Template name: ", "default",
                                  functools.partial(self.on_done, paths[0]),
                                  None, Helper().on_cancel)

    def on_done(self, path, name):
        name = name if name.endswith('.php') else name + '.php'
        path = None if Project().type() == 'plugin' else path

        if path is not None:
            path = path if os.path.isdir(path) else os.path.dirname(path)
            self.extension = Plugin(os.path.basename(path))
            self.extension.path(path)
        else:
            self.extension = Plugin()
            self.extension.path(os.path.join(Project().root(),
                                             self.extension.fullname))

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

    def is_enabled(self, paths):
        if Project().type() == 'plugin':
            return True
        elif Project().type() == 'package':
            if len(paths) == 1:
                path = paths[0] if os.path.isdir(paths[0]) \
                    else os.path.dirname(paths[0])
                for f in os.listdir(path):
                    if f.endswith('.xml') and \
                            Manifest(os.path.join(path, f)).is_manifest() and \
                            Manifest(os.path.join(path, f)).type() == 'plugin':
                        return True

        return False


class AddLayoutToPluginCommand(sublime_plugin.WindowCommand):

    def run(self, paths):
        Helper().show_input_panel("Type Layout context: ",
                                  "joomla.edit.title_alias",
                                  functools.partial(self.on_done, paths[0]),
                                  None, Helper().on_cancel)

    def on_done(self, path, name):
        name = re.sub('\.php$', '', re.sub('\.', '/', name))
        path = None if Project().type() == 'plugin' else path

        if path is not None:
            path = path if os.path.isdir(path) else os.path.dirname(path)
            self.extension = Plugin(os.path.basename(path))
            self.extension.path(path)
        else:
            self.extension = Plugin()
            self.extension.path(os.path.join(Project().root(),
                                             self.extension.fullname))

        if self.extension.add_folder('layouts') \
            and self.extension.add_file(os.path.join('layouts', name),
                                        'joomla-header'):

            Manifest(os.path.join(self.extension.path,
                                  '%s.xml' % self.extension.name)) \
                .add_child('files',
                           {'tag': 'folder', 'text': 'layouts'},
                           {'tag': 'folder', 'text': 'tmpl'})
        Project().refresh()

    def is_enabled(self, paths):
        if Project().type() == 'plugin':
            return True
        elif Project().type() == 'package':
            if len(paths) == 1:
                path = paths[0] if os.path.isdir(paths[0]) \
                    else os.path.dirname(paths[0])
                for f in os.listdir(path):
                    if f.endswith('.xml') and \
                            Manifest(os.path.join(path, f)).is_manifest() and \
                            Manifest(os.path.join(path, f)).type() == 'plugin':
                        return True

        return False
