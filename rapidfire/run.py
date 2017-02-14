import argparse
import textwrap

from .ansi import term
from .parser import ParsePyFile
from .config import Config, make_rapidfire_config

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

    parser.add_argument('-i', '--init',
                        action='store_true',
                        default=False,
                        help='init rapid fire')
    return parser


def main():
    parser = get_argparser()
    args = parser.parse_args()
    if args.init:
        make_rapidfire_config()
    else:
        config = Config()
        rap_parser = ParsePyFile(config.rapidfire_pyfile_path)
        rap_parser.set_code_obj(args.function_name)
        rap_parser.run()
