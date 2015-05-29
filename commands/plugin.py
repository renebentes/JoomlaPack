# coding: utf-8
import sublime
import sublime_plugin
import os
from shutil import copytree

st_version = int(sublime.version())

if st_version > 3000:
    from JoomlaPack.lib.helpers import *
else:
    from lib.helpers import *


class NewPluginCommand(sublime_plugin.WindowCommand):

    def run(self, args):
        source = os.path.join(args["source"], 'contents')
        copytree(source, args["destination"])

        self.rename(args)

    def rename(self, args):
        name = args["name"].replace('plg_', '')
        for root, dirs, files in os.walk(args["destination"]):
            for filename in files:
                if filename.find('{{plugin}}') != -1:
                    newname = filename.replace('{{plugin}}', name)
                elif filename.find('{{locale}}') != -1:
                    newname = filename.replace('{{locale}}', get_language())
                else:
                    newname = ''

                if newname != '':
                    os.rename(os.path.join(root, filename),
                              os.path.join(root, newname))

            for folder in dirs:
                if folder.find('{{locale}}') != -1:
                    newname = filename.replace('{{locale}}', get_language())
                else:
                    newname = ''

                if newname != '':
                    os.rename(os.path.join(root, folder),
                              os.path.join(root, newname))
