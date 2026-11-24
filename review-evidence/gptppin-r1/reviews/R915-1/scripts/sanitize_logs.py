#!/usr/bin/env python3
"""sanitize_logs.py SRC_DIR DST_DIR: copy every file in SRC_DIR to DST_DIR with
absolute host paths replaced by placeholders (<scratch>, <tools>, <home>)."""
import re
import sys
from pathlib import Path

RULES = [
    (re.compile(r"/home/[^/\s'\"]+/\.local/share/containers/[^\s'\"]*?/usr/share/verilator"),
     "<verilator-root>"),
    (re.compile(r"/home/[^/\s'\"]+/\.local/share/containers/[^\s'\"]*"), "<toolchain>"),
    (re.compile(r"/srv/[^\s'\"]*"), "<scratch>"),
    (re.compile(r"/data/[^\s'\"]*"), "<tools>"),
    (re.compile(r"/home/[^/\s'\"]+"), "<home>"),
]


def main() -> int:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    for f in sorted(src.iterdir()):
        if not f.is_file():
            continue
        text = f.read_text(errors="replace")
        for pat, rep in RULES:
            text = pat.sub(rep, text)
        (dst / f.name).write_text(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
