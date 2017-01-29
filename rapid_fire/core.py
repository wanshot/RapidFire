# -*- coding: utf-8 -*-
import os
import sys
import termios
import tty
import subprocess
import locale
import types

from .ansi import term
from .terminalsize import get_terminal_size
from .parser import ParsePyFile

ESC = '\x1b'
FINISH_KEYS = ['q', ESC]


def get_locale():
    locale.setlocale(locale.LC_ALL, '')
    output_encoding = locale.getpreferredencoding()
    return output_encoding


class Core(object):

    def __init__(self, function, action_name=None, input_encoding=None, **kwargs):
        data = function()
        function_name = function.__name__

        try:
            _ = (x for x in data)
        except:
            sys.exit()

        encoding = get_locale()
        with RapidFire(encoding, data, function_name, input_encoding, kwargs) as rf:
            exit_code = rf.loop()
        sys.exit(exit_code)


class RapidFire(object):

    def __init__(self, output_encodeing, data, function_name, input_encoding='utf-8', kwargs=None):
        self.pos = 0
        self.data = data
        self.function_name = function_name
        self.width, self.height = get_terminal_size()
        self.output_encodeing = output_encodeing
        self.input_encoding = input_encoding
        self.args_for_action = None
        self.max_lines_range = len(data)
        self.next_action = kwargs.get('next_action')

    def __enter__(self):
        ttyname = get_ttyname()
        sys.stdin = open(ttyname)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write('\x1b[?25h\x1b[0J')
        if self.next_action:
            rf_parser = ParsePyFile('/Users/wan/rffile.py')
            rf_parser.set_code_obj(self.next_action)
            for const in rf_parser.code_obj.co_consts:
                # XXX get only action method code object
                if isinstance(const, types.CodeType):
                    rf_parser.set_rf_module(const)
                    exec(rf_parser.code_obj, {
                        # set globals
                        self.function_name: self.args_for_action,
                    })
        else:
            if self.args_for_action:
                self.execute_command()

    def loop(self):
        self.render()
        while True:
            try:
                ch = get_char()

                if ch in FINISH_KEYS:
                    break
                elif ch == 'k':
                    if self.pos > 0:
                        self.pos -= 1
                elif ch == 'j':
                    if self.pos < self.max_lines_range - 1:
                        self.pos += 1
                elif ch == '\n':
                    self.args_for_action = self.data[self.pos]
                    break

                self.render()
            except:
                sys.stdout.write('\x1b[?0h\x1b[0J')

        return 1

    def render(self):
        reset = '\x1b[0K\x1b[0m'
        sys.stdout.write('\x1b[?25l')  # hide cursor
        for idx, line in enumerate(self.data):
            line.encode(self.output_encodeing)
            sys.stdout.write('\x1b[0K')
            if idx == self.pos:
                sys.stdout.write(term(line,
                                      'yellow',
                                      'purple',
                                      'bold') + '\n' + reset + '\r')
            else:
                sys.stdout.write(line + '\n' + reset + '\r')
        sys.stdout.write('\x1b[{}A'.format(self.max_lines_range))

    def execute_command(self):
        p = subprocess.Popen(
            self.args_for_action,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
        )
        (output, err) = p.communicate()
        if err:
            sys.stdout.write(err.decode(self.output_encodeing))
        else:
            sys.stdout.write(output.decode(self.output_encodeing))


def get_ttyname():
    for file_obj in (sys.stdin, sys.stdout, sys.stderr):
        if file_obj.isatty():
            return os.ttyname(file_obj.fileno())


def get_char():
    try:
        from msvcrt import getch
        return getch()
    except ImportError:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch
