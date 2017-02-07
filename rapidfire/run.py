import argparse
import textwrap

from .ansi import term
from .parser import ParsePyFile
from .config import Config

LOGAPPNAME = 'Selection Display Interface'


def get_argparser():
    from rapidfire import __version__, __logo__

    parser = argparse.ArgumentParser(
        usage='RapidFire',
        description=textwrap.dedent(
            term(LOGAPPNAME, {'fg_color': 'red'}) + '\n' +
            term(__logo__, {'fg_color': 'red', 'style': 'bold'})
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
    config = Config()

    rf_parser = ParsePyFile(config.rapidfire_pyfile_path)
    rf_parser.set_code_obj(args.function_name)
    rf_parser.run()
