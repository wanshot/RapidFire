
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
BOLD = False
UNDERLINE = False

[select line attribute]
FG_COLOR = white
BG_COLOR = black
BOLD = True
UNDERLINE = True

[keymap]
UP = move_up
DOWN = move_down
QUITE = q, ESC
ENTER = ENTER
"""


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

    @property
    def rapidfire_pyfile_path(self):
        return self.config.get('base', 'RAPIDFIRE_PYFILE_PATH')

    @property
    def shell(self):
        return self.config.get('base', 'SHELL')

    @property
    def normal_line_attribute(self):
        return self.config['normal_line_attribute']

    @property
    def select_line_attribute(self):
        return self.config['select_line_attribute']

    @property
    def keymap(self):
        return self.config['keymap']


if __name__ == "__main__":
    c = Config()
