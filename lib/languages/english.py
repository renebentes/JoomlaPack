# coding: utf-8
import sublime
import re

st_version = int(sublime.version())
if st_version > 3000:
    from JoomlaPack.lib.languages.base import Base
else:
    from lib.languages.base import Base


class English(Base):

    '''
    Inflector for pluralize and singularize English nouns.

    This is the default Inflector for the Inflector obj
    '''

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
        word_lower = word.lower()
        for countable in rules['countable']:
            if word_lower[-1 * len(countable):] == countable:
                return word

        for irregular in rules['irregular'].keys():
            match = re.search('(' + irregular + ')$', word, re.IGNORECASE)
            if match:
                return re.sub('(?i)' + irregular + '$', match.expand('\\1')[0]
                              + rules['irregular']
                              [irregular][1:], word)

        for rule in range(0, len(rules['regular'])):
            match = re.search(rules['regular'][rule][0], word, re.IGNORECASE)
            if match:
                groups = match.groups()
                for k in range(0, len(groups)):
                    if groups[k] is None:
                        rules['regular'][rule][1] = rules['regular'][
                            rule][1].replace('\\' + str(k + 1), '')
                return re.sub(rules['regular'][rule][0],
                              rules['regular'][rule][1],
                              word)

        return word

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
                'moves': 'move',
                'people': 'person',
                # 'pianos': 'piano',
                # 'photos': 'photo',
                # 'pros': 'pro',
                # 'safes': 'safe',
                'sexes': 'sex',
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

        word_lower = word.lower()
        for countable in rules['countable']:
            if word_lower[-1 * len(countable):] == countable:
                return word

        for irregular in rules['irregular'].keys():
            match = re.search('(' + irregular + ')$', word, re.IGNORECASE)
            if match:
                return re.sub('(?i)' + irregular + '$', match.expand('\\1')[0]
                              + rules['irregular']
                              [irregular][1:], word)

        for rule in range(0, len(rules['regular'])):
            match = re.search(rules['regular'][rule][0], word, re.IGNORECASE)
            if match:
                groups = match.groups()
                for k in range(0, len(groups)):
                    if groups[k] is None:
                        rules['regular'][rule][1] = rules['regular'][
                            rule][1].replace('\\' + str(k + 1), '')
                return re.sub(rules['regular'][rule][0],
                              rules['regular'][rule][1],
                              word)

        return word
