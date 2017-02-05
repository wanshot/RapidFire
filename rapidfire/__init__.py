__version__ = '0.0.0'
__license__ = 'MIT License',
__author__ = 'wanshot'
__author_email__ = 'nishikawa0228@sj9.so-net.ne.jp'

__logo__ = """
     ____              _     _________
    / __ \____ _____  (_)___/ / ____(_)_______
   / /_/ / __ `/ __ \/ / __  / /_  / / ___/ _ \\
  / _, _/ /_/ / /_/ / / /_/ / __/ / / /  /  __/
 /_/ |_|\__,_/ .___/_/\__,_/_/   /_/_/   \___/
            /_/
"""

from .core import Core


def render(*args, **kwargs):
    # call @render
    if len(args) == 1 and callable(args[0]):
        return Core(args[0], **kwargs)

    def inner(obj):
        # call @render()
        return Core(obj, **kwargs)
    return inner
