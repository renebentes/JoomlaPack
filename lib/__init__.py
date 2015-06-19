# coding: utf-8
import sublime

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.helper import Helper
    from JoomlaPack.lib.project import Project
else:
    from lib.helper import Helper
    from lib.project import Project

__all__ = [
    'Helper',
    'Project'
]
