# coding: utf-8
import sublime

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.commands.project import NewProjectCommand
    from JoomlaPack.commands.component import NewComponentCommand
    from JoomlaPack.commands.package import NewPackageCommand
    from JoomlaPack.commands.plugin import NewPluginCommand
    from JoomlaPack.commands.plugin import AddFormToPluginCommand
    from JoomlaPack.commands.plugin import AddFieldToPluginCommand
else:
    from commands.project import NewProjectCommand
    from commands.component import NewComponentCommand
    from commands.package import NewPackageCommand
    from commands.plugin import NewPluginCommand
    from commands.plugin import AddFormToPluginCommand
    from commands.plugin import AddFieldToPluginCommand

__all__ = [
    'NewProjectCommand',

    'NewComponentCommand',

    'NewPackageCommand',

    'NewPluginCommand',
    'AddFormToPluginCommand',
    'AddFieldToPluginCommand'
]
