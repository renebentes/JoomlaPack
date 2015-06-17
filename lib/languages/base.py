# coding: utf-8
import re


class Base(object):

    '''
    Locale inflectors must inherit from this base class inorder to provide the
    basic Inflector functionality.
    '''

    def conditional_plural(self, word, number=1):
        '''
        Returns the plural form of a word if number parameter is greater than 1.
        '''

        if number > 1:
            return self.pluralize(word)
        else:
            return word

    def humanize(self, word, prefix='id_', suffix='_id'):
        '''
        Returns a human-readable string from word, by replacing underscores with
        a space.
        '''
        return re.sub('^' + prefix, '',
                      re.sub(suffix + '$', '', word)).replace('_', ' ')

    def underscore(self, word):
        '''
        Convert any "CamelCased" or "ordinary Word" into an
        "underscored_word".
        '''
        return re.sub('[^A-Z^a-z^0-9^\/]+', '_',
                      re.sub('([a-z\d])([A-Z])', '\\1_\\2',
                             re.sub('([A-Z]+)([A-Z][a-z])', '\\1_\\2',
                                    re.sub('::', '/', word)))).lower()

    def titleize(self, word, uppercase=''):
        '''
        Converts text like "WelcomePage", "welcome_page" or  "welcome page" to
        this "Welcome Page".

        If uppercase parameter is set to 'first' it will only capitalize the
        first character of the title. Otherwise, the first character of each
        word is capitalized.
        '''

        if uppercase == 'first':
            return self.humanize(self.underscore(word)).capitalize()
        else:
            return self.humanize(self.underscore(word)).title()

    def camelize(self, word):
        '''
        Converts a word like "send_email" or "send email" to "SendEmail".

        It will remove non alphanumeric character from the word, so
        "who's online" will be converted to "WhoSOnline".
        '''
        return ''.join(w[0].upper() + w[1:]
                       for w in re.sub('[^A-Z^a-z^0-9^:]+', ' ',
                                       word).split(' '))

    def variablize(self, word):
        '''
        Converts a word like "send_email" or "send email" to "sendEmail".

        It will remove non alphanumeric character from the word, so
        "who's online" will be converted to "whoSOnline"'''

        word = self.camelize(word)
        return word[0].lower() + word[1:]
