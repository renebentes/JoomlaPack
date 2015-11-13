# coding: utf-8
import sublime
import re

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.inflector.base import Base
else:
    from lib.inflector.base import Base


class English(Base):

    '''
    Inflector for pluralize and singularize English nouns.

    This is the default Inflector
    '''

    def __init__(self):
        Base.__init__(self)

    def pluralize(self, word):
        '''
        Pluralizes English nouns.
        '''
        rules = {
            'regular': [
                ['(?i)(on)$', 'a'],
                ['(?i)(alumn|alg)a$', '\\1ae'],
                ['(?i)([ti])um$', '\\1a'],
                ['(?i)(ndum)$', 'nda'],
                ['(?i)(gen|visc)us$', '\\1era'],
                ['(?i)(corp)us$', '\\1ora'],
                ['(?i)(octop|vir|alumn|bacill|cact|foc|fung)us$', '\\1i'],
                ['(?i)(loc|nucle|radi|stimul|styl|succub)us$', '\\1i'],
                ['(?i)(syllab|termin|tor)us$', '\\1i'],
                ['(?i)(us)$', '\\1es'],
                ['(?i)(matr|vert|ind)(ix|ex)$', '\\1ices'],
                ['(?i)([m|l])ouse$', '\\1ice'],
                ['(?i)(hive)$', '\\1s'],
                ['(?i)(s|t|x)is$', '\\1es'],
                ['^(?i)(ox)$', '\\1en'],
                ['(?i)(quiz)$', '\\1zes'],
                ['(?i)(?:([^f])fe|([aelor])f)$', '\\1\\2ves'],
                ['(?i)(([p|m]atriar|monar|stoma|con|epo)ch)$', '\\1s'],
                ['(?i)(x|ch|s|ss|sh|z)$', '\\1es'],
                ['(?i)([^aeiouy]o)$', '\\1es'],
                ['(?i)([^aeiouy]|qu)y$', '\\1ies'],
                ['(?i)$', 's']
            ],
            'irregular': {
                'albino': 'albinos',
                'armadillo': 'armadillos',
                'auto': 'autos',
                'cello': 'cellos',
                'chief': 'chiefs',
                'child': 'children',
                'combo': 'combos',
                'ego': 'egos',
                'foot': 'feet',
                'goose': 'geese',
                'halo': 'halos',
                'inferno': 'infernos',
                'lasso': 'lassos',
                'man': 'men',
                'memento': 'mementos',
                'memo': 'memos',
                'person': 'people',
                'piano': 'pianos',
                'photo': 'photos',
                'pro': 'pros',
                'safe': 'safes',
                'sex': 'sexes',
                'silo': 'silos',
                'solo': 'solos',
                'staff': 'staves',
                'taco': 'tacos',
                'tooth': 'teeth',
                'tuxedo': 'tuxedos',
                'typo': 'typos',
                'veto': 'vetos',
                'yo': 'yos'
            },
            'countable': [
                'aircraft',
                'cannon',
                'deer',
                'elk',
                'equipment',
                'fish',
                'glasses',
                'information',
                'money',
                'moose',
                'news',
                'pants',
                'pliers',
                'politics',
                'rice',
                'savings',
                'scissors',
                'series',
                'sheep',
                'species',
                'swine'
            ]
        }

        word = word.lower()

        for key, value in self.cache.items():
            if word == key or word == value:
                return value

        if word in rules['countable']:
            self.cache[word] = word
            return word

        for key, value in rules['irregular'].items():
            if word == key or word == value:
                self.cache[key] = value
                return value

        for rule in range(0, len(rules['regular'])):
            match = re.search(rules['regular'][rule][0], word,
                              re.IGNORECASE)
            if match:
                groups = match.groups()
                for k in range(0, len(groups)):
                    if groups[k] is None:
                        rules['regular'][rule][1] = rules['regular'][
                            rule][1].replace('\\' + str(k + 1), '')
                self.cache[word] = re.sub(rules['regular'][rule][0],
                                          rules['regular'][rule][1],
                                          word)
                return self.cache[word]

        return Base.pluralize(self, word)

    def singularize(self, word):
        '''
        Singularizes English nouns.
        '''
        rules = {
            'regular': [
                ['(?i)([ti])a$', '\\1um'],
                ['(?i)(alumn|alg)ae$', '\\1a'],
                ['(?i)^(ox)en', '\\1'],
                ['(?i)a$', 'on'],
                ['(?i)(nda)$', 'ndum'],
                ['(?i)(gen|visc)era$', '\\1us'],
                ['(?i)(corp)ora$', '\\1us'],
                ['(?i)(octop|vir|alumn|bacill|cact|foc|fung)i$', '\\1us'],
                ['(?i)(loc|nucle|radi|stimul|styl|succub)i$', '\\1us'],
                ['(?i)(syllab|termin|tor)i$', '\\1us'],
                ['(?i)(quiz)zes$', '\\1'],
                ['(?i)([m|l])ice$', '\\1ouse'],
                ['(?i)(matr)ices$', '\\1ix'],
                ['(?i)(vert|ind)ices$', '\\1ex'],
                ['(?i)(test|ax|cris)es$', '\\1is'],
                ['(?i)(m)ovies$', '\\1ovie'],
                ['(?i)([aelor])ves$', '\\1f'],
                ['(?i)(tive)s$', '\\1'],
                ['(?i)(hive)s$', '\\1'],
                ['(?i)([^f])ves$', '\\1fe'],
                ['(?i)(x|ch|ss|sh|zz)es$', '\\1'],
                ['(?i)([^aeiouy]|qu)ies$', '\\1y'],
                ['(?i)((a)naly|(b)a|(d)iagno|(p)arenthe)ses$', '\\1sis'],
                ['(?i)((p)rogno|(s)ynop|(t)he)ses$', '\\1\\2sis'],
                ['(?i)(penis|alias|status)es$', '\\1'],
                ['(?i)(bus)es$', '\\1'],
                ['(?i)(shoe)s$', '\\1'],
                ['(?i)(o)es$', '\\1'],
                ['(?i)s$', '']
            ],
            'irregular': {
                # 'albinos': 'albino',
                # 'armadillos': 'armadillo',
                # 'autos': 'auto',
                # 'cellos': 'cello',
                # 'chiefs': 'chief',
                'children': 'child',
                # 'combos': 'combo',
                # 'egos': 'ego',
                'feet': 'foot',
                'geese': 'goose',
                # 'halos': 'halo',
                # 'infernos': 'inferno',
                # 'lassos': 'lasso',
                'men': 'man',
                # 'mementos': 'memento',
                # 'memos': 'memo',
                # 'moves': 'move',
                'people': 'person',
                # 'pianos': 'piano',
                # 'photos': 'photo',
                # 'pros': 'pro',
                # 'safes': 'safe',
                # 'sexes': 'sex',
                # 'silos': 'silo',
                # 'solos': 'solo',
                'staves': 'staff',
                # 'tacos': 'taco',
                'teeth': 'tooth',
                # 'tuxedos': 'tuxedo',
                # 'typos': 'typo',
                # 'vetos': 'veto',
                # 'yos': 'yo'
            },
            'countable': [
                'aircraft',
                'cannon',
                'deer',
                'elk',
                'equipment',
                'fish',
                'glasses',
                'information',
                'money',
                'moose',
                'news',
                'pants',
                'pliers',
                'politics',
                'rice',
                'savings',
                'scissors',
                'series',
                'sheep',
                'species',
                'swine'
            ]
        }

        word = word.lower()

        for key, value in self.cache.items():
            if word == key or word == value:
                return key

        if word in rules['countable']:
            self.cache[word] = word
            return word

        for key, value in rules['irregular'].items():
            if word == key or word == value:
                self.cache[value] = key
                return value

        for rule in range(0, len(rules['regular'])):
            match = re.search(rules['regular'][rule][0], word)
            if match is not None:
                groups = match.groups()
                for k in range(0, len(groups)):
                    if groups[k] is None:
                        rules['regular'][rule][1] = rules['regular'][
                            rule][1].replace('\\' + str(k + 1), '')

                key = re.sub(rules['regular'][rule][0],
                             rules['regular'][rule][1],
                             word)
                self.cache[key] = word
                return key

        return Base.singularize(self, word)

    def __str__(self):
        return "JoomlaPack: English Inflector"
