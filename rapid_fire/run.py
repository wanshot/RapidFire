# -*- coding: utf-8 -*-

import argparse
import textwrap

from .ansi import term
from .parser import ParsePyFile

LOGAPPNAME = 'Selection Display Interface'


def get_argparser():
    from rapid_fire import __version__, __logo__

    parser = argparse.ArgumentParser(
        usage='RapidFire',
        description=textwrap.dedent(
            term(LOGAPPNAME, fg_color='red') + '\n' +
            term(__logo__, fg_color='red', style='bold')
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('-v', '--version',
                        action='version',
                        version='{version}'.format(version=__version__))

    parser.add_argument('function_name',
                        nargs='?',
                        type=str)

    parser.add_argument('-c', '--into_clipboald',
                        action='store_true',
                        default=False,
                        help='copy to clipboald')
    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args()

    rf_parser = ParsePyFile('/Users/wan/rffile.py')
    rf_parser.set_code_obj(args.function_name)
    rf_parser.run()
