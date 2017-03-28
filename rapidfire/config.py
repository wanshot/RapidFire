import os
from configparser import ConfigParser

HOME = os.path.expanduser('~')
RAPIDFIRE_CONF_DIRECTORY = os.path.join(HOME, '.rapidfire.d')
RAPIDFIRE_CONF_PATH = os.path.join(RAPIDFIRE_CONF_DIRECTORY, 'raprc')

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
UP = <Up>
DOWN = <Down>
QUITE = <Escape>
ENTER = <C-J>, <C-M>
ERASE_CHAR = <Backspace>
"""


def make_rapidfire_config():
    if not os.path.exists(RAPIDFIRE_CONF_DIRECTORY):
        os.makedirs(RAPIDFIRE_CONF_DIRECTORY)
    with open(RAPIDFIRE_CONF_PATH, 'w+') as f:
        f.write(DEFAULT_CONFIG)


class Config(object):

    def __init__(self):
        if not os.path.exists(RAPIDFIRE_CONF_DIRECTORY):
            exit('No such .rapidfire.d')
        if not os.path.isfile(RAPIDFIRE_CONF_PATH):
            exit('No such raprc')

        self.config = ConfigParser()
        self.config.read(RAPIDFIRE_CONF_PATH)
        if not os.path.isfile(self.rapidfire_pyfile_path):
            exit('File set in RAPIDFIRE_PYFILE_PATH of raprc can not be found')
        if not os.access(self.rapidfire_pyfile_path, os.R_OK):
            exit('%s Permission denied' % self.rapidfire_pyfile_path)

    def get_keys(self, operate):
        keys = []
        for key in self.config['keymap'][operate].replace(' ', '').split(','):
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
