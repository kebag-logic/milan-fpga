#!/usr/bin/env python3
"""Replace host path prefixes in receipts with neutral placeholders, in place.

Usage: normalise.py PACKET CLONE
  PACKET -> <packet>, CLONE -> <clone>, the home directory -> $HOME.
Only text files under PACKET/receipts are rewritten; prints the files changed.
"""
import os
import sys
from pathlib import Path


def main():
    packet, clone = (str(Path(arg).resolve()) for arg in sys.argv[1:3])
    home = os.path.expanduser("~")
    pairs = [(packet, "<packet>"), (clone, "<clone>"), (home, "$HOME")]
    for path in sorted(Path(packet, "receipts").rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        new = text
        for old, placeholder in pairs:
            new = new.replace(old, placeholder)
        if new != text:
            path.write_text(new)
            print(path.relative_to(packet))
    return 0


if __name__ == "__main__":
    sys.exit(main())
