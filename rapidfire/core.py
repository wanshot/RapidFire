import os
import sys
import termios
import tty
import subprocess
import locale
import select

from wcwidth import wcwidth

from .ansi import term, ANSI_SEQUENCES
from .terminalsize import get_terminal_size
from .parser import ParsePyFile
from .config import Config
from .clipboard import copy_to_clipboard
from .pager import Paginator


def get_locale():
    locale.setlocale(locale.LC_ALL, '')
    output_encoding = locale.getpreferredencoding()
    return output_encoding


class Core(object):

    def __init__(self, function, action_name=None, input_encoding=None, **option):
        selections = function()
        function_name = function.__name__

        try:
            _ = (x for x in selections)  # noqa
        except:
            sys.exit()

        encoding = get_locale()
        with RapidFire(encoding, selections, function_name, input_encoding, **option) as rap:
            exit_code = rap.loop()
        sys.exit(exit_code)


class RapidFire(object):

    def __init__(self, output_encodeing, selections, function_name, input_encoding='utf-8', **option):
        self.width, self.height = get_terminal_size()
        self.selections = selections
        self.pager = Paginator(selections, self.height - 1)  # subtract prompt line
        self.page_number = 1
        self.function_name = function_name
        self.output_encodeing = output_encodeing
        self.input_encoding = input_encoding
        self.option = option
        self.pos = 1
        self.finished = False
        self.args_for_action = None
        self.prompt = Prompt()

    def __enter__(self):
        self.config = Config()
        ttyname = get_ttyname()
        sys.stdin = open(ttyname)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write('\x1b[?25h\x1b[0J')
        if self.finished:
            return
        elif self.option.get('next_action') and not self.finished:
            rap_parser = ParsePyFile(self.config.rapidfire_pyfile_path)
            rap_parser.set_code_obj(self.option.get('next_action'))
            rap_parser.run({self.function_name: self.args_for_action})
        elif self.args_for_action and self.option.get('clipboard'):
            copy_to_clipboard(self.args_for_action)
        else:
            self.execute_command()

    def loop(self):
        page = self.render()
        while True:
            on_input, byte = get_byte()
            if on_input:
                key = ANSI_SEQUENCES.get(byte)
                try:

                    # search selections
                    if key is None:
                        self.prompt.update(byte.decode(self.output_encodeing))
                        self.pos = 1

                    # Exit rapidfire
                    elif key.name in self.config.get_keys('QUITE'):
                        self.finished = True
                        break

                    # Position Up
                    elif key.name in self.config.get_keys('UP'):
                        if self.pos > 1:
                            self.pos -= 1
                        elif page.has_previous():
                            self.page_number -= 1
                            page = self.pager.page(self.page_number)
                            self.pos = len(page)
                        else:
                            self.page_number = page.paginator.num_pages
                            page = self.pager.page(self.page_number)
                            self.pos = len(page)

                    # Position Down
                    elif key.name in self.config.get_keys('DOWN'):
                        if self.pos < len(page):
                            self.pos += 1
                        elif page.has_next():
                            self.page_number += 1
                            self.pos = 1
                        else:
                            self.page_number = 1
                            self.pos = 1

                    # Selecting
                    elif key.name in self.config.get_keys('ENTER') or byte == b'\n':
                        self.args_for_action = page[self.pos - 1]
                        break

                    # Erase Input Char
                    elif key.name in self.config.get_keys('ERASE_CHAR'):
                        self.prompt.erase_one()
                        self.pos = 1

                    # Update Screen
                    page = self.render()
                except:
                    sys.stdout.write('\x1b[?0h\x1b[0J')
        return 1

    def render(self):
        self.search(self.prompt.query)
        page = self.pager.page(self.page_number)
        # erase behind the cursor and reset attribute
        reset = '\x1b[0K\x1b[0m'
        sys.stdout.write('\x1b[?25l')  # hide cursor
        sys.stdout.write(reset)        # erase behind the cursor
        sys.stdout.write(term(
            self.truncate_string_by_line('input:{}'.format(self.prompt.query)),
            self.config.normal_line_attribute) + '\n' + reset + '\r')

        for idx in range(1, self.height):
            # subtract prompt line
            eol = '' if self.height - 1 == idx else '\n'
            try:
                if idx == self.pos:
                    sys.stdout.write(
                        term(self.truncate_string_by_line(page[idx - 1]),
                             self.config.select_line_attribute,
                             ) + eol + reset + '\r')
                else:
                    sys.stdout.write(
                        term(self.truncate_string_by_line(page[idx - 1]),
                             self.config.normal_line_attribute,
                             ) + eol + reset + '\r')
            except IndexError:
                sys.stdout.write(eol + reset + '\r')

        # initialize the position of the cursor
        sys.stdout.write('\x1b[{}A'.format(self.height))
        return page

    def search(self, query):
        if query:
            new_selections = [selection for selection in self.selections
                              if self.prompt.query in selection]
        else:
            new_selections = self.selections
        self.pager = Paginator(new_selections, self.height - 1)
        self.page_number = 1

    def execute_command(self):
        p = subprocess.Popen(
            self.args_for_action,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            executable=self.config.shell,
        )
        (output, err) = p.communicate()
        if err:
            sys.stdout.write(err.decode(self.output_encodeing))
        else:
            sys.stdout.write(output.decode(self.output_encodeing))

    def truncate_string_by_line(self, line):
        counter = 0
        string = []
        for s in line:
            counter += wcwidth(s)
            if counter > self.width:
                break
            else:
                string.append(s)
        return ''.join(string)


class Prompt(object):

    def __init__(self):
        self.query = ''

    def update(self, ch):
        self.query += ch

    def erase_one(self):
        self.query = self.query[:-1]

    def __repr__(self):
        return ('{cls.__name__}(query={self.query})'
                .format(cls=type(self), self=self))


def get_ttyname():
    for file_obj in (sys.stdin, sys.stdout, sys.stderr):
        if file_obj.isatty():
            return os.ttyname(file_obj.fileno())


def get_byte():
    timeout = 0.1
    on_input = False
    input_byte = b''
    try:
        from msvcrt import getch
        return True, getch()
    except ImportError:
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            readers, _, _ = select.select([fd], [], [], timeout)
            if readers:
                on_input = True
                try:
                    input_byte = os.read(fd, 1024)
                except:
                    on_input = False
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return on_input, input_byte
