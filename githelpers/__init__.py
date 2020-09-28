import re
import subprocess


def run(cmd):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').rstrip()


def get_len(colored_str):
    escape_sequences_sub = re.compile(r"""
        \x1b     # literal ESC
        \[       # literal [
        [;\d]*   # zero or more digits or semicolons
        [A-Za-z] # a letter
        """, re.VERBOSE).sub
    uncolored = escape_sequences_sub("", colored_str)
    return len(uncolored)


def as_col(text, need_size):
    real_len = get_len(text)
    spaces = need_size - real_len
    if spaces > 0:
        text += " " * spaces
    return text
