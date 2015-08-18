# coding: utf-8
import sys
import sublime

st_version = 2

if sublime.version() == '' or int(sublime.version()) > 3000:
    st_version = 3
    from imp import reload

mod_prefix = ''
reload_mods = []

for mod in sys.modules:
    if mod.startswith('JoomlaPack') and sys.modules[mod] is not None:
        reload_mods.append(mod)

if st_version == 3:
    mod_prefix = 'JoomlaPack' + mod_prefix

mods_load_order = [
    '',

    '.lib',

    '.lib.inflector',
    '.lib.inflector.base',
    '.lib.inflector.english',

    '.lib.file',
    '.lib.folder',
    '.lib.helper',
    '.lib.json',
    '.lib.manifest',
    '.lib.project',

    '.lib.extensions',
    '.lib.extensions.base',
    '.lib.extensions.component',
    '.lib.extensions.package',
    '.lib.extensions.plugin',

    '.commands',
    '.commands.component',
    '.commands.package',
    '.commands.plugin'
]

for mod in mods_load_order:
    mod = mod_prefix + mod
    if mod in reload_mods:
        try:
            reload(sys.modules[mod])
        except ImportError as e:
            sublime.error_message('Joomla Pack\n\n[Error] Modules could not ' +
                                  'be imported! %s' % e)
