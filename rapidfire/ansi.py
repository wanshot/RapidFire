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


def term(message, fg_color=None, bg_color=None, style=None):
    """Display with ANSI Attribute

    :param str message: String to be displayed
    :param str fg_color: text color
    :param str bg_color: background color
    :param str style: text style
    :return str: escape sequence character
    """
    style = STYLE.get(style, 0)
    fg_color = FOREGROUND_COLORS.get(fg_color, 30)
    bg_color = BACKGROUND_COLORS.get(bg_color, 40)

    highlight = ';'.join(map(str, [style, fg_color, bg_color]))

    return u'\x1b[{attribute}m{char}\x1b[0m'.format(attribute=highlight,
                                                    char=message)

if __name__ == '__main__':
    for s, _ in sorted(STYLE.items(), key=lambda x: x[1]):
        for fc, _ in sorted(BACKGROUND_COLORS.items(), key=lambda x: x[1]):
            tmp = []
            for bc, _ in sorted(BACKGROUND_COLORS.items(), key=lambda x: x[1]):
                tmp.append(term('test', fg_color=fc, bg_color=bc, style=s))
            print(' '.join(tmp))
