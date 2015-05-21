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


class NewPackageCommand(sublime_plugin.WindowCommand):

    def run(self, args):
        source = os.path.join(args["source"], 'contents')
        copytree(source, args["destination"])

        self.rename(args)

    def rename(self, args):
        name = args["name"].replace('pkg_', '')
        for root, dirs, files in os.walk(args["destination"]):
            for filename in files:
                if filename.find('{{package}}') != -1:
                    newname = filename.replace('{{package}}', name)

                if newname != '':
                    os.rename(os.path.join(root, filename),
                              os.path.join(root, newname))
