# coding: utf-8
import sublime
import locale
import re


def window():
    '''
    Alias to sublime.active_window() function.
    '''
    return sublime.active_window()


def settings(name, default=None):
    '''
    Get settings contents.
    '''
    settings = sublime.load_settings('Preferences.sublime-settings')
    if settings.get(name, default):
        return settings.get(name, default)
    else:
        settings = sublime.load_settings('JoomlaPack.sublime-settings')
        return settings.get(name, default)


def language():
    '''
    Get the current language of environment.
    '''
    language, enconding = locale.getlocale()
    return language.replace("_", "-")


def show_input_panel(caption, text, on_done=None,
                     on_change=None, on_cancel=None):
    '''
    Alias for sublime.active_window().show_input_panel().
    '''
    return window().show_input_panel(
        caption, text, on_done, on_change, on_cancel)


def show_message(dialog, message, ok_title="Ok"):
    ''' Show message dialog based on dialog param. '''
    message = u"Joomla Pack\n\n%s" % message
    if dialog == "confirm":
        return sublime.ok_cancel_dialog(message, ok_title)
    elif dialog == "info":
        return sublime.message_dialog(message)
    elif dialog == "error":
        return sublime.error_message(message)
    else:
        return sublime.status_message(re.sub('\n\n', ': ',
                                             message))


def on_cancel(message='Operation Canceled!'):
    '''
    Displays cancellation message.
    '''
    return show_message("", message)


def directories():
    '''
    Get directories for extension project.
    '''
    return window().folders()


def refresh():
    '''
    Refresh the current project directory.
    '''
    try:
        sublime.set_timeout(
            lambda: window().run_command('refresh_folder_list'), 200)
        sublime.set_timeout(
            lambda: window().run_command('refresh_folder_list'), 1300)
    except:
        pass
