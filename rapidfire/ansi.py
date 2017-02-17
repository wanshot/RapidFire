# -*- coding: utf-8 -*-

STYLE = {
    'reset':     0,
    'bold':      1,
    'underline': 2,
    'negative1': 3,
    'negative2': 5,
}

FOREGROUND_COLORS = {
    'black':  30,
    'red':    31,
    'green':  32,
    'yellow': 33,
    'blue':   34,
    'purple': 35,
    'cyan':   36,
    'white':  37,
}

BACKGROUND_COLORS = {
    'black':  40,
    'red':    41,
    'green':  42,
    'yellow': 43,
    'blue':   44,
    'purple': 45,
    'cyan':   46,
    'white':  47,
}


def term(message, section):
    """Display with ANSI Attribute

    :param str message: String to be displayed
    :param dict section: attribute
    :return str: escape sequence character
    """
    style = [0]
    if section.get('style'):
        style = [STYLE.get(s) for s in section['style'].replace(' ', '').split(',')]

    attribute = [
        FOREGROUND_COLORS.get(section.get('fg_color'), 30),
        BACKGROUND_COLORS.get(section.get('bg_color'), 40)
    ] + style

    highlight = ';'.join(map(str, attribute))

    return '\x1b[{attribute}m{char}\x1b[0m'.format(attribute=highlight, char=message)

if __name__ == '__main__':
    for s, _ in sorted(STYLE.items(), key=lambda x: x[1]):
        for fc, _ in sorted(BACKGROUND_COLORS.items(), key=lambda x: x[1]):
            tmp = []
            for bc, _ in sorted(BACKGROUND_COLORS.items(), key=lambda x: x[1]):
                tmp.append(term('test', {'fg_color': fc, 'bg_color': bc, 'style': s}))
            print(' '.join(tmp))
