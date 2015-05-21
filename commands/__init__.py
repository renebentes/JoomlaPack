# coding: utf-8
import sublime

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.commands.project import NewProjectCommand
    from JoomlaPack.commands.component import NewComponentCommand
    from JoomlaPack.commands.package import NewPackageCommand
else:
    from commands.project import NewProjectCommand
    from commands.component import NewComponentCommand
    from commands.package import NewPackageCommand

__all__ = [
    'NewProjectCommand',
    'NewComponentCommand',
    'NewPackageCommand'
]
