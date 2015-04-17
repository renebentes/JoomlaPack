# coding: utf-8
import sys
import sublime

VERSION = 2

if sublime.version() == '' or int(sublime.version()) > 3000:
    VERSION = 3
    from imp import reload

reload_mods = []
for mod in sys.modules:
    if mod[0:10] == 'JoomlaPack' and sys.modules[mod] is not None:
        reload_mods.append(mod)

mod_prefix = ""
if VERSION == 3:
    mod_prefix = "JoomlaPack." + mod_prefix

mods_load_order = [
    '',
    '.lib'
    '.lib.helpers',
    '.lib.project',

    ".commands",
    ".commands.new_project",
    ".commands.new_component"
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        try:
            reload(sys.modules[mod])
        except (ImportError):
            pass
