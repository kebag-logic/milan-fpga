#!/usr/bin/env python3
"""Static stand-in for xvlog's VRFC 10-3380 (identifier used before its declaration):
for every `logic` declared in a module body, report the first non-comment line that
names it above its declaration.

Usage: decl_order_scan.py FILE...   prints "FILE|identifier|first use line|decl line"
It is a reviewer's corroboration only; xvlog stops at the first error per module,
which this scan does not model.
"""
import re
import sys

DECL = re.compile(r"^\s*logic\b(?:\s*\[[^\]]*\])*\s+([A-Za-z_]\w*(?:\s*(?:\[[^\]]*\]\s*)*,\s*[A-Za-z_]\w*)*)")


def strip(line, in_block):
    out = ""
    i = 0
    while i < len(line):
        if in_block:
            j = line.find("*/", i)
            if j < 0:
                return out, True
            i, in_block = j + 2, False
        elif line.startswith("//", i):
            break
        elif line.startswith("/*", i):
            in_block, i = True, i + 2
        else:
            out += line[i]
            i += 1
    return out, in_block


def main() -> int:
    for path in sys.argv[1:]:
        lines, blk = [], False
        for raw in open(path):
            s, blk = strip(raw, blk)
            lines.append(s)
        decls = {}
        depth = 0  # declarations inside begin/end blocks or functions are local; only depth 0 counts
        for n, s in enumerate(lines, 1):
            if depth == 0:
                m = DECL.match(s)
                if m:
                    for name in re.split(r"\s*(?:\[[^\]]*\]\s*)*,\s*", m.group(1)):
                        name = re.sub(r"\[.*", "", name).strip()
                        decls.setdefault(name, n)
            depth += len(re.findall(r"\b(begin|function|task)\b", s))
            depth -= len(re.findall(r"\b(end|endfunction|endtask)\b", s))
            depth = max(depth, 0)
        for name, dl in sorted(decls.items(), key=lambda kv: kv[1]):
            w = re.compile(r"\b" + re.escape(name) + r"\b")
            for n, s in enumerate(lines[: dl - 1], 1):
                if w.search(s):
                    print(f"{path}|{name}|{n}|{dl}")
                    break
    return 0


if __name__ == "__main__":
    sys.exit(main())
