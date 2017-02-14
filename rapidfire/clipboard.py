import os
import platform
import subprocess


def copy_to_clipboard(text):
    if os.name == 'mac' or platform.system() == 'Darwin':
        p = subprocess.Popen(['pbcopy', 'w'],
                             stdin=subprocess.PIPE,
                             close_fds=True)
        p.communicate(input=text.encode('utf-8'))
    else:
        pass
