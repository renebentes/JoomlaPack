# coding: utf-8
import sublime

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.commands.component import NewComponentCommand
    from JoomlaPack.commands.package import NewPackageCommand
    from JoomlaPack.commands.plugin import NewPluginCommand
    from JoomlaPack.commands.plugin import AddFormToPluginCommand
    from JoomlaPack.commands.plugin import AddFieldToPluginCommand
    from JoomlaPack.commands.plugin import AddInstallScriptToPluginCommand
    from JoomlaPack.commands.plugin import AddTemplateToPluginCommand
    from JoomlaPack.commands.plugin import AddLayoutToPluginCommand
else:
    from commands.component import NewComponentCommand
    from commands.package import NewPackageCommand
    from commands.plugin import NewPluginCommand
    from commands.plugin import AddFormToPluginCommand
    from commands.plugin import AddFieldToPluginCommand
    from commands.plugin import AddInstallScriptToPluginCommand
    from commands.plugin import AddTemplateToPluginCommand
    from commands.plugin import AddLayoutToPluginCommand

__all__ = [
    'NewComponentCommand',

    'NewPackageCommand',

    'NewPluginCommand',
    'AddFormToPluginCommand',
    'AddFieldToPluginCommand',
    'AddInstallScriptToPluginCommand',
    'AddTemplateToPluginCommand',
    'AddLayoutToPluginCommand'
]
