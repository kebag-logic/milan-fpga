#!/usr/bin/env python3
"""R328-4: compare SystemVerilog code tokens (comments and whitespace removed)
of one path between two commits. Exit 0 iff the token streams are identical.
Usage: code_token_diff.py <repo> <base> <head> <path>...
"""
import re
import subprocess
import sys

TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_][A-Za-z0-9_$]*|\d[\w\']*|\S')


def tokens(repo, rev, path):
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"//[^\n]*", " ", text)
    return TOKEN.findall(text)


def main():
    repo, base, head, *paths = sys.argv[1:]
    status = 0
    for path in paths:
        a, b = tokens(repo, base, path), tokens(repo, head, path)
        same = a == b
        print(f"{'CODE-IDENTICAL' if same else 'CODE-CHANGED'} {path} "
              f"tokens {len(a)} -> {len(b)}")
        status |= 0 if same else 1
    sys.exit(status)


if __name__ == "__main__":
    main()
