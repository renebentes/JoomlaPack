# coding: utf-8
import sublime

VERSION = int(sublime.version())
if VERSION > 3000:
    from JoomlaPack.commands.project import NewProjectCommand
    from JoomlaPack.commands.component import NewComponentCommand
else:
    from commands.project import NewProjectCommand
    from commands.component import NewComponentCommand

__all__ = [
    'NewProjectCommand',
    'NewComponentCommand'
]
