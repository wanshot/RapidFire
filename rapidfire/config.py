
import os
from configparser import ConfigParser

RAPIDFIRE_ROOT_DIRECTORY = os.path.expanduser('~/.rapidfire.d/')
RAPIDFIRE_CONF_PATH = RAPIDFIRE_ROOT_DIRECTORY + 'rfrc'

DEFAULT_CONFIG = """
[base]
RAPIDFIRE_PYFILE_PATH =
SHELL = /bin/sh

[normal line attribute]
FG_COLOR = white
BG_COLOR = black
STYLE =

[select line attribute]
FG_COLOR = yellow
BG_COLOR = red
STYLE = bold

[keymap]
UP = k
DOWN = j
QUITE = q, ESC
ENTER = ENTER
"""

KEY_MAP = {
    'ESC': '\x1b'
}


def make_rapidfire_config():
    if not os.path.exists(RAPIDFIRE_ROOT_DIRECTORY):
        os.makedirs(RAPIDFIRE_ROOT_DIRECTORY)
    with open(RAPIDFIRE_CONF_PATH, 'w+') as f:
        f.write(DEFAULT_CONFIG)


class Config(object):

    def __init__(self):
        if not os.path.exists(RAPIDFIRE_ROOT_DIRECTORY):
            exit('~/.rapidfire.d is not found')
        if not os.path.isfile(RAPIDFIRE_CONF_PATH):
            exit('rfrc is not found')

        self.config = ConfigParser()
        self.config.read(RAPIDFIRE_CONF_PATH)

    def get_key(self, key):
        keys = []
        for key in self.config['keymap'][key].replace(' ', '').split(','):
            if KEY_MAP.get(key):
                keys.append(KEY_MAP[key])
            else:
                keys.append(key)
        return keys

    @property
    def rapidfire_pyfile_path(self):
        return self.config.get('base', 'RAPIDFIRE_PYFILE_PATH')

    @property
    def shell(self):
        return self.config.get('base', 'SHELL')

    @property
    def normal_line_attribute(self):
        return self.config['normal line attribute']

    @property
    def select_line_attribute(self):
        return self.config['select line attribute']



if __name__ == "__main__":
    c = Config()
