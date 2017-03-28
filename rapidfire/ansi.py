# -*- coding: utf-8 -*-
from .keys import Keys

STYLE = {
    'reset':     0,
    'bold':      1,
    'dim':       2,
    'negative1': 3,
    'underline': 4,
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

# Mapping of escape codes to Keys.
ANSI_SEQUENCES = {
    b'\x1b': Keys.Escape,
    b'\x01': Keys.ControlA,
    b'\x02': Keys.ControlB,
    b'\x03': Keys.ControlC,
    b'\x04': Keys.ControlD,
    b'\x05': Keys.ControlE,
    b'\x06': Keys.ControlF,
    b'\x07': Keys.ControlG,
    b'\x08': Keys.ControlH,
    b'\x09': Keys.ControlI,
    b'\x0a': Keys.ControlJ,
    b'\x0b': Keys.ControlK,
    b'\x0c': Keys.ControlL,
    b'\x0d': Keys.ControlM,
    b'\x0e': Keys.ControlN,
    b'\x0f': Keys.ControlO,
    b'\x10': Keys.ControlP,
    b'\x11': Keys.ControlQ,
    b'\x12': Keys.ControlR,
    b'\x13': Keys.ControlS,
    b'\x14': Keys.ControlT,
    b'\x15': Keys.ControlU,
    b'\x16': Keys.ControlV,
    b'\x17': Keys.ControlW,
    b'\x18': Keys.ControlX,
    b'\x19': Keys.ControlY,
    b'\x1a': Keys.ControlZ,

    b'\x00': Keys.ControlSpace,
    b'\x1c': Keys.ControlBackslash,
    b'\x1d': Keys.ControlSquareClose,
    b'\x1e': Keys.ControlCircumflex,
    b'\x1f': Keys.ControlUnderscore,
    b'\x7f': Keys.Backspace,

    b'\x1b[A': Keys.Up,
    b'\x1b[B': Keys.Down,
    b'\x1b[C': Keys.Right,
    b'\x1b[D': Keys.Left,

    b'\x1b[H': Keys.Home,
    b'\x1bOH': Keys.Home,
    b'\x1b[F': Keys.End,
    b'\x1bOF': Keys.End,
    b'\x1b[3~': Keys.Delete,
    b'\x1b[3;2~': Keys.ShiftDelete,  # xterm, gnome-terminal.
    b'\x1b[3;5~': Keys.ControlDelete,  # xterm, gnome-terminal.
    b'\x1b[1~': Keys.Home,  # tmux
    b'\x1b[4~': Keys.End,  # tmux
    b'\x1b[5~': Keys.PageUp,
    b'\x1b[6~': Keys.PageDown,
    b'\x1b[7~': Keys.Home,  # xrvt
    b'\x1b[8~': Keys.End,  # xrvt
    b'\x1b[Z': Keys.BackTab,  # shift + tab
    b'\x1b[2~': Keys.Insert,

    b'\x1bOP': Keys.F1,
    b'\x1bOQ': Keys.F2,
    b'\x1bOR': Keys.F3,
    b'\x1bOS': Keys.F4,
    b'\x1b[[A': Keys.F1,  # Linux console.
    b'\x1b[[B': Keys.F2,  # Linux console.
    b'\x1b[[C': Keys.F3,  # Linux console.
    b'\x1b[[D': Keys.F4,  # Linux console.
    b'\x1b[[E': Keys.F5,  # Linux console.
    b'\x1b[11~': Keys.F1,  # rxvt-unicode
    b'\x1b[12~': Keys.F2,  # rxvt-unicode
    b'\x1b[13~': Keys.F3,  # rxvt-unicode
    b'\x1b[14~': Keys.F4,  # rxvt-unicode
    b'\x1b[15~': Keys.F5,
    b'\x1b[17~': Keys.F6,
    b'\x1b[18~': Keys.F7,
    b'\x1b[19~': Keys.F8,
    b'\x1b[20~': Keys.F9,
    b'\x1b[21~': Keys.F10,
    b'\x1b[23~': Keys.F11,
    b'\x1b[24~': Keys.F12,
    b'\x1b[25~': Keys.F13,
    b'\x1b[26~': Keys.F14,
    b'\x1b[28~': Keys.F15,
    b'\x1b[29~': Keys.F16,
    b'\x1b[31~': Keys.F17,
    b'\x1b[32~': Keys.F18,
    b'\x1b[33~': Keys.F19,
    b'\x1b[34~': Keys.F20,

    # Xterm
    b'\x1b[1;2P': Keys.F13,
    b'\x1b[1;2Q': Keys.F14,
    # '\x1b[1;2R': Keys.F15,  # Conflicts with CPR response.
    b'\x1b[1;2S': Keys.F16,
    b'\x1b[15;2~': Keys.F17,
    b'\x1b[17;2~': Keys.F18,
    b'\x1b[18;2~': Keys.F19,
    b'\x1b[19;2~': Keys.F20,
    b'\x1b[20;2~': Keys.F21,
    b'\x1b[21;2~': Keys.F22,
    b'\x1b[23;2~': Keys.F23,
    b'\x1b[24;2~': Keys.F24,

    b'\x1b[1;5A': Keys.ControlUp,     # Cursor Mode
    b'\x1b[1;5B': Keys.ControlDown,   # Cursor Mode
    b'\x1b[1;5C': Keys.ControlRight,  # Cursor Mode
    b'\x1b[1;5D': Keys.ControlLeft,   # Cursor Mode

    b'\x1b[1;2A': Keys.ShiftUp,
    b'\x1b[1;2B': Keys.ShiftDown,
    b'\x1b[1;2C': Keys.ShiftRight,
    b'\x1b[1;2D': Keys.ShiftLeft,
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
