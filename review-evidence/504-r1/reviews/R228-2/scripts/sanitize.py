#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Neutralise local absolute paths in a text receipt, in place or to a copy.

Usage: SANITIZE_MAP=<map-file> sanitize.py <src> [<dst>]
The map file is local and unpublished: one `<local-prefix>\t<placeholder>`
pair per line, applied in order (longest prefixes first), so published
receipts carry placeholders such as $CLONE, $REVIEW_OUT and $HOME instead of
this machine's layout.
"""

import os
import sys
from pathlib import Path


def main() -> None:
    pairs = [line.split("\t", 1)
             for line in Path(os.environ["SANITIZE_MAP"]).read_text().splitlines()
             if "\t" in line]
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else src
    text = src.read_text(errors="replace")
    for old, new in pairs:
        text = text.replace(old, new)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text)


if __name__ == "__main__":
    main()
