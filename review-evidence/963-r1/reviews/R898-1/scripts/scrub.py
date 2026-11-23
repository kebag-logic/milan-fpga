#!/usr/bin/env python3
"""Replace host-specific paths in text receipts with neutral placeholders, in place.

Usage: scrub.py --map OLD=NEW [--map OLD=NEW ...] [--user NAME] -- <file>...
Each --map is applied in the order given (give the longest paths first); --user replaces that account name, as a
whole word, with <user>. Binary files are skipped. This round mapped its packet, review clone, pinned SDK, pinned
Verilator, tools directory and home directory to <packet>, <review-clone>, <pinned-rv32-sdk>, <pinned-verilator>,
<tools> and <home>.
"""
import argparse
import re
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--map', action='append', default=[], help='OLD=NEW')
    ap.add_argument('--user')
    ap.add_argument('files', nargs='*')
    args = ap.parse_args()
    pairs = [m.split('=', 1) for m in args.map]
    for name in args.files:
        p = Path(name)
        try:
            text = p.read_text()
        except UnicodeDecodeError:
            continue
        new = text
        for old, rep in pairs:
            new = new.replace(old, rep)
        if args.user:
            new = re.sub(r'\b' + re.escape(args.user) + r'\b', '<user>', new)
        if new != text:
            p.write_text(new)
            print('scrubbed', p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
