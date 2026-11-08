# SPDX-License-Identifier: MIT
"""Print .text/.rodata output-section sizes from GNU ld map files.

Usage: python3 -I map_sections.py LABEL=PATH [LABEL=PATH ...]
An output-section line in a GNU ld map starts at column 0 with the section
name, followed by its address and size (possibly on the next line).
"""
import re
import sys

SECTIONS = (".text", ".rodata")


def sizes(path):
    out = {}
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    for i, line in enumerate(lines):
        for name in SECTIONS:
            if line == name or line.startswith(name + " "):
                rest = line[len(name):].split()
                if len(rest) < 2 and i + 1 < len(lines):
                    rest = lines[i + 1].split()
                if len(rest) >= 2 and re.fullmatch(r"0x[0-9a-fA-F]+", rest[1]):
                    out.setdefault(name, int(rest[1], 16))
    helper = sum(1 for l in lines if "__lshrdi3" in l)
    return out, helper


def main(argv):
    for arg in argv:
        label, path = arg.split("=", 1)
        s, helper = sizes(path)
        total = sum(s.get(n, 0) for n in SECTIONS)
        parts = " ".join(f"{n}={s.get(n)}" for n in SECTIONS)
        print(f"{label} {parts} sum={total} lshrdi3_lines={helper}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
