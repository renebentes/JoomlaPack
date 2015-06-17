# coding: utf-8
import sys
import sublime

st_version = 3

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

    '.lib.helpers',

    '.lib.project',
    '.lib.project.extensions',
    '.lib.project.extensions.base',
    '.lib.project.extensions.component',
    '.lib.project.extensions.package',
    '.lib.project.extensions.plugin',

    '.lib.inflector',
    '.lib.inflector.languages',
    '.lib.inflector.languages.base',
    '.lib.inflector.languages.english',

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
