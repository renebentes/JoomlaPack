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
        return self.get_project_file() is not None

    def write_file(self, path, name, content):
        '''
        Write files on disk.
        '''
        with open(os.path.join(path, name), 'w+',
                  encoding='utf8') as f:
            f.write(content)

        # Fixes as best as possible a new file permissions issue
        # See https://github.com/titoBouzout/SideBarEnhancements/issues/203
        # See https://github.com/SublimeTextIssues/Core/issues/239
        if 3000 <= st_version < 3088:
            oldmask = os.umask(0o000)
            if oldmask == 0:
                os.chmod(path, 0o644)
            os.umask(oldmask)

    def make_dir(self, path, name):
        '''
        Creates structure folder to extensions.
        '''
        data = '<!DOCTYPE html>'
        data += '<html>'
        data += '<head>'
        data += '  <title>&nbsp;</title>'
        data += '</head>'
        data += '<body></body>'
        data += '</html>'
        folder = os.path.join(path, name)
        try:
            if 3000 <= st_version < 3088:
                # Fixes as best as possible a new directory permissions issue
                # See:
                # https://github.com/titoBouzout/SideBarEnhancements/issues/203
                # https://github.com/SublimeTextIssues/Core/issues/239
                oldmask = os.umask(0o000)
                if oldmask == 0:
                    os.makedirs(path, 0o755)
                else:
                    os.makedirs(path)
                os.umask(oldmask)
            else:
                os.makedirs(folder)
            self.write(folder, 'index.html', data)
        except Exception as e:
            Helper().show_message("error",
                                  "[Error] Folder %s could not be created! %s"
                                  % (folder, e))

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
