# coding: utf-8
import sublime

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.helpers import get_language
    from JoomlaPack.lib.helpers import show_input_panel
    from JoomlaPack.lib.helpers import show_message
    from JoomlaPack.lib.helpers import get_settings
    from JoomlaPack.lib.helpers import get_project_root
    from JoomlaPack.lib.helpers import get_templates
    from JoomlaPack.lib.helpers import pluralize
    from JoomlaPack.lib.helpers import singularize
else:
    from lib.helpers import get_language
    from lib.helpers import show_input_panel
    from lib.helpers import show_message
    from lib.helpers import get_settings
    from lib.helpers import get_project_root
    from lib.helpers import get_templates
    from lib.helpers import pluralize
    from lib.helpers import singularize
    from lib.project import Project

__all__ = [
    'get_language',
    'show_input_panel',
    'show_message',
    'get_settings',
    'get_project_root',
    'get_templates',
    'pluralize',
    'singularize',
    'Project'
]
