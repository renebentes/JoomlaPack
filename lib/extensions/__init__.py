import sublime

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.extensions.component import Component
    from JoomlaPack.lib.extensions.package import Package
    from JoomlaPack.lib.extensions.plugin import Plugin
else:
    from lib.extensions.component import Component
    from lib.extensions.package import Package
    from lib.extensions.plugin import Plugin

__all__ = [
    'Component',
    'Package',
    'Plugin'
]
