# coding: utf-8
import sublime
import os
import re
import locale


def get_language():
    language, enconding = locale.getlocale()
    return language.replace("_", "-")


def show_input_panel(caption, text, on_done, on_change, on_cancel):
    ''' Alias for sublime.active_window().show_input_panel(). '''
    sublime.active_window().show_input_panel(
        caption, text, on_done, on_change, on_cancel)


def show_message(dialog, msg):
    ''' Show message dialog based on dialog param. '''
    msg = u"Joomla Pack\n\n%s" % msg
    if dialog == "confirm":
        return sublime.ok_cancel_dialog(msg)
    elif dialog == "info":
        sublime.message_dialog(msg)
    elif dialog == "error":
        sublime.error_message(msg)
    else:
        sublime.status_message(msg)


def get_settings(name, default=None):
    ''' Get settings contents '''
    settings = sublime.load_settings('JoomlaPack.sublime-settings')
    return settings.get(name, default)


def get_project_root():
    ''' Get the project root define by user or standard. '''
    project_root = get_settings('project_root')
    if project_root is None:
        message = '''[Error] Project root is invalid! Please, check the
            sublime-settings file.'''
        show_message("error", message)
        return
    project_root = project_root.replace("", os.path.expanduser("~"))
    return project_root


def get_templates():
    ''' Gets the templates for Joomla's extensions types. '''
    packages_path = sublime.packages_path()
    installed_packages_path = sublime.installed_packages_path()
    templates_path = 'JoomlaPack/templates'
    templates = {}
    try:
        for k in os.listdir(os.path.join(packages_path, templates_path)):
            templates[k] = os.path.join(packages_path, templates_path, k)
    except IOError:
        try:
            for k in os.listdir(os.path.join(installed_packages_path,
                                             templates_path)):
                templates[k] = os.path.join(installed_packages_path,
                                            templates_path, k)
        except:
            message = "[Error] No such folder: %s or %s!" % (
                os.path.join(packages_path, templates_path),
                os.path.join(installed_packages_path, templates_path))
            show_message("error", message)
    finally:
        return templates


def pluralize(word):
    ''' Pluralize English's words. '''
    rules = {
        'regular': [
            ['(?i)(on)$', 'a'],
            ['(?i)(alumn|alg)a$', '\\1ae'],
            ['(?i)([ti])um$', '\\1a'],
            ['(?i)(ndum)$', 'nda'],
            ['(?i)(gen|visc)us$', '\\1era'],
            ['(?i)(corp)us$', '\\1ora'],
            ['(?i)(octop|vir|alumn|bacill|cact|foc|fung)us$', '\\1i'],
            ['(?i)(styl|succub|loc|nucle|radi|stimul)us$', '\\1i'],
            ['(?i)(syllab|termin|tor)us$', '\\1i'],
            ['(?i)(i|e)x$', 'ices'],
            ['(?i)([m|l])ouse$', '\\1ice'],
            ['(?i)(is)$', 'es'],
            ['(?i)(m)an$', '\\1en'],
            ['(?i)(quiz)$', '\\1zes'],
            ['(?i)(?:([^f])fe|([lar])f)', '\\1\\2ves'],
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
            'child': 'children',
            'combo': 'combos',
            'ego': 'egos',
            'foot': 'feet',
            'german': 'germans',
            'goose': 'geese',
            'halo': 'halos',
            'hoof': 'hooves',
            'inferno': 'infernos',
            'lasso': 'lassos',
            'memento': 'mementos',
            'memo': 'memos',
            'ox': 'oxen',
            'person': 'people',
            'piano': 'pianos',
            'photo': 'photos',
            'pro': 'pros',
            'roman': 'romans',
            'sex': 'sexes',
            'silo': 'silos',
            'solo': 'solos',
            'taco': 'tacos',
            'tooth': 'teeth',
            'tuxedo': 'tuxedos',
            'typo': 'typos',
            'veto': 'vetoes',
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
            'rice',
            'series',
            'sheep'
            'species',
            'swine'
        ]
    }

    word_lower = word.lower()
    for countable in rules['countable']:
        if word_lower == countable:
            return word

    for irregular in rules['irregular'].keys():
        if word_lower == irregular.lower():
            return rules['irregular'][irregular]

    for rule in range(len(rules['regular'])):
        match = re.search(rules['regular'][rule][0], word_lower, re.IGNORECASE)
        if match:
            groups = match.groups()
            for k in range(0, len(groups)):
                if groups[k] is None:
                    rules['regular'][rule][1] = rules['regular'][rule][
                        1].replace('\\' + str(k + 1), '')

            return re.sub(rules['regular'][rule][0], rules['regular'][rule][1],
                          word)

    return word


def singularize(word):
    ''' Singulrize English's words. '''
    pass
