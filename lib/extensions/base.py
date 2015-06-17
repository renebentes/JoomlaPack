# coding: utf-8
import sublime
import json
import os
from shutil import copytree, rmtree

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.helpers import *
else:
    from lib.helpers import *


class Base(object):

    '''
    Joomla's extensions types must inherit from this base class inorder
    to provide basic functionality.
    '''

    def get_root(self):
        '''
        Get the project root define by user or standard.
        '''
        root = settings('project_root')
        if root is None:
            message = '''[Error] Project root is invalid! Please, check the
                sublime-settings file.'''
            show_message("error", message)
            return None

        if root == "":
            root = os.path.expanduser("~")

        if not os.path.exists(root):
            message = '''[Error] Project root not exists! Please, check the
                sublime-settings file.'''
            show_message("error", message)
            return None

        return root

    def write(self, name, content):
        '''
        Write files on disk.
        '''
        with open(os.path.join(self.path, name), 'w+',
                  encoding='utf8', newline='') as f:
            f.write(str(content))

        # Fixes as best as possible a new file permissions issue
        # See https://github.com/titoBouzout/SideBarEnhancements/issues/203
        # See https://github.com/SublimeTextIssues/Core/issues/239
        if 3000 <= st_version < 3088:
            oldmask = os.umask(0o000)
            if oldmask == 0:
                os.chmod(self.path, 0o644)
            os.umask(oldmask)

    def make_dir(self, name):
        '''
        Creates structure folder to extensions.
        '''
        data = '''<!DOCTYPE html>
            <html>
            <head>
                <title>&nbsp;</title>
            </head>
            <body></body>
            </html>'''
        folder = os.path.join(self.path, name)
        try:
            os.makedirs(folder, 0o755)
            self.write('index.html', data)
        except Exception as e:
            show_message("error",
                         "[Error] Folder %s could not be created! %s"
                         % (folder, e))

    def path(self, path=None):
        if path is not None:
            self.path = os.path.join(self.get_root(), path)
        else:
            self.path = directories()

    def create(self):
        '''
        Creates structure to extensions.
        '''
        self.path(self.fullname)
        if os.path.exists(self.path):
            if not show_message("confirm",
                                "[Confirm] Project %s already exists!"
                                % self.fullname, "Delete and overwrite"):
                return
            else:
                rmtree(self.path)

        try:
            self.get_template()
            if self.template_path is not None:
                copytree(self.template_path, self.path)
                self.rename()
        except Exception as e:
            rmtree(self.path)
            show_message("error",
                         "[Error] Project %s could not be created! %s"
                         % (self.fullname, e))
        else:
            self.save_project_file()

    def get_template(self):
        '''
        Gets the template path to extension.
        '''
        packages_path = sublime.packages_path()
        installed_packages_path = sublime.installed_packages_path()
        self.template_path = 'JoomlaPack/templates/' + self.template_path

        if os.path.exists(os.path.join(packages_path, self.template_path)):
            self.template_path = os.path.join(
                packages_path, self.template_path)
        elif os.path.exists(os.path.join(installed_packages_path,
                                         self.template_path)):
            self.template_path = os.path.join(
                installed_packages_path, self.template_path)
        else:
            message = '[Error] No such folder: "%s" or "%s"!' % (
                os.path.join(packages_path, self.template_path),
                os.path.join(installed_packages_path, self.template_path))
            show_message("error", message)
            self.template_path = None

    def save_project_file(self):
        '''
        Save the project file to extension.
        '''
        data = {
            "folders": [{"follow_symlinks": True, "path": self.path}],
            "settings": [{"tab_size": 2, "translate_tabs_to_spaces": True}]
        }

        try:
            self.write(self.inflector.variablize(self.fullname) +
                       '.sublime-project', json.dumps(data, sort_keys=True,
                                                      indent=2))
        except (Exception, IOError) as e:
            show_message("error",
                         '''[Error] %s.sublime-project could not
                              be created! %s''' % (self.fullname, e))
        else:
            window().set_project_data(data)
