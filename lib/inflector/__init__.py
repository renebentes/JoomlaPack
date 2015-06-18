# coding: utf-8
import sublime

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.inflector.english import English
else:
    from lib.inflector.english import English

__all__ = [
    'English'
]
