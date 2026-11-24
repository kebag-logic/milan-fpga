#!/usr/bin/env python3
"""Check that every internal name a harness touches is public in the built model.

usage: probe_check.py OBJDIR HARNESS.cpp [HARNESS2.cpp ...]
Extracts every `<scope>__DOT__...` identifier from the harness sources, classifies
each as WRITTEN (an `=`/`+=`... assignment whose left side is the name) or READ,
and looks it up in the model's generated scope table (__Syms*.cpp varInsert):
a READ name must be registered VLVF_PUB_RD or VLVF_PUB_RW; a WRITTEN name must be
VLVF_PUB_RW. Static parameter members (`::name`) must exist in the root header.
Exit 0 = all covered, 1 = a name is missing or under-privileged.
"""
import re
import sys
from pathlib import Path

NAME = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*__DOT__[A-Za-z0-9_]+)")
INSERT = re.compile(r"varInsert\(\"[^\"]+\", &\(TOP\.([A-Za-z0-9_]+)\)[^;]*?(VLVF_PUB_RW|VLVF_PUB_RD)")


def main() -> int:
    obj = Path(sys.argv[1])
    syms = "".join(p.read_text() for p in obj.glob("*__Syms*.cpp"))
    roots = "".join(p.read_text() for p in obj.glob("*___024root.h"))
    public = {m.group(1): m.group(2) for m in INSERT.finditer(syms)}
    used: dict[str, set[str]] = {}
    for src in sys.argv[2:]:
        text = Path(src).read_text()
        for m in NAME.finditer(text):
            name = m.group(1)
            # strip a trailing comment-only mention: skip names inside // comments
            line_start = text.rfind("\n", 0, m.start()) + 1
            line = text[line_start:text.find("\n", m.end())]
            if "//" in line and line.index("//") < m.start() - line_start:
                continue
            rest = text[m.end():m.end() + 4]
            before = text[max(0, m.start() - 2):m.start()]
            static = before.endswith("::")
            written = bool(re.match(r"\s*(=(?!=)|\+=|-=|\|=|&=|\^=|\+\+|--)", rest))
            kind = "static" if static else ("write" if written else "read")
            used.setdefault(name, set()).add(kind)
    bad = 0
    for name in sorted(used):
        kinds = used[name]
        if "static" in kinds:
            ok = re.search(r"\b" + re.escape(name) + r"\b", roots) is not None
            state = "static-member present" if ok else "STATIC MEMBER MISSING"
        else:
            flag = public.get(name)
            need = "VLVF_PUB_RW" if "write" in kinds else None
            ok = flag is not None and (need is None or flag == need)
            state = flag or "NOT PUBLIC"
        print(f"{'ok ' if ok else 'BAD'} {name:70s} {'/'.join(sorted(kinds)):10s} {state}")
        bad += not ok
    print(f"{obj.name}: {len(used)} names, {bad} uncovered")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
