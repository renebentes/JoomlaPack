# coding: utf-8
import sublime
import locale
import re


class Helper:

    def window(self):
        '''
        Alias to sublime.active_window() function.
        '''
        return sublime.active_window()

    def settings(self, name, default=None):
        '''
        Get settings contents.
        '''
        settings = sublime.load_settings('Preferences.sublime-settings')
        if settings.get(name, default):
            return settings.get(name, default)
        else:
            settings = sublime.load_settings('JoomlaPack.sublime-settings')
            return settings.get(name, default)

    def language(self):
        '''
        Get the current language of environment.
        '''
        language, enconding = locale.getlocale()
        return language.replace("_", "-")

    def show_input_panel(self, caption, text, on_done=None,
                         on_change=None, on_cancel=None):
        '''
        Alias for sublime.active_window().show_input_panel().
        '''
        return self.window().show_input_panel(
            caption, text, on_done, on_change, on_cancel)

    def show_message(self, dialog, message, ok_title="Ok"):
        ''' Show message dialog based on dialog param. '''
        message = u"Joomla Pack\n\n%s" % message
        if dialog == "confirm":
            return sublime.ok_cancel_dialog(message, ok_title)
        elif dialog == "info":
            return sublime.message_dialog(message)
        elif dialog == "error":
            return sublime.error_message(message)
        elif dialog == "status":
            return sublime.status_message(re.sub('\n\n', ': ',
                                                 message))
        else:
            print(re.sub('\n\n', ': ', message))
            return None

    def on_cancel(self, message='Operation Canceled!'):
        '''
        Displays cancellation message.
        '''
        return self.show_message("", message)
