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


class NewComponentCommand(sublime_plugin.WindowCommand):

    def run(self, args):
        source = os.path.join(args["source"], 'contents', 'basic')
        copytree(source, args["destination"])
        self.rename(args)

    def rename(self, args):
        name = args["name"].replace('com_', '')
        for root, dirs, files in os.walk(args["destination"]):
            for filename in files:
                if filename.find('{{component}}') != -1:
                    newname = filename.replace('{{component}}', name)
                elif filename.find('{{singular}}') != -1:
                    newname = filename.replace('{{singular}}', name)
                elif filename.find('{{plural}}') != -1:
                    newname = filename.replace('{{plural}}', pluralize(name))
                elif filename.find('{{locale}}') != -1:
                    newname = filename.replace('{{locale}}', get_language())
                else:
                    newname = ''

                if newname != '':
                    os.rename(os.path.join(root, filename),
                              os.path.join(root, newname))
            for folder in dirs:
                if folder.find('{{singular}}') != -1:
                    newname = folder.replace('{{singular}}', name)
                elif folder.find('{{plural}}') != -1:
                    newname = folder.replace('{{plural}}', pluralize(name))
                elif folder.find('{{locale}}') != -1:
                    newname = filename.replace('{{locale}}', get_language())
                else:
                    newname = ''

                if newname != '':
                    os.rename(os.path.join(root, folder),
                              os.path.join(root, newname))
