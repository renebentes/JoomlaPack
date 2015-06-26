# coding: utf-8

import sublime
import os

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib import *
else:
    from lib import *


class Project:

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

    def set_project_file(self, path, name, data):
        JsonFile(path, name + '.sublime-project').save(data)
        JsonFile(path, name + '.sublime-workspace').save({})

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

    def set_session_file(self, path):
        print(os.path.exists(os.path.join(
            sublime.packages_path(),
            '..',
            'Local',
            'Session.sublime_session')
        )
        )

    def has_opened_project(self):
        return self.get_project_file() is not None

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
