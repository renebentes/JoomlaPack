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

    '''
    Joomla's extensions types must inherit from this base class inorder
    to provide basic functionality.
    '''

    def __init__(self, inflector):
        self.inflector = inflector()

    def path(self, path=None):
        if path is not None:
            self.path = os.path.join(Project().root(), path)
        else:
            self.path = Project().get_directories()

    def create(self):
        '''
        Creates structure to extensions.
        '''
        self.path(self.fullname)
        if os.path.exists(self.path):
            if not Helper().show_message("confirm",
                                         "[Confirm] Project %s already exists!"
                                         % self.fullname,
                                         "Delete and overwrite"):
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
            Helper().show_message("error",
                                  "[Error] Project %s could not be created! %s"
                                  % (self.fullname, e))
        else:
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
