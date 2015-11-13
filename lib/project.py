# coding: utf-8

import sublime
import os

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class Project:

    def root(self):
        '''
        Get the project root define by user or standard.
        '''
        root = Helper().settings('project_root')
        if root is None:
            message = '''[Error] Project root is invalid! Please, check the
                sublime-settings file.'''
            Helper().show_message("error", message)
            return None

        if root == "":
            root = os.path.expanduser("~")

        if not os.path.exists(root):
            message = '''[Error] Project root not exists! Please, check the
                sublime-settings file.'''
            Helper().show_message("error", message)
            return None

        return root

    def get_directories(self):
        '''
        Returns directories for projects.
        '''
        return Helper().window().folders()

    def has_directories(self):
        '''
        Checks if exists folders in project.
        '''
        return len(self.get_directories()) > 0

    def get_project_file(self):
        '''
        Returns the project file name.
        '''
        return Helper().window().project_file_name()

    def get_project_name(self):
        '''
        Returns the project name.
        '''
        return os.path.splitext(os.path.basename(self.get_project_file()))[0]

    def set_project_file(self, path, data):
        '''
        Defines data to project file name.
        '''
        Json('%s.sublime-project' % path).write(data)
        Json('%s..sublime-workspace' % path).write({})

    def get_project_json(self):
        '''
        Returns JSON data from project file.
        '''
        return Helper().window().project_data()

    def set_project_json(self, data):
        '''
        Defines JSON data to project file.
        '''
        return Helper().window().set_project_data(data)

    def has_opened_project(self):
        '''
        Checks if project is opened.
        '''
        return self.get_project_file() is not None

    def has_valid_manifest(self):
        '''
        Checks if Manifest XML file is valid.
        '''
        if self.has_opened_project():
            for f in os.listdir(self.get_directories()[0]):
                if f.endswith('.xml'):
                    return Manifest(os.path.join(self.get_directories()[0],
                                                 f)).is_manifest()
        return False

    def type(self):
        '''
        Returns the project type.
        '''
        if self.has_opened_project() and self.has_valid_manifest():
            for f in os.listdir(self.get_directories()[0]):
                if f.endswith('.xml'):
                    return Manifest(os.path.join(self.get_directories()[0],
                                                 f)).type()
        return None

    def open(self, path):
        '''
        Open project from file name.
        '''
        import subprocess

        if not path.endswith('.sublime-project'):
            path += '.sublime-project'

        executable_path = sublime.executable_path()
        if sublime.platform() == 'osx':
            app_path = executable_path[:executable_path.rfind(".app/") + 5]
            executable_path = app_path + 'Contents/SharedSupport/bin/subl'

        command = [executable_path, '--project ', path]
        sublime.set_timeout_async(
            lambda: subprocess.Popen(command), 10)

    def refresh(self):
        '''
        Updates the project folder.
        '''
        try:
            sublime.set_timeout(
                lambda: Helper().window().run_command('refresh_folder_list'),
                200)
            sublime.set_timeout(
                lambda: Helper().window().run_command('refresh_folder_list'),
                1300)
        except:
            pass
