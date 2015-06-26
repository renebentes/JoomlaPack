# coding: utf-8
import sys
import sublime

st_version = 2

if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3
    from imp import reload

reload_mods = []
for mod in sys.modules:
    if mod[0:10] == 'JoomlaPack' and sys.modules[mod] is not None:
        reload_mods.append(mod)

mod_prefix = ""
if st_version == 3:
    mod_prefix = "JoomlaPack" + mod_prefix

mods_load_order = [
    '',
    '.lib',
    '.lib.file',
    '.lib.folder',
    '.lib.helper',
    '.lib.json_file',
    '.lib.project',

    '.lib.extensions',
    '.lib.extensions.base',
    '.lib.extensions.component',
    '.lib.extensions.package',
    '.lib.extensions.plugin',

    '.lib.inflector',
    '.lib.inflector.base',
    '.lib.inflector.english',

    ".commands",
    ".commands.new_project",
    ".commands.new_component",
    ".commands.new_package",
    ".commands.new_plugin"
]

for suffix in mods_load_order:
    mod = mod_prefix + suffix
    if mod in reload_mods:
        try:
            reload(sys.modules[mod])
        except (ImportError):
            pass
