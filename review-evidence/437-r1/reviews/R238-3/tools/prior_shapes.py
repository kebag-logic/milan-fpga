#!/usr/bin/env python3
"""Pull every page a prior public review round published inline (a quoted or
backticked string carrying an escaped newline and an ATX heading), decode
it, and write a probe list tagged by round.

Usage: prior_shapes.py <out.json> <round>=<body.md> ...
"""
import json
import re
import sys
from pathlib import Path

PATTERNS = [re.compile(r'"((?:[^"\\\n]|\\.)*?\\n(?:[^"\\\n]|\\.)*?)"'),
            re.compile(r'`((?:[^`\n])*?\\n(?:[^`\n])*?)`')]


def decode(raw: str) -> str:
    out, i = [], 0
    while i < len(raw):
        c = raw[i]
        if c == "\\" and i + 1 < len(raw):
            nxt = raw[i + 1]
            out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(nxt, "\\" + nxt))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def main() -> int:
    out = Path(sys.argv[1])
    rows, seen = [], set()
    for arg in sys.argv[2:]:
        tag, path = arg.split("=", 1)
        text = Path(path).read_text()
        for pattern in PATTERNS:
            for m in pattern.finditer(text):
                page = decode(m.group(1))
                if "\n#" not in "\n" + page or (tag, page) in seen:
                    continue
                if not page.endswith("\n"):
                    page += "\n"
                seen.add((tag, page))
                rows.append({"name": f"{tag} #{len(rows)}", "round": tag, "page": page})
    out.write_text(json.dumps(rows, indent=1))
    print(f"{len(rows)} published pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
