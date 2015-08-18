# coding: utf-8
import sublime
import os
from shutil import copytree, rmtree

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class Base(object):

    """Joomla's extensions types must inherit from this base class inorder
    to provide basic functionality."""

    def __init__(self, inflector):
        self.inflector = inflector()

    def path(self, path):
        '''
        Defines path to extensions.
        '''
        self.path = os.path.join(Project().root(), path)

    def create(self):
        '''
        Creates structure to extensions.
        '''

        if Project().type() == 'package':
            self.path(os.path.join(Project().get_directories()[0],
                                   'packages', self.fullname))
        else:
            self.path(self.fullname)

        if os.path.exists(self.path):
            if not Helper().show_message("confirm",
                                         "[Confirm] Project %s already exists!"
                                         % self.fullname,
                                         "Delete and overwrite"):
                return False
            else:
                rmtree(self.path)

        try:
            self.get_template()
            if self.template_path is not None:
                copytree(self.template_path, self.path)
                self.rename()
            return True
        except Exception as e:
            rmtree(self.path)
            Helper().show_message("error",
                                  "[Error] Project %s could not be created! %s"
                                  % (self.fullname, e))
            return False

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
            Helper().show_message("error", message)
            self.template_path = None

    def add_folder(self, name):
        """Adds folders on Joomla! Extensions.

        Args:
            name (str): Name of folder

        Returns:
            bool: True on success, false otherwise.
        """
        return Folder(os.path.join(self.path, name)).create()

    def add_file(self, name, data):
        """Adds files on Joomla! Extensions.

        Args:
            name (str): Name of file
            data (str): Data of file

        Returns:
            bool: True on success, false otherwise.
        """
        return File(os.path.join(self.path, name)).write(data)

    def set_project(self):
        """Defines and open project extensions."""
        data = {
            "folders": [{"follow_symlinks": True, "path": self.path}],
            "settings": [{"tab_size": 2, "translate_tabs_to_spaces": True}]
        }

        Project().set_project_file(os.path.join(self.path,
                                                self.inflector.variablize(
                                                    self.fullname)),
                                   data)
        Project().open(os.path.join(self.path,
                                    self.inflector.variablize(
                                        self.fullname)))
