# coding: utf-8
import sublime

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.languages.english import English
else:
    from languages.english import English


class Inflector(object):

    '''
    inflector for pluralizing and singularizing nouns.

    It provides methods for helping on creating programs
    based on naming conventions like on Ruby on Rails.
    '''

    def __init__(self, inflector=English):
        self.cache = {
            'singularized': {},
            'pluralized': {}
        }

        assert callable(inflector), "inflector should be a callable obj"
        self._inflector = inflector()

    def is_singular(self, word):
        '''
        Check to see if a word is singular.
        '''
        singular = self.cache['singularized'][
            word] if word in self.cache['singularized'].keys() else None

        plural = self.cache['pluralized'][singular] \
            if (singular and singular in self.cache[
                'pluralized'].keys()) \
            else None

        if singular and plural:
            return plural != word

        return self.singularize(self.pluralize(word)) == word

    def is_plural(self, word):
        '''
        Check to see if a word is plural.
        '''
        plural = self.cache['pluralized'][word] if word in self.cache[
            'pluralized'].keys() else None

        singular = self.cache['singularized'][plural] if plural and \
            plural in self.cache['singularized'].keys() else None

        if plural and singular:
            return singular != word

        return self.pluralize(self.singularize(word)) == word

    def singularize(self, word):
        '''
        Singularize nouns.
        '''
        if word in self.cache['singularized'].keys():
            return self.cache['singularized'][word]
        self.cache['singularized'][word] = self._inflector.singularize(word)
        return self.cache['singularized'][word]

    def pluralize(self, word):
        '''
        Pluralizes nouns.
        '''
        if word in self.cache['pluralized'].keys():
            return self.cache['pluralized'][word]
        self.cache['pluralized'][word] = self._inflector.pluralize(word)
        return self.cache['pluralized'][word]

    def conditional_plural(self, word, number):
        '''
        Returns the plural form of a word if number parameter is greater than 1.
        '''
        return self._inflector.conditional_plural(word, number)

    def humanize(self, word, prefix='id_', suffix='_id'):
        '''
        Returns a human-readable string from word, by replacing underscores with
        a space.
        '''
        return self._inflector.humanize(word, prefix, suffix)

    def underscore(self, word):
        '''
        Convert any "CamelCased" or "ordinary Word" into an
        "underscored_word".
        '''
        return self._inflector.underscore(word)

    def titleize(self, word, uppercase=''):
        '''
        Converts text like "WelcomePage", "welcome_page" or  "welcome page" to
        this "Welcome Page".

        If uppercase parameter is set to 'first' it will only capitalize the
        first character of the title. Otherwise, the first character of each
        word is capitalized.
        '''

        return self._inflector.titleize(word, uppercase)

    def camelize(self, word):
        '''
        Converts a word like "send_email" or "send email" to "SendEmail".

        It will remove non alphanumeric character from the word, so
        "who's online" will be converted to "WhoSOnline".
        '''
        return self._inflector.camelize(word)

    def variablize(self, word):
        '''
        Converts a word like "send_email" or "send email" to "sendEmail".

        It will remove non alphanumeric character from the word, so
        "who's online" will be converted to "whoSOnline".
        '''
        return self._inflector.variablize(word)
