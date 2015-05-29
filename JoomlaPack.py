# coding: utf-8
import sublime
import sys
import os

st_version = 2

if sublime.version() == '':
    st_version = 3
    print('Joomla Pack: Please upgrade to Sublime Text 3 build 3012 or newer')
elif int(sublime.version()) > 3000:
    st_version = 3

if st_version == 3:
    installed_dir, _ = __name__.split('.')
elif st_version == 2:
    installed_dir = os.path.basename(os.getcwd())

# Ensure the user has installed Joomla Pack properly
if installed_dir != 'JoomlaPack':
    message = (u"Joomla Pack\n\nThis package appears to be installed " +
               u"incorrectly.\n\nIt should be installed as \"Joomla Pack\", " +
               u"but seems to be installed as \"%s\".\n\n" % installed_dir)
    # If installed unpacked
    if os.path.exists(os.path.join(sublime.packages_path(), installed_dir)):
        message += (u"Please use the Preferences > Browse Packages... menu " +
                    u"entry to open the \"Packages/\" folder and rename" +
                    u"\"%s/\" to \"JoomlaPack/\" " % installed_dir)
    # If installed as a .sublime-package file
    else:
        message += (u"Please use the Preferences > Browse Packages... menu " +
                    u"entry to open the \"Packages/\" folder, then browse up " +
                    u"a folder and into the \"Installed Packages/\" folder." +
                    u"\n\nInside of \"Installed Packages/\", rename " +
                    u"\"%s.sublime-package\" to " % installed_dir +
                    u"\"JoomlaPack.sublime-package\" ")
    message += u"and restart Sublime Text."
    sublime.error_message(message)
else:
    reloader_name = 'reloader'

    # ST3 loads each package as a module, so it needs an extra prefix
    if st_version == 3:
        reloader_name = 'JoomlaPack.' + reloader_name
        from imp import reload

    # Make sure all dependencies are reloaded on upgrade
    if reloader_name in sys.modules:
        reload(sys.modules[reloader_name])

    try:
        # Python 3
        from .commands import *
        from .lib.helpers import *
    except (ValueError):
        # Python 2
        from commands import *
        from lib.helpers import *

    def plugin_loaded():
        print('Joomla Pack loaded')

    def plugin_unloaded():
        print('Joomla Pack Unloaded')

    if st_version == 2:
        plugin_loaded()
